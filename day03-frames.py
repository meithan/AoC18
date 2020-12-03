import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
import sys

class Claim:
  def __init__(self, ID, xpos, ypos, width, height):
    self.ID = ID
    self.xpos = xpos
    self.ypos = ypos
    self.width = width
    self.height = height

all_claims = []
with open("day3.in") as f:
  pattern = r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
  for line in f:
    match = re.match(pattern, line.strip())
    all_claims.append(Claim(*[int(x) for x in match.groups(1)]))


def plot(claims):

  def is_special(claim):
    for i in range(claim.xpos, claim.xpos+claim.width):
      for j in range(claim.ypos, claim.ypos+claim.height):
        if len(fabric[i][j]) > 1:
          return False
    return True

  N = 1000
  fabric = [[] for i in range(N)]
  for i in range(N):
    for j in range(N):
      fabric[i].append([])
  for claim in claims:
    for i in range(claim.xpos, claim.xpos+claim.width):
      for j in range(claim.ypos, claim.ypos+claim.height):
        fabric[i][j].append(claim.ID)

  plt.figure(figsize=(10,10))
  ax = plt.gca()

  for claim in claims:
    if is_special(claim):
      color = "limegreen"
      alpha = 0.7
    else:
      color = "red"
      alpha = 0.2
    rect = patches.Rectangle((claim.xpos, claim.ypos), claim.width, claim.height, color=color, alpha=alpha)
    ax.add_patch(rect)

  plt.xlim(0,1000)
  plt.ylim(0,1000)
  ax.set_aspect("equal")
  plt.tight_layout()

  fname = "frame%04i.png" % k
  plt.savefig(fname)
  print(fname)
  plt.close()
  # plt.show()

k1 = int(sys.argv[1])
k2 = int(sys.argv[2])

for k in range(k1, k2+1):
  plot(all_claims[:k+1])
