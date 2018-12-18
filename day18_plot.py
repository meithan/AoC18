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

from PIL import Image

NX = 50
NY = 50

expand = 10
width = NX * expand
height = NY * expand


# Read grid
grid = []
with open(sys.argv[1]) as f:
  for line in f:
    grid.append(list(line.strip()))


for minute in range(1,1000+1):

  grid = evolve(grid)

  #wooded, lumberyards = count()

  img = Image.new('RGB', (width, height))
  pix = img.load()
  for x in range(width):
    for y in range(height):
      i = int(y // expand)
      j = int(x // expand)
      value = grid[i][j]
      if value == '#': color = (106, 19, 12)
      elif value == '|': color = (52, 78, 10)
      elif value == '.': color = (198, 169, 125)
      pix[x,y] = color
  fname = "frames/frame%03i.png" % minute
  img.save(fname)
  print(fname)
