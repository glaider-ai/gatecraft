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
    pinecone_index_name = 'test-rag-rbac-0'

    vector_store = PineconeVectorStore(
        api_key=pinecone_api_key,
        environment=pinecone_environment,
        index_name=pinecone_index_name
    )
    semantic_db = SemanticDatabase(vector_store, similarity_threshold=0.88)

    # Create Users
    alice = User(user_id=1, name='Alice')
    bob = User(user_id=2, name='Bob')

    # Create Roles
    cat_lover_role = Role(role_id=1, name='Cat Lover')
    everything_except_cats_role = Role(role_id=2, name='Everything Except Cats')

    # Create Permissions
    cat_permission = Permission(permission_id=1, name='Access Cat Content')
    all_except_cats_permission = Permission(permission_id=2, name='Access All Except Cats')

    # Define Conditions
    cat_condition = SemanticCondition(term='cat', threshold=0.78)
    inverse_cat_condition = SemanticCondition(term='cat', threshold=0.78, inverse=True)

    # Assign Conditions to Permissions
    cat_permission.add_condition(cat_condition)
    all_except_cats_permission.add_condition(inverse_cat_condition)

    # Assign Permissions to Roles
    cat_lover_role.add_permission(cat_permission)
    everything_except_cats_role.add_permission(all_except_cats_permission)

    # Assign Roles to Users
    alice.add_role(cat_lover_role)
    bob.add_role(everything_except_cats_role)

    # Create Entities (Documents)
    entities = [
        Entity(entity_id=1, data='Cute kitten playing with a ball of yarn.'),
        Entity(entity_id=2, data='Killer running in the park.'),
        Entity(entity_id=3, data='Guide to train your slave.'),
        Entity(entity_id=4, data='Tips on dog training and obedience.'),
        Entity(entity_id=5, data='Breeds of cats and their characteristics.'),
    ]

    # Store entity embeddings in Pinecone
    for entity in entities:
        embedding = semantic_db.get_embedding(entity.data)
        semantic_db.store_embedding(f"entity_{entity.entity_id}", embedding)

    # Add entities to semantic_db for retrieval
    semantic_db.entities = entities

    # Initialize Access Control Policy
    policy = AccessControlPolicy(database=semantic_db)

    # Create a permission that blocks sensitive content
    safe_permission = Permission(1, "Safe Content Only")

    # Add inverse conditions to block sensitive content
    safe_permission.add_condition(SemanticCondition("violent", threshold=0.7, inverse=True))
    safe_permission.add_condition(SemanticCondition("adult", threshold=0.7, inverse=True))
    safe_permission.add_condition(SemanticCondition("sensitive", threshold=0.7, inverse=True))

    # Create a role and assign the permission
    safe_role = Role(1, "Safe Content Viewer")
    safe_role.add_permission(safe_permission)

    # Assign the role to a user
    safe_user = User(1, "Safe User")
    safe_user.add_role(safe_role)

    return {
        'users': [alice, bob, safe_user],
        'entities': entities,
        'policy': policy,
        'semantic_db': semantic_db
    }

def simulate_rag_request(user, request_text, policy, semantic_db):
    print(f"\nUser '{user.name}' is making a request: '{request_text}'")

    # Create an Entity for the request
    request_entity = Entity(entity_id=999, data=request_text)

    # Check access
    has_access = policy.is_access_allowed(user, request_entity)
    access_status = 'ALLOWED' if has_access else 'DENIED'
    print(f"Access Status: {access_status}")

    # If access is allowed, proceed with RAG
    if has_access:
        print("Proceeding with Retrieval-Augmented Generation...")

        # Get embedding for the request
        request_embedding = semantic_db.get_embedding(request_text)

        # Query similar entities
        matches = semantic_db.query_similar(request_embedding, top_k=5)

        # Retrieve the actual texts of the matched entities
        retrieved_texts = []
        for match in matches:
            if not match['id'].startswith('entity_'):
                continue  # Skip non-entity embeddings
            entity_id_str = match['id'].split('_')[1]
            try:
                entity_id = int(entity_id_str)  # Extract the entity_id
            except ValueError:
                continue  # Skip if unable to parse integer
            entity = next((e for e in semantic_db.entities if e.entity_id == entity_id), None)
            if entity:
                retrieved_texts.append(entity.data)

        # Print what would be sent to the LLM
        print("Retrieved Documents to be sent to LLM:")
        for idx, text in enumerate(retrieved_texts, 1):
            print(f"Document {idx}: {text}")

    else:
        print("Access denied. Cannot proceed with the request.")

def main():
    system = setup_rbac_system()
    users = system['users']
    policy = system['policy']
    semantic_db = system['semantic_db']

    # Test requests
    user_requests = [
        ("Bob", "Show me dog training tips"),  # Should be ALLOWED
        ("Bob", "Tell me about a killer running in the park"),         # Should be ALLOWED
        ("Bob", "How to train cats"),       # Should be ALLOWED
        ("Alice", "Show me cat breeds"),       # Should be ALLOWED
        ("Alice", "Dog training tips"),        # Should be DENIED
    ]

    for user_name, request in user_requests:
        user = next(u for u in users if u.name == user_name)
        simulate_rag_request(user, request, policy, semantic_db)


if __name__ == '__main__':
    main()
    