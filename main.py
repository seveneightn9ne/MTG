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
		if len(self.cards) > 0:
			return self.cards.pop()
		else:
			print self.owner.name + "'s deck is empty!"
			return None
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
	def pull(self, amt, color="colorless"):
		if color == "colorless":
			amt_colorless = self.pool["colorless"]
			self.pool["colorless"] = max(0, amt_colorless-amt)
			amt -= amt_colorless
			if amt > 0:
				#need to pull colored mana
				for color in self.pool.keys():
					amt_color = self.pool[color]
					self.pool[color] = max(0, amt_color - amt)
					amt -= amt_color
					if amt <= 0:
						break
				if amt > 0:
					raise Exception("Not enough mana in the mana pool!")
		else:
			if amt > self.pool[color]:
				raise Exception("Not enough mana in the mana pool!")
			else:
				self.pool[color] -= amt

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
		self.canPlaceLand = True
	def untap(self):
		for card in self.table:
			card.untap()
			self.canPlaceLand = True
	def upkeep(self):
		for card in self.table:
			card.upkeep()
	def drawcard(self, n=1):
		for i in range(n):
			card = self.library.draw()
			self.hand.add(card)
			print self.name + " draws " + str(card)
	def main(self):
		#place land if able
		if self.canPlaceLand:
			# print self.name + " can place a land this turn."
			for card in self.hand:
				# print self.name + " looks at his " + str(card)
				# print "it is a " + card.data["type"]
				if card.data["type"] == "Basic Land":
					self.hand.remove(card)
					self.table.add(card)
					print self.name + " places " + str(card) + " on the table."
					self.canPlaceLand = False
					break
		#tap all lands
		for card in self.table:
			if card.data["type"] == "Basic Land":
				card.tap()
		#place affordable creatures
		for card in filter(lambda card: card.data["type"]=="Creature", self.hand):
			cost = {'colorless': card.data["cost"].get("any", 0)}
			for m in card.data["cost"].keys():
				#TODO eval colored mana before colorless!
				if m == "any":
					continue
				elif self.manapool.get(m) < card.data["cost"][m]:
					#can't afford this creature
					return
				cost[m] = cost.get(m, 0) + card.data["cost"][m]
			if sum(cost.values()) > self.manapool.total:
				#can't afford this creature
				continue # to next creature
			else:
				for color in cost.keys():
					if color != 'colorless':
						self.manapool.pull(cost[color], color)
				self.manapool.pull(cost['colorless'], 'colorless')
				self.hand.remove(card)
				self.table.add(card)
				print self.name + " places " + str(card) + " on the table."

#pre game: load cards

p1 = Player("Dave")
p2 = Player("Mike")

[p1.library.add(Card("swamp", p1)) for _ in range(60)]
[p2.library.add(Card("plains", p2)) for _ in range(60)]
p1.library.add(Card("forest", p1))
p2.library.add(Card("island", p2))
p1.library.add(Card("elvish-visionary", p1))
p2.library.add(Card("voiceless-spirit", p2))

#GAME
p1.drawcard(7)
p2.drawcard(7)
#TODO who goes first?
active = p1
ticker = 0
while(True):
	print active.name + "'s turn!"
	active.untap()
	active.upkeep()
	active.drawcard()
	active.main()
	if active == p1:
		active = p2
	else:
		active = p1
	ticker += 1
	if ticker > 5:
		break
