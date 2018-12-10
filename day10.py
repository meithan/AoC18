from math import sqrt
import re
import sys
import matplotlib.pyplot as plt

plt.ion()

# Represents a particle, its position and speed, and a move method
class Particle:
  def __init__(self, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
  def move(self):
    self.x += self.vx
    self.y += self.vy

# Using regex for parsing, just for practice
pattern = re.compile(r"position=<([ \+\-0-9]+),([ \+\-0-9]+)> velocity=<([ \+\-0-9]+),([ \+\-0-9]+)>")

# Load the particles (positions and speeds) from input
particles = []
with open(sys.argv[1]) as f:
  for line in f:
    x, y, vx, vy = [int(x) for x in pattern.match(line).groups()]
    particles.append(Particle(x, y, vx, vy))

# We plot the particles and visually search for the message only when
# their bounding box has the max of (width, height) within this value
# Determined by trial and error. Started with 300 and gradually
# narrowed it down.
bbox_search_size = 65

# Iterate particle motion and plot when bounding box is small
time = 0
while True:

  xs = [p.x for p in particles]
  ys = [-p.y for p in particles]   # reverse since up is negative
  bbox_size = max(abs(max(xs)-min(xs)), abs(max(ys)-min(ys)))

  if bbox_size <= bbox_search_size:
    print(time, bbox_size)
    plt.figure(figsize=(10,2))
    plt.scatter(xs, ys)
    plt.tight_layout()
    ans = input("Message found? (y/N) ")
    if ans.lower() in ("y", "yes"): break
    plt.close()

  for p in particles:
    p.move()
  time += 1

  if time % 1000 == 0: print(time, bbox_size)

print("Part 1: <read message from plot>")
print("Part 2:", time)

input("Press ENTER to exit")
