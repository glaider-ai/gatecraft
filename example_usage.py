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
    # Load environment variables
    load_dotenv()

    # Initialize OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key

    # Initialize Pinecone vector store
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_environment = os.getenv('PINECONE_ENVIRONMENT')
    pinecone_index_name = 'rbac-rag-index'

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
    cat_lover_role = Role(role_id=1, name='Cat Lover')
    dog_lover_role = Role(role_id=2, name='Dog Lover')

    # Create Permissions
    cat_permission = Permission(permission_id=1, name='Access Cat Content')
    dog_permission = Permission(permission_id=2, name='Access Dog Content')

    # Define Conditions
    cat_condition = SemanticCondition(term='cat')
    dog_condition = SemanticCondition(term='dog')

    # Assign Conditions to Permissions
    cat_permission.add_condition(cat_condition)
    dog_permission.add_condition(dog_condition)

    # Assign Permissions to Roles
    cat_lover_role.add_permission(cat_permission)
    dog_lover_role.add_permission(dog_permission)

    # Assign Roles to Users
    alice.add_role(cat_lover_role)
    bob.add_role(dog_lover_role)

    # Create Entities (Documents)
    entities = [
        Entity(entity_id=1, data='Cute kitten playing with a ball of yarn.'),
        Entity(entity_id=2, data='Puppy running in the park.'),
        Entity(entity_id=3, data='Guide to caring for your pet cat.'),
        Entity(entity_id=4, data='Tips on dog training and obedience.'),
        Entity(entity_id=5, data='Breeds of cats and their characteristics.'),
    ]

    # Store entity embeddings in Pinecone
    for entity in entities:
        embedding = semantic_db.get_embedding(entity.data)
        semantic_db.store_embedding(f"entity_{entity.entity_id}", embedding)

    # Initialize Access Control Policy
    policy = AccessControlPolicy(database=semantic_db)

    return {
        'users': [alice, bob],
        'entities': entities,
        'policy': policy
    }

def simulate_rag_request(user, request_text, policy):
    print(f"\nUser '{user.name}' is making a request: '{request_text}'")

    # Create an Entity for the request
    request_entity = Entity(entity_id=999, data=request_text)

    # Check access
    has_access = policy.is_access_allowed(user, request_entity)
    access_status = 'ALLOWED' if has_access else 'DENIED'
    print(f"Access Status: {access_status}")

    # If access is allowed, proceed with RAG (mocked here)
    if has_access:
        print("Proceeding with Retrieval-Augmented Generation...")
        # Mock RAG process (e.g., retrieve relevant documents and generate response)
    else:
        print("Access denied. Cannot proceed with the request.")

def main():
    system = setup_rbac_system()
    users = system['users']
    policy = system['policy']

    # Simulate RAG requests
    user_requests = [
        ("Alice", "Show me pictures of cats"),
    ]

    # Create a mapping of user names to User objects
    user_mapping = {user.name: user for user in users}

    for user_name, request_text in user_requests:
        user = user_mapping[user_name]
        simulate_rag_request(user, request_text, policy)

if __name__ == '__main__':
    main()
    