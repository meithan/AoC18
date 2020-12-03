import re
import sys

class Nanobot:
  def __init__(self, pos, radius):
    self.xc = pos[0]
    self.yc = pos[1]
    self.zc = pos[2]
    self.pos = pos
    self.radius = radius
  def __repr__(self):
    return "[<%i,%i,%i> r=%i]" % (*self.pos, self.radius)

class SearchCube:

  def __init__(self, corner, side):
    self.corner = corner
    self.side = side
    self.x0 = corner[0]
    self.y0 = corner[1]
    self.z0 = corner[2]
    self.x1 = self.x0 + self.side - 1
    self.y1 = self.y0 + self.side - 1
    self.z1 = self.z0 + self.side - 1
    self.op_corner = (self.x1, self.y1, self.z1)
    self.center = ((self.x0+self.x1)//2, (self.y0+self.y1)//2, (self.z0+self.z1)//2)
    self.verts = [(self.x0, self.y0, self.z0), (self.x1, self.y0, self.z0), (self.x0, self.y1, self.z0), (self.x1, self.y1, self.z0), (self.x0, self.y0, self.z1), (self.x1, self.y0, self.z1), (self.x0, self.y1, self.z1), (self.x1, self.y1, self.z1)]

  def draw(self, ax, **kwargs):
    for vs in [[0, 1, 3, 2, 0], [4, 5, 7, 6, 4], [1, 5], [0, 4], [3, 7], [2, 6]]:
      xs = [self.verts[i][0] for i in vs]
      ys = [self.verts[i][1] for i in vs]
      zs = [self.verts[i][2] for i in vs]
      ax.plot(xs, ys, zs, **kwargs)

  def get_children(self):
    assert self.side % 2 == 0
    new_side = self.side // 2
    new_corners = [(self.x0, self.y0, self.z0), (self.x0+new_side, self.y0, self.z0), (self.x0, self.y0+new_side, self.z0), (self.x0+new_side, self.y0+new_side, self.z0), (self.x0, self.y0, self.z0+new_side), (self.x0+new_side, self.y0, self.z0+new_side), (self.x0, self.y0+new_side, self.z0+new_side), (self.x0+new_side, self.y0+new_side, self.z0+new_side)]
    children = []
    for corner in new_corners:
      children.append(SearchCube(corner, new_side))
    return children

  def best_child(self, bots):
    best_num = -1
    best_child = []
    for child in self.get_children():
      num = len(child.bots_in_range(bots))
      if num > best_num:
        best_num = num
        best_child = [child]
      elif num == best_num:
        best_child.append(child)
    return best_child

  # Determines whether the given bot is in range of (any part of) the cube
  # Based on the algorithm by Jim Arvo from "Graphics Gems"
  def is_in_range(self, bot):
    dmin = 0
    for i in range(3):
      if bot.pos[i] < self.corner[i]:
        dmin += (self.corner[i] - bot.pos[i])**2
      elif bot.pos[i] > self.op_corner[i]:
        dmin += (bot.pos[i] - self.op_corner[i])**2
    return dmin <= bot.radius**2

  # Returns the list of bots in range of the cube
  def bots_in_range(self, bots):
    bots1 = []
    for bot in bots:
      if self.is_in_range(bot):
        bots1.append(bot)
    return bots1

  def __str__(self):
    return "<Cube corner=(%i,%i,%i), side=%i>" % (self.x0, self.y0, self.y0, self.side)

# Manhattan distance between two points
def man_dist(p1, p2):
  return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])

# =========================================================

# Read bots from input
bots = []
with open(sys.argv[1]) as f:
  for line in f:
    groups = re.match("pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=(-?[0-9]+)", line).groups()
    bot = Nanobot([int(x) for x in groups[:3]], int(groups[3]))
    bots.append(bot)

# Part 1

# Determine strongest
strongest = None
max_range = float("-inf")
for bot in bots:
  if bot.radius > max_range:
    strongest = bot
    max_range = bot.radius

in_range = 0
for bot in bots:
  dist = man_dist(bot.pos, strongest.pos)
  if dist <= strongest.radius:
    in_range += 1

print("Part 1:", in_range)

# Part 2

xcs = [b.xc for b in bots]
ycs = [b.yc for b in bots]
zcs = [b.zc for b in bots]

# Search cube containing all bots and with a side a power of 2
a = 2**28
cube0 = SearchCube((-a,-a,-a), 2*a)
to_search = [cube0]

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xcs, ycs, zcs)
cube0.draw(ax, color="r")

# for i in range(20):
#   print(i, len(to_search[0].bots_in_range(bots)), len(to_search))
#   next_to_search = []
#   for cube in to_search:
#     # cube.draw(ax, color="C%i" % (i%5))
#     children = cube.best_child(bots)
#     print(len(children))
#     bots = cube.bots_in_range(bots)
#     next_to_search.extend(children)
#   to_search = next_to_search

# for i in range(29):
#   print(i, len(to_search[0].bots_in_range(bots)), len(to_search))
#   next_to_search = []
#   for cube in to_search:
#     # cube.draw(ax, color="C%i" % (i%5))
#     children = cube.best_child(bots)
#     bots = cube.bots_in_range(bots)
#     children.sort(key=lambda bot: man_dist(bot.center, (0,0,0)))
#     for child in children:
#       print(len(child.bots_in_range(bots)), child.side, man_dist(child.center, (0,0,0)))
#     print()
#     next_to_search.append(children[0])
#   to_search = next_to_search

cube = cube0
while True:
  children = cube.get_children()
  children.sort(key=lambda c: len(c.bots_in_range(bots)), reverse=True)
  cube = children[0]
  print(len(cube.bots_in_range(bots)), cube)
  if cube.side == 64:
    break
  #cube.draw(ax, color="C%i" % (i%5))

print(len(cube.bots_in_range(bots)))

max_in_range = 0
best_pos = None
for i in range(cube.x0, cube.x1+1):
  for j in range(cube.y0, cube.y1+1):
    for k in range(cube.z0, cube.z1+1):
      in_range = 0
      for bot in bots:
        dist = man_dist(bot.pos, (i,j,k))
        if dist <= bot.radius:
          in_range += 1
      if in_range > max_in_range:
        max_in_range = in_range
        best_pos = (i,j,k)
  print(i-cube.x0, max_in_range)

print(best_pos, max_in_range, man_dist(best_pos, (0,0,0)))


print("Part 2:", cube.x0+cube.y0+cube.z0)

plt.gca().set_aspect("equal")
plt.show()
