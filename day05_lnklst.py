from string import ascii_lowercase

# Linked list implementation
class Node:
  def __init__(self, value):
    self.value = value
    self.next = None
class LinkedList:
  def __init__(self, iterable):
    self.head = None
    self.size = 0
    last = None
    self.cur = None
    for value in iterable:
      if self.head is None:
        self.head = Node(value)
        last = self.head
      else:
        node = Node(value)
        last.next = node
        last = node
      self.size += 1
  def __len__(self):
    return self.size
  def advance(self):
    self.cur = self.cur.next
  def rewind(self):
    self.cur = self.head
  def remove(self, idx):
    assert idx < self.size
    if idx == 0:
      self.head = self.head.next
    else:
      node = self.head
      prev = None
      for i in range(idx):
        prev = node
        node = node.next
      prev.next = node.next
    self.size -= 1
  def __repr__(self):
    values = []
    node = self.head
    while node is not None:
      values.append(node.value)
      node = node.next
    return "->".join(values)
  def copy(self):
    node = self.head
    iterable = []
    while node is not None:
      iterable.append(node.value)
      node = node.next
    return LinkedList(iterable)

#  Linked list test
# A = ['a', 'b', 'c', 'd', 'e']
# ll = LinkedList(A)
# print(ll)
# for i in range(len(A)):
#   ll1 = ll.copy()
#   ll1.remove(i)
#   print(ll1)

# Read in units and load them into a linked list
with open("day5.in") as f:
  for line in f:
    units_str = line.strip()
# units_str = "bcaAdeAaf"
units = LinkedList(units_str)
print(len(units_str))

def reduce(units):
  units1 = units.copy()
  while True:
    node1 = units1.head
    node2 = node1.next
    found = False
    for k in range(units1.size):
      if node2 is None:
        break
      a = node1.value
      b = node2.value
      if a.lower() == b.lower() and ((a.islower() and b.isupper()) or (a.isupper() and b.islower())):
        found = True
        break
      else:
        node1 = node2
        node2 = node1.next
    if not found:
      break
    else:
      units1.remove(k)
      units1.remove(k)
  return units1

# Part 1

reduced = reduce(units)
print(reduced)
print("Part 1:", len(reduced))

sys.exit()

# Part 2

print(len(units))
min_len = None
best_letter = None
for letter in ascii_lowercase:

  units1 = "".join([l for l in units if l != letter])
  units1 = "".join([l for l in units1 if l != letter.upper()])
  print(letter, len(units1))

  reduced = reduce(units1)
  if min_len is None or len(reduced) < min_len:
    min_len = len(reduced)
    best_letter = letter

  print(len(reduced))

print("Part 2:", min_len)
