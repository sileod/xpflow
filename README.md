# xpflow

Did you ever perform experiments by nesting loops ? Like this ?
```python
args=edict({a:'A'}}

for b in [1,2]:
    for lr in [1e-3, 2e-3]:
        args.lr=lr
        args.b=b
        # do stuff(args)
```
Using dictionaries is an alternative, but you would have to implement custom functions to take care of the loops.

`xpflow` allows a concise and readable, and framework-agnostic formulation of experiments by using classes. You can specify the global hyperparameters into a base class, and make subclasses experiments to check the influence of some parameters, e.g. a learning rate. Lists of values are used to denote multiple values to try for a given parameter. All combinations will be generated in the form of EasyDict objects. You can use a list of list to represent values that should actually be lists.

### Usage


```python
from xpflow import Xp

class base(Xp):
    a='A'
    b=[1,2]

class learning_rate(base):
    lr=[1e-3,2e-3]
    list_values=[[1,2]]
    
for args in learning_rate():
    # do_stuff(args)
    print(args.a, args.b, args.lr, args.list_values)
```
will print the following output:
```
A 1 0.001 [1, 2]
A 1 0.002 [1, 2]
A 2 0.001 [1, 2]
A 2 0.002 [1, 2]
```


### Installation
Installation:
```
pip install git+https://github.com/sileod/xpflow.git 
```

