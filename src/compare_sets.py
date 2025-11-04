class CompareSets:
    """
    Compute Jaccard similarity between two sets of hashed shingles.
    """

    @staticmethod
    def jaccard_similarity(set_a, set_b):
        if not set_a and not set_b:
            return 1.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        if union == 0:
            return 0.0
        return intersection / union
