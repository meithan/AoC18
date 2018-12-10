from math import sqrt
import re
import sys
import matplotlib.pyplot as plt

plt.ion()

# Represents a particle, its position and speed, a move method
# and a method to return its squared distance to the origin
class Particle:
  def __init__(self, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
  def move(self):
    self.x += self.vx
    self.y += self.vy
  def dist2(self):
    return self.x**2 + self.y**2

# Using regex for parsing, just for practice
pattern = re.compile(r"position=<([ \+\-0-9]+),([ \+\-0-9]+)> velocity=<([ \+\-0-9]+),([ \+\-0-9]+)>")

# Load the particles (positions and speeds) from input
particles = []
with open(sys.argv[1]) as f:
  for line in f:
    x, y, vx, vy = [int(x) for x in pattern.match(line).groups()]
    particles.append(Particle(x, y, vx, vy))

# We plot the particles to search for the message only when all
# particles are within this distance of the origin.
# Determined by trial and error. Started with 500 and gradually
# narrowed it down.
search_dist = 280

# Iterate particle motion and plot only when all particles are
# within search_dist
time = 0
while True:

  # Finding the max of *squared* distances saves an expensive sqrt
  # for each particle
  max_dist = sqrt(max([p.dist2() for p in particles]))
  if max_dist <= search_dist:
    print(time, max_dist)
    plt.figure(figsize=(10,2))
    xs = [p.x for p in particles]
    ys = [-p.y for p in particles]   # reverse since up is negative
    plt.scatter(xs, ys)
    plt.tight_layout()
    ans = input("Message found? (y/N) ")
    if ans.lower() in ("y", "yes"): break
    plt.close()

  for p in particles:
    p.move()
  time += 1

  if time % 1000 == 0: print(time, max_dist)

print("Part 1: <read message from plot>")
print("Part 2:", time)

input("Press ENTER to exit")
