import re

# Even though it's more code, I prefer to use classes to store data
# and refer to it by name rather than an integer-indexed list/tuple
class Entry:
  def __repr__(self):
    return "[%s] %s" % (self.datetime, self.msg)

class Guard:
  def __init__(self, ID):
    self.ID = int(ID)
    self.log = {}
    self.total = 0
    self.max_minute = None
    self.max_minute_time = None
  def __repr__(self):
    return "Guard #%i: %i" % (self.ID, self.total)
  def asleep(self, minute):
    if minute not in self.log:
      self.log[minute] = 1
    else:
      self.log[minute] += 1
    self.total += 1
  def calc_max_minute(self):
    foo = [(x,self.log[x]) for x in self.log]
    if len(foo) > 0:
      self.max_minute = max(foo, key=lambda x: x[1])[0]
      self.max_minute_time = int(self.log[self.max_minute])

# Read in all entries
entries = []
with open("day4.in") as f:
  pattern = r"\[(([0-9]+)-([0-9]+)-([0-9]+) ([0-9]+):([0-9]+))\] (.+)"
  for line in f:
    match = re.match(pattern, line.strip())
    e = Entry()
    e.datetime = match.group(1)
    e.minute = match.group(6)
    e.msg = match.group(7)
    entries.append(e)

# Sort by date/time
entries.sort(key=lambda e: e.datetime)

# Go over guard schedule, logging when they're asleep
guards = {}
cur_guard = None
i = 0
for i in range(len(entries)):
  entry = entries[i]
  if "begins shift" in entry.msg:
    m = re.match(r"Guard #([0-9]+) begins shift", entry.msg)
    guard_ID = m.group(1)
    if guard_ID not in guards:
      guards[guard_ID] = Guard(guard_ID)
    guard = guards[guard_ID]
    cur_guard = guard
  elif entry.msg == "falls asleep":
    minute1 = int(entry.minute)
    i += 1
    entry = entries[i]
    minute2 = int(entry.minute)
    for m in range(minute1, minute2):
      cur_guard.asleep(m)

# Compute max_minute for all guards
guards = list(guards.values())
for g in guards:
  g.calc_max_minute()

# Part 1

# Determine which guard slept the most
slept_most = max(guards, key=lambda g: g.total)
max_minute = int(slept_most.max_minute)
print("Part 1:", slept_most.ID*max_minute)

# Part 2

# Determine which guard was most frequently asleep on the same minute
guards_slept = [g for g in guards if g.total > 0]
most_frequent = max(guards_slept, key=lambda g: g.max_minute_time)
max_minute = int(most_frequent.max_minute)
print("Part 2:", most_frequent.ID*max_minute)
