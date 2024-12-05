import os
from NeverMind.core.user import User
from NeverMind.core.role import Role
from NeverMind.core.permission import Permission
from NeverMind.utils.semantic_condition import SemanticCondition
from NeverMind.core.entity import Entity
from NeverMind.core.policy import AccessControlPolicy
from NeverMind.db.semantic_database import SemanticDatabase
from NeverMind.db.pinecone_vector_store import PineconeVectorStore
import openai
from dotenv import load_dotenv


def setup_rbac_system():
    # Initialize OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key

    # Initialize Pinecone vector store
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')
    pinecone_index_name = 'test-rag-rbac-0'

    vector_store = PineconeVectorStore(
        api_key=pinecone_api_key,
        environment=pinecone_environment,
        index_name=pinecone_index_name
    )
    semantic_db = SemanticDatabase(vector_store)

    # Create Users
    alice = User(user_id=1, name='Alice')
    bob = User(user_id=2, name='Bob')

    # Create Roles
    animal_role = Role(role_id=1, name='Animal Access')
    cat_role = Role(role_id=2, name='Cat Access')

    # Create Permissions
    animal_permission = Permission(permission_id=1, name='Access Animal Data')
    cat_permission = Permission(permission_id=2, name='Access Cat Data')

    # Define Conditions
    animal_condition = SemanticCondition(term='animal', threshold=0.8)
    cat_condition = SemanticCondition(term='cat', threshold=0.8)

    # Assign Conditions to Permissions
    animal_permission.add_condition(animal_condition)
    cat_permission.add_condition(cat_condition)

    # Assign Permissions to Roles
    animal_role.add_permission(animal_permission)
    cat_role.add_permission(cat_permission)

    # Assign Roles to Users
    alice.add_role(animal_role)
    bob.add_role(cat_role)

    # Create Entities
    entities = [
        Entity(entity_id=1, data='Information about dogs'),
        Entity(entity_id=2, data='Data on cats and their behavior'),
        Entity(entity_id=3, data='Details on automobiles'),
        Entity(entity_id=4, data='Research on feline species'),
    ]

    # Store entity embeddings in Pinecone
    for entity in entities:
        embedding = semantic_db.get_embedding(entity.data)
        semantic_db.store_embedding(f"entity_{entity.entity_id}", embedding)

    # Print index statistics to verify storage
    print("\nPinecone Index Statistics:")
    print(vector_store.describe_index_stats())

    # Initialize Access Control Policy
    policy = AccessControlPolicy(database=semantic_db)

    return {
        'users': [alice, bob],
        'entities': entities,
        'policy': policy
    }


def main():
    system = setup_rbac_system()
    users = system['users']
    entities = system['entities']
    policy = system['policy']

    # Evaluate Access
    for user in users:
        print(f"\nAccess evaluation for {user.name}:")
        for entity in entities:
            has_access = policy.is_access_allowed(user, entity)
            access_status = 'ALLOWED' if has_access else 'DENIED'
            print(f"  Access to '{entity.data}': {access_status}")


if __name__ == '__main__':
    load_dotenv()
    main() 
    