def jaccard_similarity(i: set, j: set):
    """
    Calculate Jaccard similarity.

    .. math:: Sim(i, j) = \\frac{|i \\cap j|}{|i \\cup j|}

    :param i: a set of nodes
    :param j: a set of nodes
    :return: jaccard similarity of two set of nodes.
    """
    return len(i & j) / len(i | j)
