import sys

# Constant for directions of motion
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
directions = [(-1,0), (1,0), (0,-1), (0,1)]
direc_names = ["left", "right", "up", "down"]

# Represents one of the carts
class Cart:

  # Encodes position, direction of motion, turn cycle and whether dead
  def __init__(self, ID, x, y, direc):
    self.ID = ID
    self.x = x
    self.y = y
    self.direc = direc
    self.turn = 0
    self.dead = False

  # Moves the cart following the tracks
  def move(self):

    # Determine and apply possible direction change
    track = grid[self.x][self.y]
    if track == '/':
      if self.direc == LEFT: self.direc = DOWN
      elif self.direc == RIGHT: self.direc = UP
      elif self.direc == UP: self.direc = RIGHT
      elif self.direc == DOWN: self.direc = LEFT
    elif track == '\\':
      if self.direc == LEFT: self.direc = UP
      elif self.direc == RIGHT: self.direc = DOWN
      elif self.direc == UP: self.direc = LEFT
      elif self.direc == DOWN: self.direc = RIGHT
    elif track == "+":
      if self.turn == 0:
        if self.direc == LEFT: self.direc = DOWN
        elif self.direc == RIGHT: self.direc = UP
        elif self.direc == UP: self.direc = LEFT
        elif self.direc == DOWN: self.direc = RIGHT
      elif self.turn == 1:
        pass   # just continue straight
      elif self.turn == 2:
        if self.direc == LEFT: self.direc = UP
        elif self.direc == RIGHT: self.direc = DOWN
        elif self.direc == UP: self.direc = RIGHT
        elif self.direc == DOWN: self.direc = LEFT
      self.turn = (self.turn+1) % 3

    # Actually move cart according to (possibly changed) direction
    self.x += directions[self.direc][0]
    self.y += directions[self.direc][1]

  # Two carts are "equal" if their positions match
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  # Print the cart
  def __repr__(self):
    return "<Cart #%i: (%i,%i) %s>" % (self.ID, self.x, self.y, direc_names[self.direc])

# Utility function to draw the grid (for debugging)
def draw_grid():
  for j in range(NY):
    s = ""
    for i in range(NX):
      is_cart = False
      for cart in carts:
        if cart.x == i and cart.y == j:
          if cart.direc == LEFT: s += "<"
          elif cart.direc == RIGHT: s += ">"
          elif cart.direc == UP: s += "^"
          elif cart.direc == DOWN: s += "v"
          is_cart = True
          break
      if not is_cart:
        s += grid[i][j]
    print(s)

# ====================================

# Load the grid
grid = []
with open(sys.argv[1]) as f:
  for line in f:
    row = line.strip("\n")
    grid.append(row)

# Transpose grid so X,Y coincides with problem description
grid = list(map(list, zip(*grid)))

# Create carts and remove them from grid input
NX = len(grid)
NY = len(grid[0])
id_counter = 0
carts = []
for i in range(NX):
  for j in range(NY):
    s = grid[i][j]
    if s in ['<', '>', '^', 'v']:
      if s == '<':
        direc = LEFT
      elif s == '>':
        direc = RIGHT
      elif s == '^':
        direc = UP
      elif s == 'v':
        direc = DOWN
      id_counter += 1
      cart = Cart(id_counter, i, j, direc)
      carts.append(cart)
      if s in ['<', '>']:
        grid[i][j] = '-'
      elif s in ['^', 'v']:
        grid[i][j] = '|'

# ====================================

# Parts 1 and 2

tick = 0
first_collision = False
while len(carts) > 1:

  # Sort by (y, x) and reset moved status
  carts.sort(key=lambda c: c.x)
  carts.sort(key=lambda c: c.y)

  # Go over each cart, move it, and check for collisions
  i = 0
  while i < len(carts):

    cart = carts[i]

    # Skip cart if dead
    if cart.dead:
      i += 1
      continue

    # Move cart
    cart.move()

    # Check for collisions
    for j in range(len(carts)):
      if j == i or carts[j].dead: continue
      other_cart = carts[j]
      if cart == other_cart:
        print("Collision at tick %i:" % tick, cart, other_cart)
        if not first_collision:
          first_col_pos = (cart.x, cart.y)
          first_collision = True
        cart.dead = True
        other_cart.dead = True
        break

    i += 1

  # Clean up dead carts
  carts = [c for c in carts if not c.dead]

  tick += 1

print("Part 1: first collision at %i,%i" % first_col_pos)
print("Part 2: surviving cart #%i at %i,%i" % (carts[0].ID, carts[0].x, carts[0].y))
