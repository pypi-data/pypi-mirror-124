import datetime, time
import functools
TODAY = datetime.date.today()

# want to express this as a generator to be called in the individual generator files
def generator(g):
	# prserve wrapped functions name, docstring, and signature
	@functools.wraps(g)
	def wrapped_generator():
		start = time.time()
		new_cards = g()
		stop = time.time()
		elapsed = int(stop - start)
		for card in new_cards:
			card.make_string()
			card.add_history(TODAY, elapsed, 'create')
			card.load_metadata()  # TODO why do I need this?
		return new_cards[0]
	return wrapped_generator
