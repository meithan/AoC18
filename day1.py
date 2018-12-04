increments = []
with open("day1.in") as f:
  for line in f:
    increments.append(int(line))

total = sum(increments)
print("Part 1:", total)

seen = set()
freq = 0
i = 0
while True:
  inc = increments[i%len(increments)]
  freq += inc
  if freq in seen:
    break
  else:
    seen.add(freq)
  i += 1

print("Part 2:", freq)
