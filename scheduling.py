#!/usr/bin/env python3

import itertools
from typing import NamedTuple


HOURS_PER_DAY = 7

class Task(NamedTuple):
    name: str
    time: float
    bursts: int

    def __str__(self):
        return f"{task.name}\t{task.time} hours ({task.bursts} bursts)"

    
def bursts(combination):
    yield from zip(*[ [(task, n) for n in range(task.bursts, 0, -1)]
      for task in combination ])

def combinations(tasks):
    for n in range(len(tasks), 0, -1):
        yield from itertools.combinations(tasks, n)

def solutions(tasks):
    for combination in combinations(tasks):
        for schedule in bursts(combination):
            total = sum(n * task.time / task.bursts for task, n in schedule)
            if total <= HOURS_PER_DAY:
                yield schedule

                
def main(tasks):
    schedule = next(solutions(tasks), None)
    if schedule:
        total = sum(n * task.time / task.bursts for task, n in schedule)
        for task, n in schedule:
            print(f"{task.name}\t{n}")
        print("-----------------------------")
        print(f"TOTAL: {total} ({HOURS_PER_DAY-total} left)")
        print()
    else:
        print("No solutions")
        print()

    
if __name__ == '__main__':
    import sys
    from pathlib import Path
    import time

    from faker import Faker

    if len(sys.argv) >3:
        print()
        print(f"Usage {Path(__file__).name} [seed]")
        print()
        print()
        sys.exit(1)
    elif len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            seed = hash(sys.argv[1])
    else:
        seed = time.time_ns()

    fake = Faker(['es_ES', 'en_US', 'ja_JP'])
    print(f"seed= {seed}", file= sys.stderr)
    Faker.seed(seed)

    tasks = []
    n = fake.random_int(min=2, max= 4)
    for _ in range(0, n):
        tasks.append(Task(name= fake.text(max_nb_chars= 20),
                          time= fake.random_int(min=1, max= HOURS_PER_DAY),
                          bursts= fake.random_int(min=1, max= 5)))

    print(f"{n} tasks")
    for task in tasks:
        print(f"{task.name}\t\t{task.time} ({task.bursts})")
    print()
    
    main(tasks)
