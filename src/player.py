from enum import Enum
class PlayerState(Enum):
	UNKNOWN = 1
	PLAYING = 2
	FOLD = 3
	UNACTIVE = 4

class Player:
	name = "Name"
	state = PlayerState.UNKNOWN
	capital = 0
	bounding_rect = None

	def __str__(self):
		return (self.name + " (state: " + str(self.state.name) + "):\nCapital: " + str(self.capital))
