# About

Implementation of a profit maximizer as part of a programming assignment.

# Set-up

1. Install the module and run tests:

```sh
$ cd profit_maximizer
$ pip install .
$ python -m unittest discover "./tests" -v
```

2. Try out the assignment input:

```sh
$ import profit_maximizer
$ solver = profit_maximizer.CaseHandler("./tests/inputs/input.txt") 
$ solver.content_handler()
```

The code above should print:

```
Case 1: 44
Case 2: 11
Case 3: 12
Case 4: 10
Case 5: 39
```

# Post-Mortem

The goal was to spend at most half a day on the topic. The assignment felt very similar to the dynamic programming job scheduler problem, albeit with a seemingly added layer of complexity due to the ability of each machine to vary in profit/length of profit accretion.

The present implementation solves the assignment example input but fails in runtime when trying more complex examples (see ``tests_runtime.py``).

One interesting tidbit of the case was finding that the context of each case (the first row containing three integers N, C, and D) can be represented in a similar way to a machine state (a machine is characterized by four integers characterizing it: D, P, R, and G), i.e.:

> At day D=0, the company, ACM, acquires a machine for price P=0, resell price R=10, daily profit G=0.

Time Spent on assignment:
| **Tasks** | **Time** |
| --- | --- | 
| Reading instructions + preliminary whiteboard |  1h00 |
| Setting project's structure | 0h30 |
| Building the CaseHandler object for file handling | 2h00 |
| Whiteboard | 1h00 |
| Building the RecursiveProfitSolver object | 2h00 |
| Building the tests | 1h00 |
| Whiteboard | 0h30 |
| Building the (iterative) ProfitSolver Object | 2h00 |
| Refactoring, comments, markdown | 2h30 |
| ***Total*** | ***12h30*** | 

# Instructions

Instructions are displayed in the ``./docs`` folder.
