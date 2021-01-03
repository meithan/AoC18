# Day 24: Immune System Simulator 20XX

import copy
import re
import sys

# ------------------------------------------------------------------------------

class Group:

  def __init__(self, name, units, hp, atk, atk_type, init, weak, immune):
    self.name = name
    self.units = units
    self.hitpoints = hp
    self.attack = atk
    self.update_power()
    self.atk_type = atk_type
    self.initiative = init
    self.weaknesses = weak
    self.immunities = immune
    self.target = None
    self.target_dmg = None

  def full_str(self):
    return "<{}: {} units, {} hp, {} power, {} {} atk, {} init, weak to {}, immune to {}>".format(self.name, self.units, self.hitpoints, self.power, self.attack, self.atk_type, self.initiative, self.weaknesses, self.immunities)

  def __repr__(self):
    return self.name

  def update_power(self):
    self.power = self.units * self.attack

  def damage_vs(self, target):
    if self.atk_type in target.immunities:
      return 0
    elif self.atk_type in target.weaknesses:
      return self.power * 2
    else:
      return self.power

  def select_target(self, targets):

    if len(targets) == 0:
      self.target = None
      self.target_dmg = None
      return

    target = targets[0]
    target_dmg = self.damage_vs(target)

    for t in targets[1:]:
      dmg = self.damage_vs(t)
      if (dmg > target_dmg) or (dmg == target_dmg and t.power > target.power):
        target = t
        target_dmg = dmg

    if target_dmg == 0:
      self.target = None
      self.target_dmg = None
    else:
      self.target = target
      self.target_dmg = target_dmg
      targets.pop(targets.index(self.target))

def Combat(armies, boost=0, debug=False):

  if boost > 0:
    for g in armies["immune_system"]:
      g.attack += boost
      g.update_power()

  last_tot_killed = 0

  while True:

    if debug:
      for name,army in armies.items():
        print(name)
        for g in army:
          print(" {} contains {} units".format(g, g.units))
      print()

    for name,army in armies.items():
      if len(army) == 0:
        if name == "immune_system":
          winner = "infection"
        else:
          winner = "immune_system"
        if debug: print("{} wins!".format(winner))
        return winner

    # Target selection
    for atk_army, def_army in (("immune_system", "infection"), ("infection", "immune_system")):
      atk_army = armies[atk_army]
      def_army = armies[def_army]
      attackers = sorted(list(atk_army), key=lambda x: (x.power, x.initiative), reverse=True)
      targets = list(def_army)
      for g in attackers:
        g.select_target(targets)
        if debug: print(g, "targets", g.target)
    if debug: print()

    # Attack phase
    tot_killed = 0
    attackers = list(armies["infection"]) + list(armies["immune_system"])
    attackers.sort(key=lambda x: x.initiative, reverse=True)
    for attacker in attackers:
      if attacker.units > 0 and attacker.target is not None:
        target = attacker.target
        damage = attacker.damage_vs(target)
        killed = min(damage // target.hitpoints, target.units)
        target.units -= killed
        tot_killed += killed
        target.update_power()
        if debug: print("{} deals {} dmg to {}, killing {} units".format(attacker, attacker.target_dmg, target, killed))
    if debug: print()

    if tot_killed == 0 and last_tot_killed == 0:
      if debug: print("Stalemate!")
      return None
    last_tot_killed = tot_killed

    # Remove dead groups
    for army in armies.values():
      for g in list(army):
        if g.units == 0:
          if debug: print("{} is dead".format(g))
          army.remove(g)

    # if debug: input()

# ------------------------------

if len(sys.argv) == 1:
  sys.argv.append(sys.argv[0].replace(".py", ".in"))

armies_orig = {"immune_system": set(), "infection": set()}
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    if len(line) == 0:
      continue
    elif "Immune" in line:
      army = "immune_system"
    elif "Infection" in line:
      army = "infection"
    else:
      m = re.search("([0-9]+) units each with ([0-9]+) hit points ?\(?([ ,;\w]*)\)? with an attack that does ([0-9]+) (\w+) damage at initiative ([0-9]+)", line)
      # print(m.groups())
      units = int(m.group(1))
      hp = int(m.group(2))
      atk = int(m.group(4))
      atk_type = m.group(5)
      init = int(m.group(6))
      immune = []
      weak = []
      if m.group(3) != "":
        for part in m.group(3).split("; "):
          tokens = part.split(" to ")
          elems = tokens[1].split(", ")
          if tokens[0] == "immune":
            immune += elems
          elif tokens[0] == "weak":
            weak += elems
      name = "{}-{}".format("Immune" if army == "immune_system" else "Infection", len(armies_orig[army])+1)
      g = Group(name, units, hp, atk, atk_type, init, weak, immune)
      armies_orig[army].add(g)

# --------------------------------------
# Part 1

armies = copy.deepcopy(armies_orig)
winner = Combat(armies)

tot_units = sum([g.units for g in armies[winner]])

print("Part 1:", tot_units)

# --------------------------------------
# Part 2

boost = 1
while True:
  armies = copy.deepcopy(armies_orig)
  winner = Combat(armies, boost=boost, debug=False)
  print(boost, winner)
  if winner == "immune_system":
    break
  boost += 1

tot_units = sum([g.units for g in armies[winner]])

print("Part 2:", tot_units)
