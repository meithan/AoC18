from string import ascii_lowercase

# Read in coords
coords = []
with open("day6.in") as f:
  for line in f:
    tokens = line.strip().split(",")
    coords.append((int(tokens[0]), int(tokens[1])))

# Manhattan distance between two (x,y) pairs
def man_dist(c1, c2):
  return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])

# Translate origin of coordinates to left-most, bottom-most coord
# This is just done for easier indexing, and to have the search
# space tightly bound around the coords
xmin = min([c[0] for c in coords])
ymin = min([c[1] for c in coords])
xmax = max([c[0] for c in coords])
ymax = max([c[1] for c in coords])
coords = [(c[0]-xmin, c[1]-ymin) for c in coords]
xs = [c[0] for c in coords]
ys = [c[1] for c in coords]
Nx = max(xs)
Ny = max(ys)

# Part 1

# Initialize grid
grid = []
for i in range(Nx):
  grid.append([0]*Ny)

# List for counting total area for each coord
areas = [0]*len(coords)

# Go over every grid location and compute distances to all coords
# Set grid value to closest coord, or if multiple coords tie, to -1
for i in range(Nx):
  for j in range(Ny):
    closest = []
    mindist = None
    for l,c in enumerate(coords):
      dist = man_dist(c, (i,j))
      if mindist is None or dist < mindist:
        mindist = dist
        closest = [l]
      elif dist == mindist:
        closest.append(l)
    if len(closest) == 1:
      grid[i][j] = closest[0]
      areas[closest[0]] += 1
    else:
      grid[i][j] = -1
    # input()

# Go over the grid's borders and determine which coords
# have grid points along board
on_border = set()
i = 0
for j in range(Ny):
  on_border.add(grid[i][j])
i = Nx-1
for j in range(Ny):
  on_border.add(grid[i][j])
j = 0
for i in range(Nx):
  on_border.add(grid[i][j])
j = Ny-1
for i in range(Nx):
  on_border.add(grid[i][j])

# The winning coord is the one with the greatest area
# that is not on the border
winner = None
maxarea = None
for k in range(len(coords)):
  if k not in on_border:
    if maxarea is None or areas[k] > maxarea:
      maxarea = areas[k]
      winner = k
#print(winner)
print("Part 1:", maxarea)

# Part 2

dist_limit = 10000

# Initialize new grid
grid = []
for i in range(Nx):
  grid.append([0]*Ny)

# For each grid point, compute the sum of distances to all coords, 
# and count it if the total dist is less than the distance limit
size = 0
areas = [0]*len(coords)
for i in range(Nx):
  for j in range(Ny):
    for l,c in enumerate(coords):
      dist = man_dist(c, (i,j))
      grid[i][j] += dist
    if grid[i][j] < dist_limit:
      size += 1

print("Part 2:", size)
