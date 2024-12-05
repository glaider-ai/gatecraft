from NeverMind.utils.conditions import Condition


class SemanticCondition(Condition):
    """
    Condition that evaluates based on semantic similarity.
    """

    def __init__(self, term, threshold=0.8, inverse=False):
        self.term = term
        self.threshold = threshold
        self.inverse = inverse
        self.term_embedding_id = f"term_{self.term}"

    def evaluate(self, user, entity, database):
        # Ensure the term embedding is stored
        if not hasattr(self, 'term_embedding'):
            self.term_embedding = database.get_embedding(self.term)
            database.store_embedding(self.term_embedding_id, self.term_embedding)

        # Generate embedding for the entity data
        entity_embedding = database.get_embedding(entity.data)

        # Compute similarity directly
        similarity = database.compute_similarity(self.term_embedding, entity_embedding)

        # Print the similarity for debugging
        print(f"Similarity between '{self.term}' and '{entity.data}': {similarity}")

        # Check if the similarity meets the threshold
        if self.inverse:
            return similarity < self.threshold
        else:
            return similarity >= self.threshold
    