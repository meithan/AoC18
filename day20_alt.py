from queue import Queue
import sys

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

direcs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

# Walk the pathstr from start_room until we hit a bifurcation or end of path
def walk(start_room, pathstr):

  if verbose: print("Walking", pathstr, "from", start_room)

  room = start_room
  for i in range(len(pathstr)):

    x,y = room.xy
    c = pathstr[i]

    if c not in direcs:
      break

    if verbose: print("Walked", c)
    nx = x + direcs[c][0]
    ny = y + direcs[c][1]
    if (nx,ny) not in rooms:
      rooms[(nx,ny)] =  Room((nx,ny))
    next_room = rooms[(nx,ny)]
    room.add_exit(c)
    next_room.add_exit(opposite[c])
    room = next_room

  return i, room

def build_map(start_room, pathstr):

  Q = Queue()
  Q.put((start_room, 0))

  while not Q.qempty():

    start_room, cur_idx = Q.get()

    # Walk until end of pathstr or bifurcation
    steps, cur_room = walk(start_room, pathstr)
    cur_idx += steps

    # If end of path reached, continue with next path in queue
    if cur_idx == len(pathstr):
      break

    # Bifurcation reached
    if verbose: print("Reached bifurcation at", cur_room)

    # Look ahead to find closing parens and outermost |
    parens = 1
    j = idx + 1
    while True:
      try:
        c1 = pathstr[j]
      except:
        print("Could not find closing parens")
        print(j, pathstr)
        raise
      if c1 == "(":
        parens += 1
      elif c1 == ")":
        parens -= 1
        if parens == 0:
          break
      elif c1 == "|" and parens == 1:
        k = j
      j += 1

    # Determine and enqueue the subpaths
    subpath1 = pathstr[idx+1:k]
    if subpath1 != "":
      Q.put()
    subpath2 = pathstr[k+1:j]

    # + pathstr[j+1:]
    if verbose:
      print("Subpaths:", subpath1, "or", subpath2)
      print("Remain:", pathstr[j+1:])

    # Walk the subpaths


      cur_room



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

start_pathstr = open(sys.argv[1]).read().strip()[1:-1]
if verbose: print(start_pathstr)

rooms = {}
start_room = Room((0,0), exits=[])
rooms[(0,0)] = start_room

build_map(start_room, start_pathstr)
show_map(start_room.xy)

find_distances(rooms, start_room)

# for room in rooms.values():
#   print(room)

max_dist = None
part2_count = 0
for room in rooms.values():
  if max_dist is None or room.distance > max_dist:
    max_dist = room.distance
  if room.distance >= 1000:
    part2_count += 1

print("Part 1:", max_dist)
print("Part 2:", part2_count)
