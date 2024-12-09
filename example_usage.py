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
    gc.add_entity(entity_id=1, data='Breeds of cats and their characteristics.')      # Cat content
    gc.add_entity(entity_id=2, data='Tips on dog training and obedience.')            # Dog content
    gc.add_entity(entity_id=3, data='Man running in the park.')                    # Violent content
    gc.add_entity(entity_id=4, data='How to train cats effectively.')                 # Cat content

    # Simulate user requests
    requests = [
        {'user': bob, 'query': 'Show me dog training tips'},
        {'user': bob, 'query': 'Tell me about a man running in the park'},
        {'user': bob, 'query': 'How to train cats'},
        {'user': alice, 'query': 'Show me dog breeds'},
        {'user': alice, 'query': 'Dog training tips'},
    ]

    for req in requests:
        user = req['user']
        query = req['query']
        print(f"\nUser '{user.name}' is making a request: '{query}'")

        # Simulate retrieval of relevant entities
        relevant_entities = gc.retrieve_entities(query)

        if not relevant_entities:
            print("No relevant documents found for the query.")
            continue

        # Check access for each retrieved entity
        access_allowed = False
        accessible_entities = []

        for entity in relevant_entities:
            if gc.is_access_allowed(user, entity.entity_id):
                access_allowed = True
                accessible_entities.append(entity)

        print(f"Access Status: {'ALLOWED' if access_allowed else 'DENIED'}")

        if access_allowed:
            print("Proceeding with Retrieval-Augmented Generation...")
            print("Retrieved Documents to be sent to LLM:")
            for idx, entity in enumerate(accessible_entities, start=1):
                print(f"Document {entity.entity_id}: {entity.data}")
        else:
            print("Access denied. Cannot proceed with the request.")


if __name__ == '__main__':
    main()
