import random
MTG_COLORS = ["green", "blue", "red", "white", "black"]

class Card(object):
	def __init__(self, owner):
		self.owner = owner
		self.type = None
		self.tapped = False
	def tap(self):
		self.tapped = True
	def untap(self):
		self.tapped = False
	def upkeep(self):
		pass

class LandCard(Card):
	def __init__(self, owner, color):
		Card.__init__(self, owner)
		self.color = color
	def tap(self):
		self.owner.manapool.add(color)
		Card.tap(self)

class Deck(object):
	def __init__(self, owner):
		self.cards = []
		self.owner = owner
		pass
	def add(self, card):
		self.cards.push(card)
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

	__getattr__(self)

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

[p1.deck.add(Card()) for _ in range(60)]
[p2.deck.add(Card()) for _ in range(60)]
p1.deck.add(LandCard("green"))
p1.deck.add(LandCard("blue"))

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


