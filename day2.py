from collections import Counter

codes = []
with open("day2.in") as f:
  for line in f:
    codes.append(line.strip())

has_two = 0
has_three = 0
for code in codes:
  counts = Counter(code)
  if 2 in counts.values(): has_two += 1
  if 3 in counts.values(): has_three += 1
print("Part 1:", has_two*has_three)

def find_code(codes):
  for i in range(len(codes)):
    code1 = codes[i]
    for j in range(i+1, len(codes)):
      code2 = codes[j]
      same = 0
      for k in range(len(code1)):
        if code1[k] == code2[k]:
          same += 1
      difs = len(code1) - same
      if difs == 1:
        common = ""
        for k in range(len(code1)):
          if code1[k] == code2[k]:
            common += code1[k]
        return common
common = find_code(codes)
print("Part 2:", common)
