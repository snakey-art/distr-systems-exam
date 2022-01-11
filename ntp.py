from general import *

class Time:
    def __init__(self):
        self.hours = 0
        self.minutes = 0

    def set_hours(self, hours):
        self.hours = hours

    def set_minutes(self, minutes):
        self.minutes = minutes

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def tick_minutes(self):
        self.minutes = self.minutes + 1
        if (self.minutes > 59):
            self.minutes = self.minutes - 60
            self.tick_hours()

    def tick_hours(self):
        self.hours = self.hours + 1
        if (self.hours > 23):
            self.hours = self.hours - 24

class NTPServer(Service):
    def __init__(self):
        super().__init__()
        self.time = Time()
        self.set_name("NTP_SERVER")

    def input(self, packet: DataPacket):
        if (packet.get_service() == "get_time"):
            return DataPacket("200", "time_is", self.get_host().interface.address, "NET", self.get_time().get_hours(), self.get_time().get_minutes())
        return

    def tick(self):
        self.time.tick_minutes()

    def big_tick(self):
        self.time.tick_hours()

    def get_time(self):
        return self.time

class Timer(Service):
    def __init__(self):
        super().__init__()
        self.ntp = None
        self.set_name("Timer")
        self.time = Time()

    def get_ntp(self):
        if not self.get_host().interface.net:
            return DataPacket("500", "time_is", "localhost", "localhost", "X", "X")
        self.ntp = self.get_host().interface.net.ntp
        self.get_time()

    def get_time(self):
        if not self.ntp:
            self.time.set_hours("X")
            self.time.set_minutes("X")
            return DataPacket("500", "time_is", "localhost", "localhost", "X", "X")
        self.time.set_hours(self.get_host().interface.net.input(DataPacket("300", "get_time", self.get_host().interface.address, "NET", None)).get_data())
        self.time.set_minutes(self.get_host().interface.net.input(DataPacket("300", "get_time", self.get_host().interface.address, "NET", None)).get_addon())
        return self.get_host().interface.net.input(DataPacket("300", "get_time", self.get_host().interface.address, "NET", None))
