# xpflow

Did you ever perform experiments by nesting loops like this ? 
```python
args = edict({'a':'A'})

for b in [1,2]:
    for lr in [1e-3, 2e-3]:
        args.lr = lr
        args.b = b
        # perform_experiment_and_logging(args)
```

This get messy when there are many loops. In addition, nested loops are not objects, so you cannot store them or share them. A better alternative is to represent experiments with dictionaries where some values are lists, e.g.: 
```python 
learning_rate = {
    'a' : 'A',
    'b' : [1, 2],
    'lr' : [1e-3, 2e-3]
}
```
but you would have to write custom code to take care of the list values.

`xpflow` does that under the hood and use classes instead of dictionaries. This allows a concise, readable, composable, and framework-agnostic formulation of experiments. You can specify the global hyperparameters into a base class, and make subclasses experiments to check the influence of some parameters, e.g. a learning rate. Lists of values are used to denote multiple values to try for a given parameter. All combinations will be generated in the form of EasyDict objects.
With xpflow, you can also store and share your experiments for better reproducibility.

```python
from xpflow import Xp

class learning_rate(Xp):
    a = 'A'
    b = [1, 2]
    lr = [1e-3, 2e-3]
    
for args in learning_rate():
    # perform_experiment_and_logging(args)
```

## Installation
```
pip install xpflow
```
or the last version with
```
pip install git+https://github.com/sileod/xpflow.git 
```

## Usage
Just make sure that your experiment classes inherits the Xp class. Instanciating the class will provide an iterable yielding the possible value combinations.
Lists of values will be used to generate the possible combinations. You can use a list of lists to represent values that should actually be lists.

```python
from xpflow import Xp

class base(Xp):
    a='A'
    b=[1,2]

class learning_rate(base):
    lr = [1e-3, 2e-3]
    list_values = [[5, 6]]
    
for args in learning_rate():
    # perform_experiment_and_logging(args)
    print(args.a, args.b, args.lr, args.list_values)
```
will print the following output:
```
A 1 0.001 [5, 6]
A 1 0.002 [5, 6]
A 2 0.001 [5, 6]
A 2 0.002 [5, 6]
```

##  Other specific use cases:

#### Distributing computations across processes
You can easily distribute the computations across processes by passing argparse arguments to your main script.

```python
for i, args in enumerate(xp()):
    if i%argparse_args.number_of_processes != argparse_args.process_index:
        continue
    # perform_experiment_and_logging(args)
```

#### Sequential experiments
`itertools.chain(xp1(), xp2())` will return the parameters for `xp1` then `xp2`. 

#### Random search

You can perform a random search by using lengthy lists of possible values and then randomly discarding parameter combinations.

```python
class random_search_space(Xp):
    learning_rate=list(np.logspace(-6,-1,100))
    batch_size=[32,64,128,256]*10
    nb_epochs=[3,4,5]*10

for args in random_search_space():
    if random.random()>1/100: 
        continue # skip 99% of the possible combinations
    # perform_experiment_and_logging(args)
```
