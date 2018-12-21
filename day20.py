from queue import Queue
import sys

direcs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

# A room. Contains the location and the of exits out of the room.
class Room:
  def __init__(self, loc, exits=None):
    self.xy = loc
    self.x = self.xy[0]
    self.y = self.xy[1]
    if exits is None:
      self.exits = set()
    else:
      self.exits = set(exits)
    self.distance = None
  def add_exit(self, direc):
    self.exits.add(direc)
  def __repr__(self):
    s = "<Room at (%s), exits: %s" % (repr(self.xy), repr(self.exits))
    if self.distance is not None:
      s += ", dist: %i" % self.distance
    s += ">"
    return s

# Print the map to the terminal
def show_map(start_loc=None):
  xs = [pos[0] for pos in rooms]
  ys = [pos[1] for pos in rooms]
  xmin = min(xs)
  xmax = max(xs)
  ymin = min(ys)
  ymax = max(ys)
  end_row = "    " + "#"*(2*(xmax-xmin+1)) + "#"
  print(end_row)
  for y in range(ymin, ymax+1):
    row1 = "%3i #" % y
    for x in range(xmin, xmax+1):
      if start_loc is not None and (x,y) == start_loc:
        row1 += "X"
      else:
        if (x,y) in rooms:
          row1 += "."
        else:
          row1 += "#"
      if x != xmax:
        if (x,y) in rooms and 'E' in rooms[(x,y)].exits:
          row1 += '|'
        else:
          row1 += '#'
    row1 += "#"
    print(row1)
    if y != ymax:
      row2 = "    #"
      for x in range(xmin, xmax+1):
        if (x,y) in rooms and 'S' in rooms[(x,y)].exits:
          row2 += '-'
        else:
          row2 += '#'
        row2 += "#"
      print(row2)
  print(end_row)

# Build the map given the start_room and the paths
def build_map(start_room, start_pathstr):

  idx = 0
  last_bifur = []
  cur_room = start_room

  while idx < len(start_pathstr):

    x,y = cur_room.xy
    c = pathstr[idx]

    if c in direcs:

      if verbose: print("Walked", c)
      nx = x + direcs[c][0]
      ny = y + direcs[c][1]
      if (nx,ny) not in rooms:
        rooms[(nx,ny)] =  Room((nx,ny))
      next_room = rooms[(nx,ny)]
      cur_room.add_exit(c)
      next_room.add_exit(opposite[c])
      cur_room = next_room

    elif c == "(":

      last_bifur.append(cur_room)
      if verbose: print("Reached bifurcation at", cur_room)

    elif c == "|":

      cur_room = last_bifur[-1]
      if verbose: print("Trying second path from", cur_room)

    elif c == (")"):

      cur_room = last_bifur.pop()
      if verbose: print("Backtracking to", cur_room)

    idx += 1


# Find the distances to every room from the given starting room
# This uses breadth-first search
def find_distances(rooms, start_room):

  Q = Queue()
  Q.put((0, start_room))
  visited = set()
  enqueued = set()

  while not Q.empty():

    dist, cur_room = Q.get()
    if cur_room.distance is None or dist < cur_room.distance:
      cur_room.distance = dist
    x, y = cur_room.xy

    for e in cur_room.exits:
      nx = x + direcs[e][0]
      ny = y + direcs[e][1]
      if (nx,ny) in visited:
        continue
      if (nx,ny) not in enqueued:
        next_room = rooms[(nx,ny)]
        Q.put((dist+1, next_room))
        enqueued.add((nx,ny))

    visited.add(cur_room.xy)

# ==============================================================================

verbose = False

# Load paths (problem input)
pathstr = open(sys.argv[1]).read().strip()[1:-1]
if verbose: print(pathstr)

# Build the map
rooms = {}
start_room = Room((0,0), exits=[])
rooms[(0,0)] = start_room
build_map(start_room, pathstr)
show_map(start_room.xy)

# Find distances from starting room
find_distances(rooms, start_room)

# Determine max distance and number of rooms with distance >= 1000 steps
max_dist = None
part2_count = 0
for room in rooms.values():
  if max_dist is None or room.distance > max_dist:
    max_dist = room.distance
  if room.distance >= 1000:
    part2_count += 1

print("Part 1:", max_dist)
print("Part 2:", part2_count)

f = open("day20.txt", "w")
for room in rooms.values():
  f.write("%i %i %i %s\n" % (room.x, room.y, room.distance, "".join(room.exits)))
f.close()
