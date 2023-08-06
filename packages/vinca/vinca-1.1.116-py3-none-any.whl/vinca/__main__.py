'''Vinca 112
Simple Spaced Repetition'''

from functools import partial as _partial
from pathlib import Path as _Path
from vinca.cardlist import Cardlist as _Cardlist
from vinca.card import Card as _Card
import fire as _fire
# generators
from vinca.generators.two_lines import two_lines
q = two_lines
from vinca.generators.verses import verses
v = verses
from vinca.generators.media import media
m = media

_cards_path = _Path.home() / 'cards'
_ALL_CARDS = [_Card(int(id.name)) for id in _cards_path.iterdir()] 

col = _Cardlist(_ALL_CARDS)

# methods of the collection
browse = b = col.browse
filter = f =  col.filter
sort = col.sort
review = r =  col.review
save = col.save
load = col.load
purge = col.purge

help = lambda: 'Use --help instead'
version = lambda: 112

_fire.Fire()
'''
Add the following code to the ActionGroup object in helptext.py of fire to get proper aliasing
A better way would be to go back further into the code and check if two functions share the same id

  def Add(self, name, member=None):
    if member and member in self.members:
      dupe = self.members.index(member)
      self.names[dupe] += ', ' + name
      return
    self.names.append(name)
    self.members.append(member)
'''
'''
Make this substitution on line 458 of core.py to allow other iterables to be accessed by index

    # is_sequence = isinstance(component, (list, tuple))
    is_sequence = hasattr(component, '__getitem__') and not hasattr(component, 'values')
'''
'''
And make a corresponding change in generating the help message

  is_sequence = hasattr(component, '__getitem__') and not hasattr(component, values)
  # if isinstance(component, (list, tuple)) and component:
  if is_sequence and component:
'''
