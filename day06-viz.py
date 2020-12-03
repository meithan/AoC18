from string import ascii_lowercase

# Read in coords
coords = []
with open("day6.in") as f:
  for line in f:
    tokens = line.strip().split(",")
    coords.append((int(tokens[0]), int(tokens[1])))

def man_dist(c1, c2):
  return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])

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

grid = [[] for i in range(Nx)]
for i in range(Nx):
  grid[i] = [0]*Ny

areas = [0]*len(coords)
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

winner = None
maxarea = None
for k in range(len(coords)):
  if k not in on_border:
    if maxarea is None or areas[k] > maxarea:
      maxarea = areas[k]
      winner = k
print(winner)
print("Part 1:", maxarea)

import matplotlib.pyplot as plt
import matplotlib.colors as mpl_colors
import numpy as np
import random
cmap = plt.cm.terrain
colors = list(cmap(np.linspace(0,1,len(coords))))
seed = random.randrange(1000)
# nice seeds: 221, 947
seed = 947
print("seed=", seed)
random.seed(seed)
random.shuffle(colors)
colors = ['black'] + colors
custom_cmap = mpl_colors.ListedColormap(colors)
norm = mpl_colors.BoundaryNorm(range(-1,len(coords)), custom_cmap.N)

plt.figure(figsize=(8,7.6))
# plt.gcf().set_facecolor("k")
grid1 = np.array(grid)
plt.imshow(np.transpose(grid1), cmap=custom_cmap, norm=norm, interpolation="none")
for c in coords:
  plt.scatter([c[0]], [c[1]], color="k", s=10, clip_on=False)
plt.xlim(0,Nx)
plt.ylim(0,Ny)
plt.axis('off')
plt.tight_layout()
plt.subplots_adjust(top=0.98, bottom=0.024, left=0.005, right=0.996, hspace=0.2, wspace=0.2)

#plt.savefig("day6_p1.png")
plt.show()

sys.exit()

# Part 2

dist_limit = 10000

grid = [[] for i in range(Nx)]
for i in range(Nx):
  grid[i] = [0]*Ny

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
