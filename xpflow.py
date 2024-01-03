import copy
import itertools
from easydict import EasyDict
import hashlib
import json
from sorcery import dict_of
import os, sys, traceback, psutil
import functools
import tqdm
import logging

def without(d, key):
    if key not in d:
        return d
    new_d = d.copy()
    new_d.pop(key)
    return new_d

def is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

def override(xp):
    import argparse, sys
    parser = argparse.ArgumentParser()
    _, unknown = parser.parse_known_args(sys.argv[1:])
    cmd_args_dict = dict(zip(unknown[:-1:2],unknown[1::2]))
    cmd_args_dict = {k.lstrip('-'): v for (k,v) in cmd_args_dict.items()}
    for k,v in cmd_args_dict.items():
        if k in xp:
            xp[k]=type(xp[k])(v)
    return xp

class edict(EasyDict):

    def __hash__(self):
        try:
            json_dump = json.dumps(self, sort_keys=True, ensure_ascii=True)
            digest = hashlib.md5(json_dump.encode('utf-8')).hexdigest()
            identifier = int(digest, 16)
            return identifier
        except:
            return 0
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
        history=[]
        for i, values in enumerate(values_list):

            args = edict({})
            for a, v in zip(keys, values):
                args[a] = v

            selfi = copy.deepcopy(self)
            for k, v in args.items():
                setattr(selfi, k, v)
            xp = selfi.edict()
            xp = override(xp)
            xp._hash = hash(xp)
            history+=[xp]
            if i==len(values_list)-1:
                xp._history=history
            yield xp
    
    def first(self):
        for xp in self:
            return xp

    def __str__(self):
        return str(self.__dict__)
    
    def __len__(self):
        return len([x for x in self])
    

# Context managers:

class NoPrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class NoTqdm:
    def __enter__(self):
        tqdm.__init__ = functools.partialmethod(tqdm.__init__, disable=True)    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        tqdm.__init__ = functools.partialmethod(tqdm.__init__, disable=False)        


class NoLogging:
    def __enter__(self):
        self._old_logging_level = logging.root.manager.disable
        logging.disable(logging.CRITICAL)
    
    def __exit__(self, exc_type, exc_value, traceback):
        logging.disable(self._old_logging_level)        
        
class Catch:
    def __init__(self, exceptions=[], exit_fn=lambda:None,info=''):
        self.allowed_exceptions = exceptions
        self.exit_fn=exit_fn
        self.info=info
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
            print(f"{exception_type.__name__} swallowed!",str(self.info),exception_value,traceback.print_tb(tb))
            _EXCEPTIONS+=[dict_of(exception_type,exception_value,tb,info=self.info)]
            return True


class Notifier:
    def __init__(self, exit_fn=lambda x:None):
        self.exit_fn=exit_fn
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.exit_fn(str(args))

class MeasureRAM:
    def __init__(self, id=None, logger=print):
        self.id = id
        self.logger = logger
        if self.logger==print:
            self.logger=type('logger', (object,), {'log':print})()

    def __enter__(self):
        self.mem_before = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

    def __exit__(self, exc_type, exc_val, exc_tb):
        mem_after = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        variation_mb = (mem_after - self.mem_before)
        if self.logger:
            self.logger.log(dict_of(self.id,variation_mb))

class DisableOutput:
    def __init__(self):
        self.devnull = None

    def __enter__(self):
        # Disable all output streams
        self.devnull = open(os.devnull, "w")
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.devnull
        sys.stderr = self.devnull
        logging.disable(logging.CRITICAL)  # Disable all logging output
        return self

    def __exit__(self, *args):
        # Re-enable the output streams
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()
        logging.disable(logging.NOTSET)  # Re-enable logging output

    def write(self, *args, **kwargs):
        pass
