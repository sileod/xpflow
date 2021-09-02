# xpflow

Did you ever perform experiments by nesting loops like this ? 
```python
args=edict({'a':'A'})

for b in [1,2]:
    for lr in [1e-3, 2e-3]:
        args.lr=lr
        args.b=b
        # perform_experiment_and_logging(args)
```
This involves repetition, low readability and it gets messy when you nest many loops.
It is possible to represent experiments with dictionaries where some values that are lists, but you would have to implement custom functions to take care of them.

`xpflow` does that under the hood. This allows a concise, readable, composable, and framework-agnostic formulation of experiments by using classes. You can specify the global hyperparameters into a base class, and make subclasses experiments to check the influence of some parameters, e.g. a learning rate. Lists of values are used to denote multiple values to try for a given parameter. All combinations will be generated in the form of EasyDict objects. You can use a list of lists to represent values that should actually be lists.

### Installation
```
pip install git+https://github.com/sileod/xpflow.git 
```


### Usage
Just make sure that your experiment classes inherits the Xp class. Instanciating the class will provide an iterable that will yield the possible combinations of the values.

```python
from xpflow import Xp

class base(Xp):
    a='A'
    b=[1,2]

class learning_rate(base):
    lr=[1e-3,2e-3]
    list_values=[[1,2]]
    
for args in learning_rate():
    # perform_experiment_and_logging(args)
    print(args.a, args.b, args.lr, args.list_values)
```
will print the following output:
```
A 1 0.001 [1, 2]
A 1 0.002 [1, 2]
A 2 0.001 [1, 2]
A 2 0.002 [1, 2]
```

Experiments can be performed sequentially : `itertools.chain(base(), learning_rate())` will sequentially perform `base` and `learning_rate`. 
