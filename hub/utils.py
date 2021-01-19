from math import gcd
import time
from collections import abc

from numpy.lib.arraysetops import isin

from hub.exceptions import ShapeLengthException
from hub import defaults


def _flatten(list_):
    """
    Helper function to flatten the list
    """
    return [item for sublist in list_ for item in sublist]


class EmptyLock(object):
    def __init__(self):
        return None

    def __enter__(self):
        return 1

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        return True


def gcp_creds_exist():
    """Checks if credentials exists"""

    try:
        import os

        env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if env is not None:
            return True
        from google.cloud import storage

        storage.Client()
    except Exception:
        return False
    return True


def s3_creds_exist():
    import boto3

    sts = boto3.client("sts")
    try:
        sts.get_caller_identity()
    except Exception:
        return False
    return True


def azure_creds_exist():
    """Checks if credentials exists"""

    import os

    env = os.getenv("ACCOUNT_KEY")
    if env is not None:
        return True
    return False


def hub_creds_exist():
    """Checks if credentials exists"""

    import os

    env = os.getenv("ACTIVELOOP_HUB_PASSWORD")
    if env is not None:
        return True
    return False


def pytorch_loaded():
    try:
        import torch

        torch.__version__
    except ImportError:
        return False
    return True


def ray_loaded():
    try:
        import ray

        ray.__version__
    except ImportError:
        return False
    return True


def dask_loaded():
    try:
        import dask

        dask.__version__
    except ImportError:
        return False
    return True


def tensorflow_loaded():
    try:
        import tensorflow

        tensorflow.__version__
    except ImportError:
        return False
    return True


def tfds_loaded():
    try:
        import tensorflow_datasets

        tensorflow_datasets.__version__
    except ImportError:
        return False
    return True


def transformers_loaded():
    try:
        import transformers

        transformers.__version__
    except ImportError:
        return False
    return True


def pathos_loaded():
    try:
        import pathos

        pathos.__version__
    except ImportError:
        return False
    return True


def compute_lcm(a):
    """
    Lowest Common Multiple of a list a
    """
    if not a:
        return None
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return int(lcm)


def batchify(iterable, n=1):
    """
    Batchify an iteratable
    """
    ls = len(iterable)
    batches = []
    for ndx in range(0, ls, n):
        batches.append(iterable[ndx : min(ndx + n, ls)])
    return batches


class Timer:
    def __init__(self, text):
        self._text = text

    def __enter__(self):
        self._start = time.time()

    def __exit__(self, *args):
        print(f"{self._text}: {time.time() - self._start}s")


def norm_shape(shape):
    shape = shape or (None,)
    if isinstance(shape, int):
        shape = (shape,)
    if not isinstance(shape, abc.Iterable):
        raise TypeError(
            f"shape is not None, int or Iterable, type(shape): {type(shape)}"
        )
    shape = tuple(shape)
    if not all([isinstance(s, int) or s is None for s in shape]):
        raise TypeError(f"Shape elements can be either int or None | shape: {shape}")
    return shape


def norm_cache(cache):
    cache = cache or 0
    if not isinstance(cache, int):
        raise TypeError("Cache should be None or int")
    return cache
