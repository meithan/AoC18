import sys

# ===============================

num_scores_str = open(sys.argv[1]).read().strip()
# num_scores_str = "59414"

N = len(num_scores_str)
num_scores = int(num_scores_str)

# Parts 1 and 2

scores = [3, 7]
elf1 = 0
elf2 = 1
part1_ans = None
part2_ans = None
it = 0

while part1_ans is None or part2_ans is None:

  tot = scores[elf1] + scores[elf2]
  for d in str(tot):
    scores.append(int(d))

  elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
  elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

  if part1_ans is None and len(scores) >= num_scores + 10:
    part1_ans = "".join([str(x) for x in scores[num_scores:num_scores+10]])
    print("Found part 1:", part1_ans)

  if part2_ans is None:
    tail = "".join([str(x) for x in scores[-N-1:]])
    if tail[1:] == num_scores_str:
      part2_ans = len(scores) - N
    elif tail[:-1] == num_scores_str:
      part2_ans = len(scores) - N - 1
    if not part2_ans is None:
      print("Found part 2:", part2_ans)

  it += 1
  if it % 1000000 == 0: print(it//1000000, len(scores))

print()
print("Part 1:", part1_ans)
print("Part 2:", part2_ans)
