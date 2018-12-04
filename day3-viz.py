import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re

claims = []
with open("day3.in") as f:
  pattern = r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)"
  for line in f:
    match = re.match(pattern, line.strip())
    claims.append([int(x) for x in match.groups(1)])

N = 1000
fabric = [[] for i in range(N)]
for i in range(N):
  for j in range(N):
    fabric[i].append([])
for ID, xpos, ypos, width, height in claims:
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      fabric[i][j].append(ID)
def is_special(claim):
  ID, xpos, ypos, width, height = claim
  for i in range(xpos, xpos+width):
    for j in range(ypos, ypos+height):
      if len(fabric[i][j]) > 1:
        return False
  return True
for claim in claims:
  if is_special(claim):
    special_claim = claim
    break

cm = plt.get_cmap('gist_rainbow')
NUM_COLORS = 10
colors = [cm(i/NUM_COLORS) for i in range(NUM_COLORS)]

plt.figure(figsize=(10,10))
ax = plt.gca()

i = 0
for ID, xpos, ypos, width, height in claims:
  rect = patches.Rectangle((xpos, ypos), width, height, color=colors[i%NUM_COLORS], alpha=0.5)
  ax.add_patch(rect)
  i += 1

plt.annotate("", xy=(special_claim[1]+special_claim[3]/2, special_claim[2]), xytext=(0, -30), textcoords="offset pixels", arrowprops=dict(color="k", arrowstyle="->", linewidth=2))

plt.xlim(0,1000)
plt.ylim(0,1000)
ax.set_aspect("equal")
plt.tight_layout()

plt.savefig("day3.png")
plt.show()
