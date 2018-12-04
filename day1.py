
# Read in increments from input
increments = []
with open("day1.in") as f:
  for line in f:
    increments.append(int(line))

# Part 1

total = sum(increments)
print("Part 1:", total)

# Part2

# Using a set with O(1) inserts/lookups (on average) 
# greatly speeds up solution
seen = set()
freq = 0
i = 0
while True:
  freq += increments[i%len(increments)]
  if freq in seen:
    break
  else:
    seen.add(freq)
  i += 1

print("Part 2:", freq)
