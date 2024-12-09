from gatecraft.core.user import User
from gatecraft.core.entity import Entity
from gatecraft.db.semantic_database import SemanticDatabase


class AccessControlPolicy:
    """
    Implements the access control policy logic.
    """

    def __init__(self, database):
        self.database = database

    def is_access_allowed(self, user, entity):
        """
        Determines if a user has access to an entity.
        Returns True if:
        1. At least one regular condition matches OR
        2. All inverse conditions match
        """
        for role in user.get_roles():
            regular_conditions = []
            inverse_conditions = []
            
            # Separate regular and inverse conditions
            for condition in role.get_conditions():
                if condition.inverse:
                    inverse_conditions.append(condition)
                else:
                    regular_conditions.append(condition)
            
            # If there are regular conditions, at least one must match
            if regular_conditions:
                for condition in regular_conditions:
                    if condition.evaluate(user, entity, self.database):
                        return True
            
            # If there are inverse conditions, all must match
            if inverse_conditions:
                if all(condition.evaluate(user, entity, self.database) 
                      for condition in inverse_conditions):
                    return True
                    
        return False
