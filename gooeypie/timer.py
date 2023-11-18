import time


class Timer:
    def __init__(self):
        """Creates a new timer"""

        # Timestamp added for each start/pause of the timer
        self._ticks = []

    @property
    def time(self) -> float:
        """Returns the current value of the timer as float to the nearest ms"""
        current_time = time.time()
        if self._ticks:
            # Add the current time to the ticks list if the timer is not paused
            if not self.paused:
                ticks = self._ticks + [current_time]
            else:
                ticks = self._ticks

            # Loop over all start/pause times to find total time
            elapsed_time = 0
            for index in range(0, len(ticks), 2):
                elapsed_time += ticks[index + 1] - ticks[index]

            return round(elapsed_time, 3)
        else:
            return 0.0

    @property
    def hours(self) -> int:
        """Returns the integer number of hours elapsed"""
        return int(self.time // 3600)

    @property
    def minutes(self) -> int:
        """Returns the minutes component of the time elapsed as an integer between 0 and 59"""
        return int(self.time // 60 % 60)

    @property
    def seconds(self) -> int:
        """Returns the seconds component of the time elapsed as an integer between 0 and 59"""
        return int(self.time) % 60

    @property
    def milliseconds(self) -> int:
        """Returns the milliseconds component of the time elapsed as an integer between 0 and 999"""
        return int(self.time % 1 * 1000)

    @property
    def stopped(self) -> bool:
        """Returns whether the timer is stopped or not"""
        return len(self._ticks) == 0

    @property
    def paused(self) -> bool:
        """Returns whether the timer is paused or not. A stopped timer is not considered paused."""

        # An even number of ticks means that the timer is paused
        return not self.stopped and len(self._ticks) % 2 == 0

    def start(self):
        """Starts the timer or continues from paused. Has no effect if the timer is running."""
        current_time = time.time()
        if self.stopped or self.paused:
            self._ticks.append(current_time)

    def stop(self) -> None:
        """Stops the timer and resets the time elapsed"""
        self._ticks.clear()

    def pause(self) -> None:
        """Pauses the timer. Has no effect if the timer is stopped or already paused"""
        current_time = time.time()
        if not self.stopped and not self.paused:
            self._ticks.append(current_time)

    def restart(self) -> None:
        """Resets the time elapsed and restarts the timer"""
        current_time = time.time()
        self._ticks = [current_time]
