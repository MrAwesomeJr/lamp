from update import Update
import datetime
import bisect


class Strip:
    def __init__(self, tickrate = 1, auto_delete_time = None):
        # buffer is a list of Updates
        self.buffer = []
        # mostly for importing ticks using bpm.
        self.tickrate = tickrate
        # automatically deletes items auto_delete_time older than the timestamp of the most recent call.
        self.auto_delete_time = auto_delete_time

        self._iterator_current_index = 0

    def __iter__(self):
        self._iterator_current_index = -1
        return self.buffer

    def __next__(self):
        if self._iterator_current_index < len(self.buffer):
            self._iterator_current_index += 1
            return self.buffer[self._iterator_current_index]
        else:
            return StopIteration

    def buffer_get_time(self, time):
        # return the update object at this time
        index = bisect.bisect_right(self.buffer, time, key=lambda update: update.timestamp) - 1
        return self.buffer[index]

    def buffer_get_tick(self, tick):
        # return the update object at this tick
        time = datetime.timedelta(seconds=tick/self.tickrate)
        return self.buffer_time(time)

    def add_update_on_time(self, timestamp, color):
        bisect.insort(self.buffer, Update(timestamp, color), key=lambda update: update.timestamp)
        self.clear()

    def add_update_on_time_delta(self, timestamp_delta, color):
        if len(self.buffer) > 0:
            timestamp = timestamp_delta + self.buffer[-1].timestamp
        else:
            timestamp = timestamp_delta

        self.add_update_on_time(timestamp, color)

    def add_update_on_tick(self, tick, color):
        timestamp = datetime.timedelta(seconds=tick/self.tickrate)
        self.add_update_on_time(timestamp, color)

    def add_update_on_tick_delta(self, tick_delta, color):
        timestamp_delta = tick_delta / self.tickrate
        self.add_update_on_time_delta(timestamp_delta, color)

    def get_timestamps(self):
        return (update.timestamp for update in self.buffer)

    def set_timestamp(self, timestamp):
        self.buffer_get_time(timestamp)

    def clear(self):
        # delete old values

        delete_time = self.buffer[self._iterator_current_index].timestamp - self.auto_delete_time

        if self.auto_delete_time is not None:
            for update in self.buffer:
                if update.timestamp < delete_time:
                    self.buffer.remove(update)
                    self._iterator_current_index -= 1
                else:
                    break
