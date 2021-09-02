# xpflow
Utilities to represent experiments with classes```

Installation:
```
pip install git+https://github.com/sileod/xpflow.git 
```

`xpflow` allows a concise formulation of experiments. Classes are more concise than dictionnaries, enforce indentation, and you can copy past variables assignment into them. You can specify the global hyperparameters into a base class, and make subclasses experiments to check the influence of some parameters, for instance the learning rate.
Lists of values are used to denote multiple values to try for a given parameter. All combinations will be generated in the form of EasyDict objects. You can use a list of list to represent values that should actually be lists.
```python
from xpflow import Xp

class base(Xp):
    a="A"
    b=[1,2]

class learning_rate(base):
    lr=[1e-3,2e-3]
    list_values=[[1,2]]
    
for args in learning_rate():
    print(args.a, args.b, args.lr, args.list_values)
```
will print the following output:
```
A 1 0.001 [1, 2]
A 1 0.002 [1, 2]
A 2 0.001 [1, 2]
A 2 0.002 [1, 2]
```
