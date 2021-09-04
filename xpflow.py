import copy
import itertools
from easydict import EasyDict as edict


class Xp:
    def __init__(self):
        self.xp_name = type(self).__name__

    def _process_xp(self):
        xp = {
            k: getattr(self, k)
            for k in dir(self)
            if not k.startswith("_") and not callable(getattr(self, k))
        }
        for (k, v) in xp.items():
            if type(v) != list:
                xp[k] = [v]
        return xp

    def _values(self):
        xp = self._process_xp()
        return list(itertools.product(*[xp[a] for a in xp]))

    def keys(self):
        return self._process_xp().keys()
    
    def edict(self):
        return edict(
            {
                k: getattr(self, k)
                for k in self.__dict__
                if not callable(getattr(self, k)) and not k.startswith("_")
            }
        )

    def __iter__(self):
        keys = self.keys()
        values_list = self._values()
        for values in values_list:

            args = edict({})
            for a, v in zip(keys, values):
                args[a] = v

            selfi = copy.deepcopy(self)
            for k, v in args.items():
                setattr(selfi, k, v)
            yield selfi.edict()

    def __str__(self):
        return str(self.__dict__)
    
    def __len__(self):
        return len([x for x in self])
    
