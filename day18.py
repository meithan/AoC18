from copy import deepcopy
import sys

# Returns neighbors of cell (i,j), excluding those outside bounds
def neighbors(i, j):
  neighs = []
  for dx in [-1, 0, 1]:
    for dy in [-1, 0, 1]:
      ni = i+dx
      nj = j+dy
      if not (ni == i and nj == j) and 0 <= ni <= NX - 1 and 0 <= nj <= NY - 1:
        neighs.append((i+dx, j+dy))
  return neighs

# One iteration of the grid
def evolve(grid):
  new_grid = []
  for i in range(NX):
    new_grid.append(['?']*NY)
  for i in range(NX):
    for j in range(NY):
      square = grid[i][j]
      neighs = [grid[n[0]][n[1]] for n in neighbors(i,j)]
      trees = neighs.count('|')
      lumbs = neighs.count('#')
      if square == '.':
        if trees >= 3:
          new_grid[i][j] = '|'
        else:
          new_grid[i][j] = '.'
      elif square == '|':
        if lumbs >= 3:
          new_grid[i][j] = '#'
        else:
          new_grid[i][j] = '|'
      else:
        if lumbs >= 1 and trees >= 1:
          new_grid[i][j] = '#'
        else:
          new_grid[i][j] = '.'
  return new_grid

# Count number of wooded cells and lumberyards
def count():
  wooded = 0
  lumberyards = 0
  for i in range(NX):
    for j in range(NY):
      if grid[i][j] == '|':
        wooded += 1
      elif grid[i][j] == '#':
        lumberyards += 1
  return wooded, lumberyards

# =====================

# Read grid
grid = []
with open(sys.argv[1]) as f:
  for line in f:
    grid.append(list(line.strip()))

NX = len(grid)
NY = len(grid[0])

# Iterate 1000 minutes
values = []
for minute in range(1,1000+1):

  grid = evolve(grid)

  wooded, lumberyards = count()

  # Count after part 1
  if minute == 10:
    part1_ans = wooded * lumberyards

  values.append((minute, wooded, lumberyards, wooded*lumberyards))
  print(minute, wooded, lumberyards, wooded*lumberyards)

print("Part 1:", part1_ans)

# Plot variables
minutes = [x[0] for x in values]
wooded = [x[1] for x in values]
lumberyards = [x[2] for x in values]
prods = [x[3] for x in values]

import matplotlib.pyplot as plt
plt.plot(wooded)
plt.plot(lumberyards)
ax2 = plt.gca().twinx()
ax2.plot(prods, color="C2")
plt.show()

# The presence of a cycle was discovered by inspection of the plot
# and its length by inspection of the printed values
cycle = 28

# Print answer based on cycle length found
mins_mod = [x % cycle for x in minutes[-cycle:]]
prods_mod = prods[-cycle:]
target = 1000000000 % cycle
for i in range(cycle):
  if mins_mod[i] == target:
    print("Part 2:", prods_mod[i])
    break
