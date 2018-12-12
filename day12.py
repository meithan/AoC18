import sys

# We set paddings so that the problem does not round out of bounds
# These must be found by trial and error
lpad = 1
rpad = 170

# Load initial state and rules from input
rules = {}
with open(sys.argv[1]) as f:
  init_state = "."*lpad + f.readline().strip().split(":")[1].strip() + "."*rpad
  f.readline()
  for line in f:
    pattern, result = line.strip().split(" => ")
    rules[pattern] = result

# Advances the given state by one generation
# Careful not to run out of bounds!
def do_generation(state):
  new_state = ""
  for i in range(len(state)):
    # For the first two and last two pots we pad with empty spots ('.')
    if i == 0:
      pattern = ".." + state[0:3]
    elif i == 1:
      pattern = "." + state[0:4]
    elif i == len(state) - 2:
      pattern = state[-4:] + "."
    elif i == len(state) - 1:
      pattern = state[-3:] + ".."
    else:
      pattern = state[i-2:i+3]
    if pattern in rules:
      new_state += rules[pattern]
    else:
      new_state += "."
  return new_state

# Computes the score of a state
# This needs to know the lpad value (to know which element is #0)
def get_score(state, lpad):
  score = 0
  for i in range(len(state)):
    if state[i] == "#":
      score += i-lpad
  return score

# =================================

state = init_state
print(state)

# Do generations until the state, stripped of left- and right-trailing
# empty spots ('.') stops changing
# We keep track of a few quantities to help identify it
last_state = init_state
last_score = get_score(init_state, lpad)
gen = 1
while True:

  state = do_generation(state)
  score = get_score(state, lpad)
  strip_state = state.strip(".")
  print(state, gen, score, score-last_score)

  # After 20 generations we save the current score for Part 1
  if gen == 20:
    part1_ans = score

  # Once the stable state is found, we break out of loop, and computing
  # the answer to Part 2 is simple arithmetic: for each generation left
  # to go to reach 50 billions, the score will increase by the number
  # of pots with plants ('#'), since each plant will move 1 space per
  # generation (hence its value will increase by 1)
  if strip_state == last_state.strip("."):
    stable_gen = gen-1
    stable_state = last_state
    stable_score = last_score
    stable_inc = state.count("#")
    break

  last_score = score
  last_state = state
  gen += 1

print("Part 1:", part1_ans)
print("Part 2:", stable_score + (50000000000-stable_gen)*stable_inc)
