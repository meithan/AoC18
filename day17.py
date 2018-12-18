from copy import deepcopy
from queue import Queue
import sys
import re

class Grid:

  def __init__(self, xmin, xmax, ymin, ymax):
    # We add extra columns to the left and right
    self.xoff = xmin - 1
    self.NX = xmax - xmin + 3
    self.NY = ymax - ymin + 1
    self.xmin = xmin - 1
    self.xmax = xmax + 1
    self.ymin = 0
    self.ymax = self.NY - 1
    self.grid = []
    for j in range(self.NY):
      self.grid.append(['.']*self.NX)
    self.set(500, 0, '+')

  # Sets values of the grid
  # Both x and y can be tuples, in which case the relevant rnge is filled
  # tiwh the given value
  def set(self, x, y, value):
    if isinstance(x, tuple): x1 = x[0]; x2 = x[1]
    else: x1 = x; x2 = x
    if isinstance(y, tuple): y1 = y[0]; y2 = y[1]
    else: y1 = y; y2 = y
    for r in range(y1,y2+1):
      for c in range(x1,x2+1):
        self.grid[r][c-self.xoff] = value

  # Retrieves the value at (x,y)
  # This is needed because internal grid indices are x-shifted
  def at(self, x, y):
    return self.grid[y][x-self.xoff]

  # Tries to fill the row from (x0,y0)
  # This will move first left and then right from (x0,y0) until either
  # the square below is empty (in which case a source will be created)
  # or a wall is found.
  def fill_row(self, x0, y0):
    x = x0
    falls = []
    limits = []
    for dx in [-1, +1]:
      x = x0
      while True:
        if self.at(x, y0+1) not in ['#', '~']:
          falls.append((x,y0))
          limits.append(x)
          break
        else:
          if self.at(x+dx, y0) not in ['#', '~']:
            x += dx
          else:
            limits.append(x)
            break
    return tuple(limits), tuple(falls)

  # Makes water flow from the initial source
  def flow(self, source):

    # We enqueue new sources, and keep track of which have been added
    sources = Queue()
    sources.put(source)
    added_sources = set(source)

    # Iterate until no more sources remain
    while not sources.empty():

      # Pop next source
      x, y = sources.get()
      # grid.plot(y)
      print("Source at", x, y)

      # Propagate water from source
      while True:

        # Bottom has been reached
        if y == grid.ymax:
          break

        # If can flow down, flow down
        elif self.at(x, y+1) in ['.', '|']:
          y += 1
          self.set(x, y, '|')
          # print("fell to", x, y)

        # If can't flow down, try to fill the current row
        # If row is contained by walls, fill it and go back up
        # If it's not, create new source(s) and break
        elif grid.at(x, y+1) in ['~', '#']:
          limits, falls = self.fill_row(x, y)
          if len(falls) == 0:
            self.set(limits, y, '~')
            y -= 1
          else:
            self.set(limits, y, '|')
            for s in falls:
              if s not in s not in added_sources:
                sources.put(s)
                added_sources.add(s)
            break

  # Count "wet" squares (do not include "flowing" squares if still_only=True)
  # Note that we skip the first rows until a clay square is found
  def count_wet(self, still_only=False):
    valid = ['~'] if still_only else ['~', '|']
    count = None
    for r in range(self.NY):
      if count is None:
        if "#" not in self.grid[r]: continue
        else: count = 0
      for c in self.grid[r]:
        if c in valid:
          count += 1
    return count

  # Print the grid to the terminal
  def show(self):
    for r in range(self.NY):
      print("".join(self.grid[r]))

  # Plot the grid using matplotlib
  def plot(self, y):
    import matplotlib.pyplot as plt
    import numpy as np
    grid1 = deepcopy(self.grid)
    for i in range(len(grid1)):
      for j in range(len(grid1[i])):
        if grid1[i][j] == '#': grid1[i][j] = 0
        elif grid1[i][j] == '.': grid1[i][j] = 1
        elif grid1[i][j] == '~': grid1[i][j] = 2
        elif grid1[i][j] == '|': grid1[i][j] = 3
        elif grid1[i][j] == '+': grid1[i][j] = 4
    plt.figure(figsize=(12,8))
    plt.imshow(np.array(grid1))
    plt.ylim(y+100,y-100)
    plt.tight_layout()
    plt.show()

  # Plot the grid using PIL and save it to disk
  def hardcopy(self, fname):
    from PIL import Image
    expand = 5
    width = self.NX * expand
    height = self.NY * expand
    img = Image.new('RGB', (width, height))
    pix = img.load()
    for x in range(width):
      for y in range(height):
        i = int(y // expand)
        j = int(x // expand)
        value = self.grid[i][j]
        if value == '#': color = (66, 0, 86)
        elif value == '.': color = (58, 79, 143)
        elif value == '~': color = (38, 145, 142)
        elif value == '|': color = (98, 203, 86)
        elif value== '+': color = (251, 234, 0)
        pix[x,y] = color
    img.save(fname)

# =============================

# Practice regex
regex = re.compile("[xy]=([0-9]+), [xy]=([0-9]+)..([0-9]+)")

with open(sys.argv[1]) as f:

  # First pass to determine bounds
  ymin = 0
  ymax = None
  xmin = None
  xmax = None
  for line in f:
    values = [int(x) for x in regex.match(line).groups()]
    if line.startswith('x'):
      x = values[0]
      if xmin is None or x < xmin: xmin = x
      if xmax is None or x > xmax: xmax = x
    elif line.startswith('y'):
      y = values[0]
      if ymin is None or y < ymin: ymin = y
      if ymax is None or y > ymax: ymax = y

  # Init grid object
  grid = Grid(xmin, xmax, ymin, ymax)

  # Second pass to load grid values
  f.seek(0)
  for line in f:
    values = [int(x) for x in regex.match(line).groups()]
    if line.startswith('x'):
      x = values[0]
      grid.set(x, (values[1],values[2]), '#')
    elif line.startswith('y'):
      y = values[0]
      grid.set((values[1],values[2]), y, '#')

# =============================

# Parts 1 and 2

# Make water flow from initial source
source = (500,0)
grid.flow(source)

print("Part 1:", grid.count_wet())
print("Part 2:", grid.count_wet(still_only=True))

print("Saving image ...")
fname = "Day17.png"
grid.hardcopy(fname)
print("Saved", fname)
