from queue import PriorityQueue
import sys

# The types of terrain
KIND_ROCKY = 0
KIND_WET = 1
KIND_NARROW = 2
kind_names = {KIND_ROCKY: "rocky", KIND_WET: "wet", KIND_NARROW: "narrow"}

# The items that can be equipped
ITEM_NONE = 0
ITEM_TORCH = 1
ITEM_GEAR = 2
item_names = {ITEM_NONE: "none", ITEM_TORCH: "torch", ITEM_GEAR: "gear"}

# The items valid in each type of terrain
valid_items = {KIND_ROCKY: [ITEM_TORCH, ITEM_GEAR], KIND_WET: [ITEM_GEAR, ITEM_NONE], KIND_NARROW: [ITEM_TORCH, ITEM_NONE]}

# Terminal colors
FMT_RED_BLINK = "\033[31;1;5m"
FMT_WHITE_BLINK = "\033[33;1;5m"
FMT_GREEN = "\033[32;1m"
FMT_RED = "\033[31;1m"
FMT_RESET = "\033[0m"
FMT_BOLD = "\033[33;1m"

# Repreents the cave
# We compute the geology way past the location of the target
# in prepareation in Part 2
class Cave:

  def __init__(self, depth, target_loc):
    self.depth = depth
    self.target_X, self.target_Y = target_loc
    self.xmax = 12*self.target_X
    self.ymax = self.target_Y*3//2
    self.NX = self.xmax + 1
    self.NY = self.ymax + 1
    self.geo_idx = []
    self.erosion = []
    self.kind = []
    for i in range(self.NX):
      self.geo_idx.append(['']*self.NY)
    for i in range(self.NX):
      self.erosion.append(['']*self.NY)
    for i in range(self.NX):
      self.kind.append(['']*self.NY)
    self.geology()

  # Compute the geology of the cave
  def geology(self):
    for y in range(self.NY):
      for x in range(self.NX):
        if x == 0 and y == 0:
          self.geo_idx[x][y] = 0
        elif x == self.target_X and y == self.target_Y:
          self.geo_idx[x][y] = 0
        elif y == 0:
          self.geo_idx[x][y] = x * 16807
        elif x == 0:
          self.geo_idx[x][y] = y * 48271
        else:
          self.geo_idx[x][y] = self.erosion[x-1][y] * self.erosion[x][y-1]
        self.erosion[x][y] = (self.geo_idx[x][y] + self.depth) % 20183
        self.kind[x][y] = self.erosion[x][y] % 3

  # Print cave to terminal
  def show(self, active=None, highlighted=None):
    for y in range(self.NY):
      s = ""
      for x in range(self.NX):
        if self.kind[x][y] == KIND_ROCKY:
          symb = 'o'
        elif self.kind[x][y] == KIND_WET:
          symb = '='
        elif self.kind[x][y] == KIND_NARROW:
          symb = '|'
        elif x == 0 and y == 0:
          symb = 'M'
        elif x == self.target_X and y == self.target_Y:
          symb = 'T'
        if active is not None and x == active[0] and y == active[1]:
          s += FMT_WHITE_BLINK + symb +  FMT_RESET
        elif x == 0 and y == 0:
          s += FMT_GREEN + symb + FMT_RESET
        elif x == self.target_X and y == self.target_Y:
          s += FMT_RED + symb +  FMT_RESET
        else:
          if highlighted is not None and (x,y) in highlighted:
            s += FMT_BOLD + symb + FMT_RESET
          else:
            s += symb
      print(s)

  # Compute the total risk in the rectangle having the
  # mouth and target as corners, for Part 1
  def calc_risk(self):
    tot_risk = 0
    for y in range(self.target_Y + 1):
      for x in range(self.target_X + 1):
        tot_risk += self.kind[x][y]
    return tot_risk

