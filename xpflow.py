import copy
import itertools
from easydict import EasyDict
import hashlib
import json
from sorcery import dict_of
import os, sys, traceback

def override(xp):
    import argparse, sys
    parser = argparse.ArgumentParser()
    _, unknown = parser.parse_known_args(sys.argv[1:])
    cmd_args_dict = dict(zip(unknown[:-1:2],unknown[1::2]))
    cmd_args_dict = {k.lstrip('-'): v for (k,v) in cmd_args_dict.items()}
    print(f"cmd_args: {cmd_args_dict}")
    for k,v in cmd_args_dict.items():
        if k in xp:
            xp[k]=type(xp[k])(v)
    return xp

class edict(EasyDict):
    def __hash__(self):
        json_dump = json.dumps(self, sort_keys=True, ensure_ascii=True)
        digest = hashlib.md5(json_dump.encode('utf-8')).hexdigest()
        identifier = int(digest, 16)
        return identifier

class Xpl():
    def __init__(self,a,b):
        self.a=a
        self.b=b
    def __iter__(self):
        for x in [self.a, self.b]:
            for y in x:
                yield y
class Xp:
    def __init__(self, dictionary=None):
        self.xp_name = type(self).__name__
        if dictionary:
            for (k,v) in dictionary.items():
                setattr(self, k, v)
        self.xp_name = type(self).__name__
        
    def __add__(self, other):
        return Xpl(self, other)
    
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
            xp = selfi.edict()
            xp = override(xp)
            xp._hash = hash(xp)
            yield xp
    
    def first(self):
        for xp in self:
            return xp

    def __str__(self):
        return str(self.__dict__)
    
    def __len__(self):
        return len([x for x in self])
    

class NoPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class Catch:
    def __init__(self, exceptions=[], exit_fn=lambda:None):
        self.allowed_exceptions = exceptions
        self.encountered_expcetions=[]
        self.exit_fn=exit_fn
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, tb):
        self.exit_fn()
        if exception_type==KeyboardInterrupt:
            return False
        global _EXCEPTIONS
        try:
            _EXCEPTIONS
        except:
            _EXCEPTIONS=[]
        
        if  exception_type and (exception_type in self.allowed_exceptions or not self.allowed_exceptions):
            print(f"{exception_type.__name__} swallowed!",exception_value,traceback.print_tb(tb))
            _EXCEPTIONS+=[dict_of(exception_type,exception_value,tb)]
            return True
