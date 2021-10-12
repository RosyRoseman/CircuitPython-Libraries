"""
Example Call
buttons = {'silver':board.A0, 'blue':board.A1, 'red':board.A2}
for key in buttons: buttons[key] = Debouncer(buttons[key])
while True:
    for key in buttons: buttons[key].update()
"""

import time
import board
from micropython import const
from microcontroller import Pin
import digitalio

_DEBOUNCED_STATE = const(0x01)  # 001 Boolean Flag on first bit
_UNSTABLE_STATE = const(0x02)   # 010 Boolean Flag on second bit
_CHANGED_STATE = const(0x04)    # 100 Boolean Flag on third bit

# Find out whether the current CircuitPython really supports time.monotonic_ns(),
# which doesn't have the accuracy limitation.
try:
    time.monotonic_ns()
    TICKS_PER_SEC = 1_000_000_000
    MONOTONIC_TICKS = time.monotonic_ns
except (AttributeError, NotImplementedError):
    TICKS_PER_SEC = 1
    MONOTONIC_TICKS = time.monotonic


class Debouncer:
    """Debounce an input pin or an arbitrary predicate"""

    def __init__(self, io_or_predicate, interval=0.010, l_p_interval=1.100, r_interval=0.800):
        """Make an instance.
        :param DigitalInOut/function io_or_predicate: the DigitalIO or function to debounce
        :param int interval: bounce threshold in seconds (default is 0.010, i.e. 10 milliseconds)
        :param int l_p_interval: short_press < l_p_interval < long_press (default is 1.1 second)
        :param int r_interval: how long it will look for consecutive presses before updating (default is .8 seconds)
        """
        self.state = 0x00  # 000
        # If you've simply passed a pin name
        # Button should connect board.pin to ground
        if type(io_or_predicate) is Pin:
            io = digitalio.DigitalInOut(io_or_predicate)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.UP
            io_or_predicate = lambda: io.value
        # if object is digital_in_out object
        if hasattr(io_or_predicate, "value"):
            self.function = lambda: io_or_predicate.value
        # if some other bouncing function
        else:  # is some other bouncing function
            self.function = io_or_predicate
        if self.function():
            self._set_state(_DEBOUNCED_STATE | _UNSTABLE_STATE)  # set DEBOUNCED and UNSTABLE flags
        self._last_bounce_ticks = 0
        self._last_duration_ticks = 0
        self._state_changed_ticks = 0
        self._short_press = 0
        self.short_press_buffer = 0
        self._long_press = 0
        self.long_press_buffer = 0
        self._interval_ticks = interval * TICKS_PER_SEC
        self._long_press_interval_ticks = l_p_interval * TICKS_PER_SEC
        self._rest_interval_ticks = r_interval * TICKS_PER_SEC

    def _set_state(self, bits):  # OR 010 + 011 = 011
        self.state |= bits      # SET Flag(bits) True

    def _unset_state(self, bits):  # and not 010 + 011 = 110
        self.state &= ~bits       # SET Flag(bits) False

    def _toggle_state(self, bits):  # xor 010 + 011 = 001
        self.state ^= bits         # SET Flag(bits) NOT Flag(bits)

    def _get_state(self, bits):  # ???? Maybe returns bool from bit?
        return (self.state & bits) != 0  # Return True IF Flag(bits)

    def update(self):
        """Update the debouncer state. MUST be called frequently"""
        now_ticks = MONOTONIC_TICKS()                                  # Sets the NOW var
        self._unset_state(_CHANGED_STATE)                              # SET _changed_state flag False
        current_state = self.function()                                # get state of button
        if current_state != self._get_state(_UNSTABLE_STATE):          # IF still bouncing
            self._last_bounce_ticks = now_ticks                        # record ticks since last bouncing
            self._toggle_state(_UNSTABLE_STATE)                        # toggle _unstable_flag (to match current_state)
        else:                                                          # IF NOT BOUNCING:
            if now_ticks - self._last_bounce_ticks >= self._interval_ticks:  # IF stable for INTERVAL
                if current_state != self._get_state(_DEBOUNCED_STATE):  # IF button state != last_stable_state e.g. state changed
                    if current_state: # if button just released
                        if now_ticks - self._state_changed_ticks >= self._long_press_interval_ticks: #  if time held > _l_p__t
                            self.long_press_buffer += 1
                        else: # else time held was less than _long_press_interval_ticks
                            self.short_press_buffer += 1
                    self._last_bounce_ticks = now_ticks                # record ticks since last bouncing
                    self._toggle_state(_DEBOUNCED_STATE)               # match _DEBOUNCED_STATE Flag to button State
                    self._set_state(_CHANGED_STATE)                    # set _CHANGED_STATE Flag to True
                    self._last_duration_ticks = now_ticks - self._state_changed_ticks  # set time since change before last
                    self._state_changed_ticks = now_ticks              # set time since changed to current
                elif current_state and (self.short_press_buffer | self.long_press_buffer): # if button released AND short or long buffer exists
                    if now_ticks - self._state_changed_ticks >= self._rest_interval_ticks: # if no further presses (rest interval has passed)
                        # dump buffer to outward facing variable and empty buffer
                        self._short_press = self.short_press_buffer
                        self.short_press_buffer = 0
                        self._long_press = self.long_press_buffer
                        self.long_press_buffer = 0

    @property
    def interval(self):
        return self._interval_ticks / TICKS_PER_SEC

    @interval.setter
    def interval(self, new_interval_s):
        self._interval_ticks = new_interval_s * TICKS_PER_SEC

    @property
    def long_press_interval(self):
        return self._long_press_interval_ticks / TICKS_PER_SEC

    @long_press_interval.setter
    def long_press_interval(self, new_l_p_i):
        self._long_press_interval_ticks = new_l_p_i * TICKS_PER_SEC

    @property
    def r_interval(self):
        return self._r_interval_ticks / TICKS_PER_SEC

    @r_interval.setter
    def r_interval(self, new_r_i):
        self._r_interval_ticks = new_r_i * TICKS_PER_SEC

    @property
    def value(self):
        """Return the current debounced value."""
        return self._get_state(_DEBOUNCED_STATE)

    @property
    def rose(self):
        """Return whether the debounced value went from low to high at the most recent update."""
        return self._get_state(_DEBOUNCED_STATE) and self._get_state(_CHANGED_STATE)

    @property
    def fell(self):
        """Return whether the debounced value went from high to low at the most recent update."""
        return (not self._get_state(_DEBOUNCED_STATE)) and self._get_state(
            _CHANGED_STATE
        )

    @property
    def long_press(self):
        val = self._long_press
        self._long_press = 0
        return val

    @property
    def short_press(self):
        val = self._short_press
        self._short_press = 0
        return val

    @property
    def last_duration(self):
        """Return the number of seconds the state was stable prior to the most recent transition."""
        return self._last_duration_ticks / TICKS_PER_SEC

    @property
    def current_duration(self):
        """Return the number of seconds since the most recent transition."""
        return (MONOTONIC_TICKS() - self._state_changed_ticks) / TICKS_PER_SEC
