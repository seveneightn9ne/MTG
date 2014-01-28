import random
from cards import Card
MTG_COLORS = ["green", "blue", "red", "white", "black"]

class Deck(object):
	def __init__(self, owner):
		self.cards = []
		self.owner = owner
		pass
	def add(self, card):
		self.cards.append(card)
	def draw(self):
		return self.cards.pop()
	def shuffle(self):
		random.shuffle(self.cards)

class ManaPool(object):
	def __init__(self, owner):
		self.owner = owner
		self.pool = {color: 0 for color in MTG_COLORS}
		self.pool["colorless"] = 0
	def add(self, color, n=1):
		if color in MTG_COLORS or color == "colorless":
			self.pool[color] += n
	def get(self, color):
		return self.pool[color]

	@property
	def total(self):
	    return sum(self.pool.values())

class Player(object):
	def __init__(self, name):
		self.library = Deck(self)
		self.graveyard = Deck(self)
		self.exiled = Deck(self)
		self.manapool = ManaPool(self)
		self.table = set([])
		self.hand = set([])
		self.name = name
	def untap(self):
		for card in self.table:
			card.untap()
	def upkeep(self):
		for card in self.table:
			card.upkeep()
	def drawcard(self, n=1):
		for i in range(n):
			card = self.library.draw()
			self.hand.add(card)

#pre game: load cards

p1 = Player("Dave")
p2 = Player("Mike")

[p1.library.add(Card("swamp", p1)) for _ in range(60)]
[p2.library.add(Card("plains", p2)) for _ in range(60)]
p1.library.add(Card("forest", p1))
p1.library.add(Card("island", p2))

#GAME
p1.drawcard(7)
p2.drawcard(7)
#TODO who goes first?
active = p1
while(True):
	active.untap()
	active.upkeep()
	active.drawcard()
	active.main()
