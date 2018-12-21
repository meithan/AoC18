import matplotlib.cm
from PIL import Image

class Room:
  def __init__(self, x, y, dist, exits):
    self.x = x
    self.y = y
    self.dist = dist
    self.exits = set(exits)

rooms = {}
with open("day20.txt") as f:
  for line in f:
    tokens = line.strip().split()
    x = int(tokens[0])
    y = int(tokens[1])
    dist = int(tokens[2])
    exits = [e for e in tokens[3]]
    rooms[(x,y)] = Room(x, y, dist, exits)

# Determine farthest room
# Determine max distance and number of rooms with distance >= 1000 steps
max_dist = None
farthest = None
for room in rooms.values():
  if max_dist is None or room.dist > max_dist:
    max_dist = room.dist
    farthest = room

# Trace path from farthest back to origin
#print(len([room for room in rooms.values() if room.distance == max_dist]))
direcs = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)}
path = [(farthest.x, farthest.y)]
room = farthest
while room.dist > 0:
  x,y = room.x, room.y
  next_rooms = []
  for e in room.exits:
    nx = x + direcs[e][0]
    ny = y + direcs[e][1]
    next_rooms.append(rooms[(nx,ny)])
  next_rooms.sort(key=lambda x: x.dist)
  room = next_rooms[0]
  path.append((room.x, room.y))

cell_size = 5

NX = 2*100 + 1
NY = 2*100 + 1
xoff = min(room.x for room in rooms.values())
yoff = min(room.y for room in rooms.values())
print(xoff, yoff)

maze = []
for j in range(NY):
  maze.append([(0,0,255)]*NX)

wall = (50, 50, 50)
door = (180, 180, 180)
start = (255, 0, 0)
end = (0, 255, 0)
path_color = (0, 150, 130)

cmap = matplotlib.cm.get_cmap('jet')
def get_color(dist):
  col = cmap(dist/max_dist)
  return (int(col[0]*255), int(col[1]*255), int(col[2]*255))

for i in range(NX):
  for j in range(NY):

    x = i // 2 + xoff
    y = j // 2 + yoff

    if i == 0 or i == NX-1 or j == 0 or j == NY-1:

      maze[i][j] = wall

    elif i % 2 == 1 and j % 2 == 1:

      if x == 0 and y == 0:
        maze[i][j] = start
      elif (x,y) == (farthest.x, farthest.y):
        maze[i][j] = end
      elif (x,y) in path:
        maze[i][j] = get_color(rooms[(x,y)].dist)
      else:
        maze[i][j] = door

    elif i % 2 == 0 and j % 2 == 0:

      maze[i][j] = wall

    elif i % 2 == 0 and j % 2 == 1:

      if (x-1,y) in path and (x,y) in path and abs(rooms[(x,y)].dist - rooms[(x-1,y)].dist) == 1:
        dist = (rooms[(x,y)].dist + rooms[(x-1,y)].dist)/2
        maze[i][j] = get_color(dist)
      elif "W" in rooms[(x,y)].exits:
        maze[i][j] = door
      else:
        maze[i][j] = wall

    elif i % 2 == 1 and j % 2 == 0:

      if (x,y-1) in path and (x,y) in path and abs(rooms[(x,y)].dist - rooms[(x,y-1)].dist) == 1:
        dist = (rooms[(x,y)].dist + rooms[(x,y-1)].dist)/2
        maze[i][j] = get_color(dist)
      elif "N" in rooms[(x,y)].exits:
        maze[i][j] = door
      else:
        maze[i][j] = wall

    if j == 2 and i == 1:
      print(i, j, x, y, rooms[(x,y)].exits, maze[i][j])


width = NX * cell_size
height = NY * cell_size

img = Image.new('RGB', (width, height))
pix = img.load()
for x in range(width):
  for y in range(height):
    i = int(x // cell_size)
    j = int(y // cell_size)
    pix[x,y] = maze[i][j]

fname = "day20.png"
img.save(fname)
print(fname)
