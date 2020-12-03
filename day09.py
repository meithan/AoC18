import re
import sys

# A node in the doubly-linked list
class Node:
  def __init__(self, marble=None):
    self.marble = marble
    self.prev = None
    self.next = None

# The marble circle is implemented as a doubly-linked list
# This allows O(1) inserts and deletes anywhere in the circle (and the problem
# doesn't require random accesses).
# A singly-linked list also works if one simply "reflects" counter-clockwise
# moves (i.e. moving by k positions counter-clockwise is the same as moving
# by N-k positions clockwise, with N the size of the circle), but using a
# doubly-linked list to allow actual counter-clockwise moves is just a few
# extra lines of code, is faster when N is large, and feels more natural.
class MarbleCircle:

  # Initialized by inserting the root node with marble 0, which links
  # back to itself both forwards and backwards
  def __init__(self):
    node = Node(0)
    node.prev = node
    node.next = node
    self.root = node
    self.cur = self.root
    self.size = 1

  # Inserts a marble into the circle
  # Where the insertion happen depends on the current circle position
  # If the marble number is a multiple of 23, the special rules apply
  # Returns the obtained score
  def insert(self, marble):
    if marble % 23 == 0:
      score = marble
      node = self.cur
      for i in range(7):
        node = node.prev
      old_prev = node.prev
      old_next = node.next
      old_prev.next = old_next
      old_next.prev = old_prev
      self.cur = old_next
      self.size -= 1
      score += node.marble
      return score
    else:
      insert_pos = self.cur.next
      old_next = insert_pos.next
      new_node = Node(marble)
      new_node.next = old_next
      new_node.prev = insert_pos
      insert_pos.next = new_node
      old_next.prev = new_node
      self.cur = new_node
      self.size += 1
      return 0

  # Plays the game with num_players and inserting num_marbles
  def play(self, num_players, num_marbles):
    scores = [0]*num_players
    for marble in range(1, num_marbles+1):
      player = marble % num_players
      score = self.insert(marble)
      scores[player-1] += score
    return scores

  # Nice print for debugging
  def __repr__(self):
    s = []
    node = self.root
    while True:
      if node == self.cur:
        s.append("(%s)" % node.marble)
      else:
        s.append("%s" % node.marble)
      node = node.next
      if node is self.root: break
    return " ".join(s)

# =======================

# Read the number of players and the number of marbles to insert from input
# This can be done in a one-liner, but "Readability counts"!
text = open(sys.argv[1]).read().strip()
pattern = r"([0-9]+) players; last marble is worth ([0-9]+) points"
match = re.match(pattern, text)
num_players, num_marbles = match.groups()
num_players = int(num_players)
num_marbles = int(num_marbles)

# Part 1

# Just play until all the marbles are inserted, get the final scores tally
game = MarbleCircle()
scores = game.play(num_players, num_marbles)

print("Part 1:", max(scores))

# Part 2

# In part 2 the number of marbles is increased 100 times
num_marbles *= 100

# The efficient inserts/deletes of the linked list allows to tackle the
# increased problem size in a reasonable time (13 seconds on i5-7600K)
game = MarbleCircle()
scores = game.play(num_players, num_marbles)

print("Part 2:", max(scores))
