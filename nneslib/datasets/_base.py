from os.path import dirname

import networkx as nx


def load_twitch(region: str) -> nx.Graph:
    """
    Load and return the Twitch Social Network.
    The details about this datasets please refer to https://github.com/benedekrozemberczki/datasets

    :param region: one of ["DE", "EN", "ES", "FR", "PT", "RU", "TW"]
    :return: `nx.Graph`. an networkx graph object
    :raise: :class:`ValueError` if the region is invalid

    .. rubric:: Example

    >>> from nneslib.datasets import load_twitch
    >>> import networkx as nx
    >>> G = load_twitch("DE")
    """
    module_path = dirname(__file__)
    raise NotImplementedError()