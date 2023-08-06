import re
import datetime
from functools import partial
from shutil import copytree, rmtree
from pathlib import Path
TODAY = datetime.date.today()
DAY = datetime.timedelta(days = 1)
from vinca.browser import Browser
from vinca.generators import generators_dict
from vinca.lib.terminal import LineWrapOff
from vinca.lib import ansi
from vinca.lib.fancy_input import fancy_input
from vinca.lib.readkey import readkey

cards_path = Path('~/cards')

class Cardlist(list):

	def __init__(self, *args):
		list.__init__(self, *args)
		self.browser_commands_dict = {'D': self.mass_delete,
					      'T': self.edit_tags}

	def __str__(self):
		s = ''
		l = len(self)
		if l == 0:
			return 'No cards.'
		if l > 10:
			s += f'10 of {l}\n'
		s += ansi.codes['line_wrap_off']
		for card in self[:10]:
			if card.due_as_of(TODAY):
				s += ansi.codes['bold']
				s += ansi.codes['blue']
			if card.deleted:
				s += ansi.codes['crossout']
				s += ansi.codes['red']
			s += f'{card.id}\t{card}\n'
			s += ansi.codes['reset']
		s += ansi.codes['line_wrap_on']
		return s

	def browse(self):
		''' scroll through your collection with j and k '''
		Browser(self).browse()

	def review(self):
		''' review all cards '''
		Browser(self).review()
				
	def mass_delete(self):
		for card in self:
			card.deleted = True

	def add_tag(cards, tag):
		for card in self:
			card.tags += [tag]

	def remove_tag(cards, tag):
		for card in self:
			if tag in card.tags:
				card.tags.remove(tag)
			# TODO do this with set removal
			card.save_metadata()

# TODO a decorator that implements scrollback by computing how much has been printed to stdout
	def edit_tags(self):
		tags_add = fancy_input(prompt = 'tags to add: ', completions = ALL_TAGS).split()
		tags_remove = fancy_input(prompt = 'tags to remove: ', completions = ALL_TAGS).split()
		for tag in tags_add:
			add_tag(cards = cards, tag = tag)
		for tag in tags_remove:
			remove_tag(cards = cards, tag = tag)

	def save(self, save_path):
		''' Backup your cards. '''
		save_path = Path(save_path)
		for card in self:
			copytree(card.path, save_path / str(card.id))

	@staticmethod
	def load(load_path, overwrite = False):
		load_path = Path(load_path)
		if overwrite:
			rmtree(cards_path)
			copytree(load_path, cards_path)
			return
		old_ids = [card.id for card in ALL_CARDS]
		max_old_id = max(old_ids, default = 1)
		for new_id,card_path in enumerate(load_path.iterdir(), max_old_id + 1):
			copytree(card_path, cards_path / str(new_id))


	def purge(self):
		''' Permanently delete all cards marked for deletion. '''
		deleted_cards = self.filter(deleted_only = True)
		if not deleted_cards:
			print('no cards are marked for deletion.')
			return
		print(f'delete {len(deleted_cards)} cards? (y/n)')
		if (confirmation := readkey()) == 'y':
			for card in deleted_cards:
				rmtree(card.path)




	def filter(self, pattern='', 
		   tags_include={}, tags_exclude={}, # specify a SET of tags
		   create_date_min=None, create_date_max=None,
		   seen_date_min=None, seen_date_max=None,
		   due_date_min=None, due_date_max=None,
		   editor=None, reviewer=None, scheduler=None,
		   deleted_only=False, 
		   due_only=False,
		   new_only=False,
		   invert=False):
		''' try --due_only or --pattern='Gettysburg Address' '''
		
		
		# cast dates to datetime format
		for date in ('create_date_min','create_date_max','seen_date_min','seen_date_max','due_date_min','due_date_max'):
			arg = locals()[date]
			if arg is int:
				locals()[date] = TODAY + arg*DAY
			elif isinstance(arg, str):
				try:
					locals()[date] = datetime.date.fromisoformat(arg)
				except ValueError as e:
					print(f'Dates must be integer or iso format')
					raise e

		if due_only: due_date_max = TODAY
		# compile the regex pattern for faster searching
		p = re.compile(f'({pattern})')  # wrap in parens to create regex group \1

		tags_include, tags_exclude = set(tags_include), set(tags_exclude)

		f = lambda card: (((not tags_include or bool(tags_include & set(card.tags))) and
				(not tags_exclude or not bool(tags_exclude & set(card.tags))) and
				(not create_date_min or create_date_min <= card.create_date) and
				(not create_date_max or create_date_max >= card.create_date) and 
				(not seen_date_min or seen_date_min <= card.seen_date) and
				(not seen_date_max or seen_date_max >= card.seen_date) and 
				(not due_date_min or due_date_min <= card.due_date) and
				(not due_date_max or due_date_max >= card.due_date) and 
				(not editor or editor == card.editor) and
				(not reviewer or reviewer == card.reviewer) and
				(not scheduler or scheduler == card.scheduler) and
				(card.deleted or not deleted_only) and
				(not new_only or card.new) and
				(not pattern or bool(p.search(card.string)))) != # TODO invert
				invert)
		
		# matches.sort(key=lambda card: card.seen_date, reverse=True)
		return self.__class__([c for c in self if f(c)])
