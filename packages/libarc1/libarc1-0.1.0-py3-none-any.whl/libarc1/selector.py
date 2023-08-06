import serial
import threading

"""
Selectors toggle IOs originating from outside the main ArC1 board with the
intend of toggling selector devices, typically MOSFETs. This is made with the
ArC1 selector board add-on in mind but custom implementations for custom
solutions should be relatively straightforward to code. libarc1 expects two
functions to be available `toggle_bitlines(*lines)` and `clear_bitlines()`. The
former toggles the selected lines and the latter disconnects all selectors.
"""

class NullSelector:
    """
    This is the default implementation of a selector, ie. no selector
    is connected. All functions are nop.
    """

    def __init__(self):
        pass

    def toggle_bitlines(self, *bitlines):
        pass

    def clear_bitlines(self):
        pass


class DefaultSelector:
    """
    The ArC1 selector board. This is typically connected to a differnt
    serial port than ArC1 and allows for up to 32 bitlines to be toggled
    at once.

    Arguments
    ---------
    Except for ``port`` most the arguments are set to sane default values.

    * ``port``: Where the add-on board is connected
    * ``maxbits``: The maximum number of bits supported. This is 32 and
      there should not be any reason to change it.
    * ``baud``: Baud rate of the serial port connection.
    * ``parity``: Parity of the serial port connection.
    * ``stop``: Number of stop bits.
    """

    def __init__(self, port, maxbits=32, baud=921600,
            parity=serial.PARITY_EVEN, stop=serial.STOPBITS_ONE):

        self.lock = threading.Lock()
        if not (maxbits & (maxbits-1) == 0):
            raise ValueError("Max bits must be a power of 2")
        self.maxbits=maxbits
        self._port = serial.Serial(port=port, baudrate=baud, timeout=7,
            parity=parity, stopbits=stop)

    def toggle_bitlines(self, *bitlines):
        """
        Toggles specified bitlines. These are arguments to the function and
        should not exceed the number of ``maxbits``. Arguments are 0-indexed.
        """
        # make a new zero bitmask
        mask = 0b0
        # set the relevant bits to 1
        for b in bitlines:
            if b >= maxbits:
                raise ValueError("Selected bit >=", self.maxbits)
            mask |= (1<<b)

        numbytes = int(self.maxbits/8)

        # send it to the uC
        with self.lock:
            self._port.write(mask.to_bytes(numbytes, byteorder='big'))

    def clear_bitlines(self):
        """
        Disconnect all bitlines.
        """
        mask = 0b0
        numbytes = int(self.maxbits/8)
        with self.lock:
            self._port.write(mask.to_bytes(numbytes, byteorder='big'))
