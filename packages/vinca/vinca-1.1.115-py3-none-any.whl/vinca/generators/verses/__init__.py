from vinca.card import Card
from vinca.generators.decorator import generator

@generator
def verses():
	''' Quizzes one line at a time. For poetry, oratory, recipes. '''
	new_card = Card(create=True)
	new_card.editor, new_card.reviewer, new_card.scheduler = 'verses', 'verses', 'base'
	new_card.edit()
	return [new_card]
