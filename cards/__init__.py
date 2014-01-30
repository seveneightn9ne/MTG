import yaml
import os.path


def load_card_data(cardpath):
  """
  :param cardpath: path to card file relative to cards directory.
    cardpath does not include .yml
  :returns: data loaded from yaml file.
  """
  return yaml.load(open(
    os.path.join(os.path.dirname(__file__), cardpath + ".yml")
  ))


class Card(object):
  def __init__(self, cardpath, owner):
    self.data = load_card_data(cardpath)
    self.owner = owner
    self.tapped = False

  def __str__(self):
    r = self.data['name'] + " (" + self.data['type']
    if 'power' in self.data.keys() and 'toughness' in self.data.keys():
      r += ", " + self.data['power'] + "/" + self.data['toughness']
    return  r + ")"

  def __repr__(self):
    return self.__str__()

  def tap(self):
    if self.data["type"] == "Basic Land":
      self.owner.manapool.add(self.data["color"])
    self.tapped = True

  def untap(self):
    self.tapped = False

  def upkeep(self):
    pass

  def __repr__(self):
    return "[{} {} ({})]".format(
      self.data["color"][0:2],
      self.data["name"],
      self.owner,
    )
