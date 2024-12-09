
# Gatecraft

Gatecraft is a semantic Role-Based Access Control (RBAC) system with Retrieval-Augmented Generation (RAG) capabilities. It provides a flexible way to manage access control based on semantic similarity and content understanding.

## Features

- Semantic-based access control
- Integration with OpenAI embeddings
- Pinecone vector store support
- Flexible RBAC system
- RAG capabilities

## Installation

```bash
pip install gatecraft
```

## Quick Start

Here's a quick example to get you started with Gatecraft:

```python
from gatecraft import Gatecraft, SemanticCondition

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
```

## Explanation

- **Initialization**: Start by importing `Gatecraft` and `SemanticCondition` from the `gatecraft` library. Initialize the Gatecraft system:

  ```python
  from gatecraft import Gatecraft, SemanticCondition

  gc = Gatecraft()
  ```
- **Creating Users**: Create user instances for Alice and Bob:

  ```python
  alice = gc.create_user(user_id=1, name='Alice')
  bob = gc.create_user(user_id=2, name='Bob')
  ```
- **Defining Roles and Conditions**:

  - *Cat Lover Role*: Create a role for users who love cats and add a condition to allow access to content related to "cat":

    ```python
    cat_lover_role = gc.create_role(role_id=1, name='Cat Lover')
    cat_condition = SemanticCondition(term='cat', threshold=0.78)
    gc.add_condition_to_role(cat_lover_role, cat_condition)
    ```
  - *Everything Except Cats Role*: Create a role for users who should access all content except that related to "cat":

    ```python
    everything_except_cats_role = gc.create_role(role_id=2, name='Everything Except Cats')
    inverse_cat_condition = SemanticCondition(term='cat', threshold=0.78, inverse=True)
    gc.add_condition_to_role(everything_except_cats_role, inverse_cat_condition)
    ```
- **Assigning Roles to Users**: Assign the roles to the respective users:

  ```python
  gc.assign_role(alice, cat_lover_role)
  gc.assign_role(bob, everything_except_cats_role)
  ```
- **Adding Entities (Documents)**: Add content entities to the system:

  ```python
  gc.add_entity(entity_id=1, data='Cute kitten playing with a ball of yarn.')
  gc.add_entity(entity_id=2, data='Dog training and obedience tips.')
  ```
- **Access Control Check**: Determine if users have access to specific entities:

  ```python
  print(f"Alice access to Entity 1: {gc.is_access_allowed(alice, 1)}")  # True
  print(f"Alice access to Entity 2: {gc.is_access_allowed(alice, 2)}")  # False
  print(f"Bob access to Entity 1: {gc.is_access_allowed(bob, 1)}")      # False
  print(f"Bob access to Entity 2: {gc.is_access_allowed(bob, 2)}")      # True
  ```

## Additional Information

- **Semantic Conditions**: The `SemanticCondition` allows you to define access conditions based on semantic similarity to a term. Setting `inverse=True` reverses the condition.
- **Similarity Threshold**: Adjust the `threshold` parameter in `SemanticCondition` to change the sensitivity of the semantic matching.
- **Gatecraft Class**: The `Gatecraft` class encapsulates all the functionality, simplifying the process of creating users, roles, and entities, and checking access.
- **No Need to Manage Permissions Directly**: Permissions are handled internally, reducing complexity and making the library easier to use.

## Advanced Usage

For more advanced scenarios, you can:

- **Integrate with Different Vector Stores**: Provide a custom vector store to the `Gatecraft` class if you wish to use something other than Pinecone.

  ```python
  from gatecraft.db.mock_vector_store import MockVectorStore

  vector_store = MockVectorStore()
  gc = Gatecraft(vector_store=vector_store)
  ```
- **Set Custom Similarity Thresholds**: Adjust the overall similarity threshold when initializing `Gatecraft`:

  ```python
  gc = Gatecraft(similarity_threshold=0.90)
  ```

## Dependencies

Ensure that you have the required API keys set in your environment variables or `.env` file:

- `OPENAI_API_KEY`
- `PINECONE_API_KEY`
- `PINECONE_ENVIRONMENT`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/lorenzoabati/gatecraft).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to reach out if you have any questions or need further assistance with Gatecraft!
