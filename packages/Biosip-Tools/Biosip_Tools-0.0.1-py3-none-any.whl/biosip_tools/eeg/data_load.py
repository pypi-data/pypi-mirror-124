import numpy as np

def load_time_series(path: str) -> np.array: 
    """[summary]

    :param path: [description]
    :type path: str
    :return: [description]
    :rtype: np.array
    """
    return np.load(path)


