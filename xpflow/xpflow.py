import copy
from tqdm.auto import tqdm
import numpy as np
import itertools
import time
import random
from easydict import EasyDict as edict

class Xp:
    def __init__(self):
        self._ts = time.time()
        self._leaves = {
            k: v for (k, v) in self.__class__.__dict__.items() if not k.startswith("_")
        }
        self._lists = {k for k in dir(self) if type(getattr(self, k)) == list}

    def _process_xp(self):
        xp = {
            k: getattr(self, k)
            for k in dir(self)
            if not k.startswith("_") and not callable(getattr(self, k))
        }
        for (k, v) in xp.items():
            assert type(v) != tuple
            if type(v) != list:
                xp[k] = [v]
        return xp

    def values(self):
        xp = self._process_xp()
        return list(itertools.product(*[xp[a] for a in xp if a != "tags"]))

    def keys(self):
        return self._process_xp().keys()

    def __iter__(self):
        keys = self.keys()
        values_list = self.values()
        for values in tqdm(values_list):

            args = edict({})
            for a, v in zip(keys, values):
                args[a] = v
            args._tsi = time.time()
            args._tags = tags

            selfi = copy.deepcopy(self)
            for k, v in args.items():
                setattr(selfi, k, v)
            yield selfi

    def __str__(self):
        return str(self.__dict__)

    def edict(self):
        return {
            k: getattr(self, k)
            for k in self.__dict__
            if not callable(getattr(self, k)) and not k.startswith("_")
        }
