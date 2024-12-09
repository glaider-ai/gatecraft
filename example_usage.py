from gatecraft import Gatecraft, SemanticCondition


def main():
    # Initialize the Gatecraft system
    gc = Gatecraft()

    # Create users
    alice = gc.create_user(user_id=1, name='Alice')
    bob = gc.create_user(user_id=2, name='Bob')

    # Create roles with conditions
    cat_lover_role = gc.create_role(role_id=1, name='Cat Lover')
    cat_condition = SemanticCondition(term='cat', threshold=0.78)
    gc.add_condition_to_role(cat_lover_role, cat_condition)

    everything_except_cats_role = gc.create_role(role_id=2, name='Everything Except Cats')
    inverse_cat_condition = SemanticCondition(term='cat', threshold=0.78, inverse=True)
    gc.add_condition_to_role(everything_except_cats_role, inverse_cat_condition)

    # Assign roles to users
    gc.assign_role(alice, cat_lover_role)
    gc.assign_role(bob, everything_except_cats_role)

    # Add entities (documents)
    gc.add_entity(entity_id=1, data='Cute kitten playing with a ball of yarn.')
    gc.add_entity(entity_id=2, data='Dog training and obedience tips.')

    # Check access
    print(f"Alice access to Entity 1: {gc.is_access_allowed(alice, 1)}")  # Should be True
    print(f"Alice access to Entity 2: {gc.is_access_allowed(alice, 2)}")  # Should be False
    print(f"Bob access to Entity 1: {gc.is_access_allowed(bob, 1)}")      # Should be False
    print(f"Bob access to Entity 2: {gc.is_access_allowed(bob, 2)}")      # Should be True


if __name__ == '__main__':
    main()
