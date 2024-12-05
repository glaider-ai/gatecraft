from NeverMind.core.user import User
from NeverMind.core.entity import Entity
from NeverMind.db.semantic_database import SemanticDatabase


class AccessControlPolicy(metaclass=type):
    """
    Implements the access control policy logic.
    """

    def __init__(self, database: SemanticDatabase):
        self.database = database

    def is_access_allowed(self, user: User, entity: Entity) -> bool:
        """
        Determines if a user has access to an entity.
        """
        user_permissions = set()
        for role in user.get_roles():
            user_permissions.update(role.get_permissions())

        for permission in user_permissions:
            for condition in permission.get_conditions():
                if condition.evaluate(user, entity, self.database):
                    return True
        return False 
    