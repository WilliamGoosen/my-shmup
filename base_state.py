class BaseState:
    """
    A base class for all game states. This defines the interface that
    the main game loop will use to interact with any state.
    """
    def __init__(self, game):
        # A reference to the main game object, which holds all the managers and resources
        self.game = game
        # Flag to tell the game loop that this state is finished and we should switch
        self.done = False
        # The name of the next state to switch to when this state is done
        self.next_state = None
        # Flag to indicate the game should quit entirely
        self.quit = False
        # State to return to after special transitions
        self.return_state = None

    def startup(self):
        """
        Called exactly once when the state becomes active.
        Use this for initializing state-specific data.
        """
        self.done = False
        self.next_state = None
        self.quit = False

    def get_event(self, event):
        """
        Handle a single event from the event loop.
        :param event: A pygame event object (e.g., KEYDOWN, MOUSEBUTTONDOWN).
        """
        pass

    def update(self, dt):
        """
        Update the state's logic.
        :param dt: Delta time (time since last frame) in seconds.
        """
        pass

    def draw(self, surface):
        """
        Draw everything in the state to the given surface.
        :param surface: The pygame Surface to draw onto (usually the screen).
        """
        pass