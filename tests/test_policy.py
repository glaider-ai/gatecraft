import unittest
from semantic_rbac.core.user import User
from semantic_rbac.core.role import Role
from semantic_rbac.core.permission import Permission
from semantic_rbac.core.entity import Entity
from semantic_rbac.core.policy import AccessControlPolicy
from semantic_rbac.utils.semantic_condition import SemanticCondition
from semantic_rbac.db.semantic_database import SemanticDatabase
from semantic_rbac.db.mock_vector_store import MockVectorStore

class TestPolicy(unittest.TestCase):

    def setUp(self):
        vector_store = MockVectorStore()
        self.semantic_db = SemanticDatabase(vector_store)
        self.policy = AccessControlPolicy(database=self.semantic_db)

        # Users
        self.user = User(user_id=1, name='Test User')

        # Roles
        self.role = Role(role_id=1, name='Test Role')

        # Permissions
        self.permission = Permission(permission_id=1, name='Test Permission')
        condition = SemanticCondition(term='test', threshold=0.5)
        self.permission.add_condition(condition)

        # Assign permissions and roles
        self.role.add_permission(self.permission)
        self.user.add_role(self.role)

        # Entities
        self.entity = Entity(entity_id=1, data='This is a test entity.')

    def test_access_allowed(self):
        allowed = self.policy.is_access_allowed(self.user, self.entity)
        self.assertTrue(allowed)

if __name__ == '__main__':
    unittest.main() 
    