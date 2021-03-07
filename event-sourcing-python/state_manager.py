"""
    Event Sourcing State Manager
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    A state manager processes events and at each steps calculates the
    new state to be used for the system.

    The event processing logic is separated from the data objects,
    as different consumers might process data differently.
"""


class MissingHandlerError(KeyError):
    """
    Error thrown when trying to apply events without a defined handler.

    Depending on your use case, ignoring events can be sometimes valid.
    In this case, only ever call apply() with one event,
    and then catch and ignore this exception type.
    """


class StateManager:
    """
    Manages the computated state of a stream of events.
    """

    def __init__(self, default_factory, handlers=None):
        """
        Initialize this state.

        :param default_factory: Function which returns the initial state
        :param handler: Optional mapping of handlers (will be cloned)
        """
        self.default_factory = default_factory
        self.handlers = dict(handlers) if handlers else {}

        self.state = default_factory()
        self.history = []

    def reset(self):
        """
        Reset this manager to it's initial state.
        """
        self.state = self.default_factory()
        self.history = []

    def handle(self, event_class):
        """
        Decorator: Register an handler function for an event class.

        The registered method will receive (state, event) as arguments.
        The state can be modified in-place, no return value is expected.

        Only exactly one function can be registered for an event type,
        additional calls will override the previously defined handler.
        """
        def decorator(func):
            self.handlers[event_class] = func
            return func
        return decorator

    def apply(self, *events):
        """
        Apply one or more events to the internal state.
        All events are being added to the internal history.
        """
        for event in events:
            if event.__class__ not in self.handlers:
                raise MissingHandlerError(event.__class__.__name__)

            self.handlers[event.__class__](self.state, event)
            self.history.append(event)

    def undo(self, count=1):
        """
        Convenience method to undo previous events.

        This is done by resetting the state, then re-applying all events
        except the last {count} ones.
        """
        assert count >= 1, "count must be 1 or higher"
        events = self.history[:-count]
        self.reset()
        self.apply(*events)

    def get(self):
        """
        Returns the internal state.

        The resulting object MUST NOT be modified.
        """
        return self.state
