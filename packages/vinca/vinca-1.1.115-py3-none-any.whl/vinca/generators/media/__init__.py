from vinca.card import Card
from vinca.generators.decorator import generator

@generator
def media():
	''' A card with audio and video files '''
	# initialize card
	new_card = Card(create=True)
	# initialize card metadata
	new_card.editor, new_card.reviewer, new_card.scheduler = 'media', 'media', 'base'
	# initialize card data files
	for side in ('front', 'back'):
		(new_card.path / side).touch()
	new_card.edit()  
	return [new_card]
