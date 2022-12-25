# xpflow: nested loops as classes

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
However, you have to write custom code to take care of the list values.

`xpflow` does that under the hood. Lists of values are used to denote multiple values to try for a given parameter. All combinations will be generated in the form of EasyDict objects. Nested loops become objects (classes).

```python
from xpflow import Xp

for args in Xp(learning_rate):
    # perform_experiment_and_logging(args)
```
This allows a concise, readable, shareable, composable, and framework-agnostic formulation of experiments. You can also use classes instead of dictionaries. Classes are a bit less verbose (no commas, no quote on parameter names), they enforce tabulation, they are easier to read, extensible, and inheritence is cleaner.

```python

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

#### Sequential experiments
```python
for args in xp1() + xp2()
    # perform_experiment_and_logging(args)

```

#### Distributing computations across processes
You can easily distribute the computations across processes by passing argparse arguments to your main script. 
The argument yielded by `xpflow` are *deterministically* hashable into integers (standard dict/edict are not hashable).

```python
for args in xp():
    if hash(args) % argparse_args.number_of_processes != argparse_args.process_index:
        continue
    # perform_experiment_and_logging(args)
```



#### Random search

You can perform a random search by using lengthy lists of possible values and then randomly discarding parameter combinations.

```python
class random_search_space(Xp):
    learning_rate=list(np.logspace(-6,-1,100))
    batch_size=[32,64,128,256]
    nb_epochs=[3,4,5]

for args in sorted(random_search_space(), key=hash)[:100]:
    # perform_experiment_and_logging(args)
```
