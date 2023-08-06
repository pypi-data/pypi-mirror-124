'''Vinca 112
Simple Spaced Repetition'''

from functools import partial as _partial
from pathlib import Path as _Path
from vinca.cardlist import Cardlist as _Cardlist
from vinca.card import Card as _Card
from vinca.generators.media import media
from vinca.generators.two_lines import two_lines
from vinca.generators.verses import verses
import fire as _fire

_cards_path = _Path.home() / 'cards'
_ALL_CARDS = [_Card(int(id.name)) for id in _cards_path.iterdir()] 

_collection = _Cardlist(_ALL_CARDS)

card = lambda id: _Card(id)
card.__doc__ = '```card 103 delete``` will delete card 103'
# methods of the collection
browse = _collection.browse
filter = _collection.filter
review = _collection.review
save = _collection.save
load = _collection.load
purge = _collection.purge

help = lambda: 'Use --help instead'
version = lambda: 112

_fire.Fire()
