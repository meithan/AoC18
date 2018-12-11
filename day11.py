
import sys

# Read in serial number
serial_no = int(open(sys.argv[1]).read().strip())

# Set grid size
N = 300

# Returns the power cell (x,y) (note these start at 1)
def get_power(x, y):
  rack_ID = x + 10
  power = rack_ID * y
  power += serial_no
  power *= rack_ID
  power = (power // 100) % 10
  power -= 5
  return power

def find_max_square(size):
  Np = N - size + 1
  # Pre-compute sub-column sums
  subcols = [[0]*(Np) for i in range(N)]
  for j in range(Np):
    for i in range(N):
      if j == 0:
        # For the first row of subcols the full sum is computed
        subcols[i][j] = sum(grid[i][j:j+size])
      else:
        # For subsequent subcols, we take the value of the previous
        # subcol, add the next grid value (vertically) and subtract
        # the previous grid value
        subcols[i][j] = subcols[i][j-1] + grid[i][j+size-1] - grid[i][j-1]
  # Determine max power square
  max_power = None
  max_power_cell = None
  for i in range(Np):
    for j in range(Np):
      tot_power = 0
      # We only have to add size subcol values to get the square value
      for k in range(size):
        tot_power += subcols[i+k][j]
      if max_power is None or tot_power > max_power:
        max_power = tot_power
        max_power_cell = (i+1,j+1)
  return max_power_cell, max_power

# ================================

# The power grid
grid = [[0]*N for i in range(N)]

# Compute power for all cells
for i in range(N):
  for j in range(N):
    grid[i][j] = get_power(i+1, j+1)

# Part 1

max_power_cell, max_power = find_max_square(3)
print("Part 1:", max_power_cell)

# Part 2

global_max_power = None
global_max_cell = None
global_max_size = None
for size in range(1,N+1):
  max_power_cell, max_power = find_max_square(size)
  if global_max_power is None or max_power > global_max_power:
    global_max_power = max_power
    global_max_cell = max_power_cell
    global_max_size = size
  print(size, max_power, max_power_cell)

print("Part 2:", global_max_cell+(global_max_size,))
