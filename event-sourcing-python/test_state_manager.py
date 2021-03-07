
import uuid
from dataclasses import dataclass, field

import pytest

from state_manager import StateManager, MissingHandlerError

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


def test_statemanager():
    def get_default_state():
        """Return the default state of a new empty game"""
        return {
            "players": {},
        }
    manager = StateManager(get_default_state)

    @manager.handle(RegisterPlayer)
    def on_register(state, event):
        state['players'][event.player_id] = {
            "name": event.name,
        }

    @manager.handle(UnregisterPlayer)
    def on_unregister(state, event):
        state['players'].pop(event.player_id)

    assert "players" in manager.get()
    assert RegisterPlayer in manager.handlers
    assert UnregisterPlayer in manager.handlers

    manager.apply(RegisterPlayer(player_id="test", name="Mitch"))
    assert "test" in manager.get()['players']

    manager.apply(UnregisterPlayer(player_id="test"))
    assert "test" not in manager.get()['players']

    manager.undo()
    assert "test" in manager.get()['players']

    manager.reset()
    assert "test" not in manager.get()['players']


def test_statemanager_missing_handler():
    """
    Make sure StateManager raises an error if handlers are missing.
    """
    with pytest.raises(MissingHandlerError):
        StateManager(lambda: None).apply(UnregisterPlayer(player_id="404"))