# The state of the walker: position and currently equipped item
# Importantly, contains a method to determine the legal states
# that are reachable from it
class State:
  def __init__(self, x, y, item):
    self.x = x
    self.y = y
    self.pos = (x,y)
    self.kind = cave.kind[self.x][self.y]
    self.item = item
  def __hash__(self):
    return hash((self.x, self.y, self.item))
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.item == other.item
  def __lt__(self, other):
    # return (self.x, self.y) < (other.x, other.y)
    return self.y > other.y
    # return True
  def __repr__(self):
    return "[%i, %i (%s); %s]" % (self.x, self.y, kind_names[cave.kind[self.x][self.y]], item_names[self.item])
  # Returns the valid children SearchNodes, and cost in minutes, of
  # square (x,y) given the currently equipped item
  def get_children(self):
    children = []
    # Move (when item is compatible)
    for dx, dy in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
      nx = self.x + dx
      ny = self.y + dy
      if nx >= 0 and ny >= 0:
        if nx > cave.xmax:
          print("Search exceeded xmax=%i" % (cave.xmax))
          sys.exit()
        elif ny > cave.ymax:
          print("Search exceeded ymax=%i" % (cave.ymax))
          sys.exit()
        nkind = cave.kind[nx][ny]
        if self.item in valid_items[nkind]:
          time_cost = 1
          # print(item_names[cur_item], item_names[next_item], distance)
          if dx == -1: action = 'L'
          elif dx == +1: action = 'R'
          elif dy == -1: action = 'U'
          elif dy == +1: action = 'D'
          children.append((action, time_cost, State(nx, ny, self.item)))
    # Stay in place but change to the other item
    for item in valid_items[self.kind]:
      if item != self.item:
        time_cost = 7
        action = item_names[item]
        children.append((action, time_cost, State(self.x, self.y, item)))
    return children

# Manhattan distance between two pairs of coordinates
def man_dist(pos1, pos2):
  x1, y1 = pos1
  x2, y2 = pos2
  return abs(x1-x2) +  abs(y1-y2)

# The estimated distance between the two states
# This is the Manhattan distance between the coordinates
def heuristic(state1, state2):
  return man_dist(state1.pos, state2.pos)

# A search node
# Contains the state, the cost incurred so far and the actions
# required to get there
class SearchNode:
  def __init__(self, state, back_cost, actions):
    self.state = state
    self.back_cost = back_cost
    self.actions = actions
  def __eq__(self, other):
    return self.state == other.state
  def __lt__(self, other):
    return self.state < other.state

# A* search algorithm
# This implementation is basically generic
# The only requirement is for the State class to have a
# get_children() method
def AstarSearch(start_state, goal_state):

  start_node = SearchNode(state=start_state, back_cost=0, actions=tuple())
  fringe = PriorityQueue()
  closed_set = set()
  fringe.put((0, start_node))
  nodes_opened = 0

  while not fringe.empty():

    _, node = fringe.get()
    nodes_opened += 1

    if node.state == goal_state:

      return node, nodes_opened

    if node.state not in closed_set:

      closed_set.add(node.state)

      for action, cost, new_state in node.state.get_children():

        child = SearchNode(new_state, node.back_cost + cost, node.actions + (action,))
        priority = child.back_cost + heuristic(child.state, goal_state)
        fringe.put((priority, child))

# ============================================

with open(sys.argv[1]) as f:
  depth = int(f.readline().split(":")[1])
  target_loc = tuple(int(x) for x in f.readline().strip().split(":")[1].split(','))

cave = Cave(depth, target_loc)
# cave.show()

# Part 1

print("Part 1:", cave.calc_risk())

# Part 2

start_state = State(x=0, y=0, item=ITEM_TORCH)
goal_state = State(x=cave.target_X, y=cave.target_Y, item=ITEM_TORCH)
end_node, nodes_opened = AstarSearch(start_state, goal_state)

print("Reached goal; %i nodes opened" % nodes_opened)
# print(node.actions)
total_time = 0
moves = 0
changes = 0
for action in end_node.actions:
  if action in ['R', 'L', 'U', 'D']:
    total_time += 1
    moves += 1
  elif action in item_names.values():
    total_time += 7
    changes += 1
print("Total time:", total_time)
print("Moves:", moves)
print("Equip changes:", changes)

print("Part 2:", total_time)
