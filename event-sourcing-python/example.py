"""
    Example usage of the StateManager for Event Sourcing
"""

import uuid
from pprint import pprint
from dataclasses import dataclass, field

from state_manager import StateManager

#
# Events are just simple dataclasses which contains information.
# They should not contain logic at all.
#

@dataclass
class RegisterPlayer:
    """Registration of a new player in the game"""
    name: str
    player_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class UnregisterPlayer:
    """Player is leaving the game"""
    player_id: str


if __name__ == '__main__':
    def get_default_state():
        """Return the default state of a new empty game"""
        return {
            "players": {},
        }

    manager = StateManager(default_factory=get_default_state)

    @manager.handle(RegisterPlayer)
    def on_register(state, event):
        state['players'][event.player_id] = {
            "name": event.name,
        }

    @manager.handle(UnregisterPlayer)
    def on_unregister(state, event):
        state['players'].pop(event.player_id)


    manager.apply(RegisterPlayer(player_id="test", name="Mitch"))
    pprint(manager.get())

    manager.apply(UnregisterPlayer(player_id="test"))
    pprint(manager.get())

    manager.undo()
    pprint(manager.get())
