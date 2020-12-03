import re

# Read in coords
todo_orig = set()
requirements = {}
with open("day7.in") as f:
  for line in f:
    match = re.match("Step ([A-Z]) must be finished before step ([A-Z]) can begin.", line.strip())
    step = match.group(2)
    todo_orig.add(step)
    req = match.group(1)
    todo_orig.add(req)
    if step not in requirements:
      requirements[step] = []
    requirements[step].append(req)

num_todo = len(todo_orig)

# Given the list of steps todo, those finished and the requirements
# returns a list of steps that can be completed because their
# requirements are fully met
def find_available(todo, finished, requirements):
  avail = []
  for step in todo:
    if step not in requirements:
      avail.append(step)
    else:
      reqs = requirements[step]
      cando = True
      for r in reqs:
        if r not in finished:
          cando = False
          break
      if cando:
        avail.append(step)
  return sorted(avail, reverse=True)

# Part 1

# Find the next step available (in order) until finished
todo = todo_orig.copy()
finished = set()
order = []
while len(finished) < num_todo:
  avail = find_available(todo, finished, requirements)
  step = avail[-1]
  todo.remove(step)
  finished.add(step)
  order.append(step)
order = "".join(order)

print("Part 1:", order)

# Part 2

num_workers = 5

def time_cost(step):
  return ord(step) - 4

class Worker:
  def __init__(self, ID):
    self.ID = ID
    self.free()
  def free(self):
    self.working = None
    self.remain = None
workers = [Worker(i) for i in range(num_workers)]

todo = todo_orig.copy()
finished = set()
t = -1
while len(finished) < num_todo:

  t += 1

  # Workers work.
  # If remain is 0, frees up the workers; else decrease remain
  for worker in workers:
    if worker.working is not None:
      if worker.remain > 0:
        worker.remain -= 1
      elif worker.remain == 0:
        finished.add(worker.working)
        worker.free()

  # Finds available work
  avail = find_available(todo, finished, requirements)

  # Assigns availanle work to free workers
  for worker in workers:
    if worker.working is None:
      if len(avail) > 0:
        step = avail.pop()
        worker.working = step
        worker.remain = time_cost(step) - 1
        todo.remove(step)

  # foo = ["%4i" % t]
  # for worker in workers:
  #   if worker.working is None:
  #     foo.append(".")
  #   else:
  #     foo.append(worker.working)
  # print(" ".join(foo))

print("Part 2:", t)
