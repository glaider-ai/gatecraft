import os
import openai  # Import OpenAI library
from .core.user import User
from .core.role import Role
from .core.entity import Entity
from .core.policy import AccessControlPolicy
from .db.semantic_database import SemanticDatabase
from .db.pinecone_vector_store import PineconeVectorStore
from .utils.semantic_condition import SemanticCondition
from dotenv import load_dotenv

class Gatecraft:
    def __init__(self, vector_store=None, similarity_threshold=0.85):
        load_dotenv()  # Load environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')
        print(os.getenv('PINECONE_API_KEY'))
        print(os.getenv('PINECONE_ENVIRONMENT'))

        if vector_store is None:
            # Initialize default vector store
            self.vector_store = PineconeVectorStore(
                api_key=os.getenv('PINECONE_API_KEY'),
                environment=os.getenv('PINECONE_ENVIRONMENT'),
                index_name=os.getenv('PINECONE_INDEX_NAME', 'default-index')
            )
        else:
            self.vector_store = vector_store

        self.semantic_db = SemanticDatabase(self.vector_store, similarity_threshold)
        self.policy = AccessControlPolicy(self.semantic_db)
        self.users = {}
        self.roles = {}
        self.entities = {}
        
    def create_user(self, user_id, name):
        user = User(user_id, name)
        self.users[user_id] = user
        return user
    
    def create_role(self, role_id, name, condition=None):
        role = Role(role_id, name)
        if condition:
            role.add_condition(condition)
        self.roles[role_id] = role
        return role
    
    def assign_role(self, user, role):
        user.add_role(role)
    
    def add_entity(self, entity_id, data):
        entity = Entity(entity_id, data)
        self.entities[entity_id] = entity
        embedding = self.semantic_db.get_embedding(data)
        self.semantic_db.store_embedding(f"entity_{entity_id}", embedding)
        return entity

    def is_access_allowed(self, user, entity_id):
        entity = self.entities.get(entity_id)
        if not entity:
            return False
        return self.policy.is_access_allowed(user, entity)

    def add_condition_to_role(self, role, condition):
        role.add_condition(condition) 

    def retrieve_entities(self, query, top_k=1):
        # Get the embedding for the query
        query_embedding = self.semantic_db.get_embedding(query)
        
        # Query the vector store for similar entities
        matches = self.semantic_db.query_similar(query_embedding, top_k=top_k)
        
        # Retrieve the matching entities
        entities = []
        for match in matches:
            entity_id = int(match['id'].replace('entity_', ''))
            entity = self.entities.get(entity_id)
            if entity:
                entities.append(entity)
        return entities
