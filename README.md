What is measurer?
=================

Measurer is easy to use python package for examining and comparing callable objects.

Installing
----------

This package distributes by Python Packaging Index, aka PyPI, so you can install measurer using pip:

`py -m pip install function_measurer`

Quick start
-----------

Let's examine using of this package on a little example:

```python
from measurer import SetTesting

@SetTesting(2, 2)
def summ(a: int, b: int): 
    return a + b
```

We have function and we want to test it. We use decorator `SetTesting` for it. Arguments given to `SetTesting` passes to `summ`.

Let's save this file with name `sample.py`. After that we open powerShell or cmd and enter this command into the shell:

`py -m measurer sample.py 3 memory`

And we get this:

```
--------------------------------------------------------
| Tests.|Functions.|Iteration 1|Iteration 2|Iteration 3|
--------------------------------------------------------
|runtime|      summ|        0.0|        0.0|        0.0|
--------------------------------------------------------
```

First column is tests those we have given to our package. In this case we have given only one test. That is runtime. When we give runtime test tester runs testing functions and prints their runtimes. The next column shows functions we have tested. Other columns show the results of the testing.

Detailed description of using.
------------------------------

The first argument in our example is the path to a file that you want to test. The second is the amount of times the functions will be tested. The third argument is test that we want to do with our functions. We can also pass more than one test to this argument and will get a table with results of those tests.

| Test    | Description                       |
| ------- | --------------------------------- |
| runtime | Measures the runtime of function. |
| memory  | Measures the occupied memory.     |

If you're too bored of repeating th same cli arguments you can just write them into file and pass the path to that file to measurer after `@` symbol.

If you did not understand something try to use `-h` option. If you found some mistakes in this docs, please make a pull request with correcting of found mistake.
