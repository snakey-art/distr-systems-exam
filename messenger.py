from general import *
from ntp import *

class Message:
    def __init__(self, time, src, dst, msg):
        self.time = Time()
        self.src = src
        self.dst = dst
        self.msg = msg

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst

    def get_msg(self):
        return self.msg

class MSGdb:
    def __init__(self):
        self.db = []

    def push_msg(self, msg : Message):
        self.db.append(msg)

    def get_messages_num(self):
        return len(self.db)

class MSGServerReplic(Service):
    def __init__(self):
        super().__init__()
        self.db = MSGdb()
        self.name = "MSGReplic"

    def input(self, packet : DataPacket):
        if (packet.get_service() == "rep_msg"):
            return self.push_msg(packet)
        if (packet.get_service() == "download_history"):
            return self.pull_history(packet)
        return

    def push_msg(self, packet):
        msg = Message(self.get_host().services["Timer"].time, packet.get_src(), packet.get_dst(), packet.get_data())
        self.db.push_msg(msg)

    def pull_history(self, packet):
        for x in range (len(self.db.db)):
            if ((self.db.db[x].get_src() == packet.get_src()) or (self.db.db[x].get_dst() == packet.get_src())):
                if (self.db.db[x].get_src == packet.get_src()):
                    addon = self.db.db[x].get_dst()
                    code = "201"
                addon = self.db.db[x].get_src()
                code = "202"
                self.get_host().interface.net.input(DataPacket(code, "msg_history", packet.get_dst(), packet.get_src(), self.db.db[x].get_msg(), addon))

class MSGServer(Service):
    def __init__(self):
        super().__init__()
        self.replic = []
        self.alive = []
        self.db = MSGdb()
        self.read_counter = 0
        self.name = "MSGServer"

    def input(self, packet : DataPacket):
        if (packet.get_service() == "msg_to_srv"):
            return self.get_msg(packet)
        if (packet.get_service() == "download_history"):
            return self.download_history(packet)
        return

    def add_replic(self, replic : MSGServerReplic):
        if not replic.get_host().interface.address:
            return "Cant add replic without net"
        self.replic.append(replic)

    def push_msg(self, packet):
        msg = Message(self.get_host().services["Timer"].time, packet.get_src(), packet.get_dst(), packet.get_data())
        self.db.push_msg(msg)
        for i in range (len(self.replic)):
            self.replic[i].push_msg(packet)

    def get_msg(self, packet):
        self.push_msg(packet)
        self.get_host().interface.net.input(DataPacket("200", "msg_to_dst", packet.get_src(), packet.get_dst(), packet.get_data()))

    def check_replic(self):
        self.alive.clear()
        for any in self.replic:
            if any.get_host().interface.net:
                self.alive.append(any)

    def download_history(self, packet):
        self.check_replic()
        if len(self.alive) < 1:
            self.pull_history(packet)
            return
        if self.read_counter > (len(self.alive) - 1):
            self.read_counter = self.read_counter - len(self.alive)
        self.alive[self.read_counter].input(DataPacket("300", "download_history", packet.get_src(), self.alive[self.read_counter].get_host().interface.address, None))

    def pull_history(self, packet):
        for x in range (len(self.db.db)):
            if ((self.db.db[x].get_src() == packet.get_src()) or (self.db.db[x].get_dst() == packet.get_src())):
                if (self.db.db[x].get_src == packet.get_src()):
                    addon = self.db.db[x].get_dst()
                    code = "201"
                addon = self.db.db[x].get_src()
                code = "202"
                self.get_host().interface.net.input(DataPacket(code, "msg_history", packet.get_dst(), packet.get_src(), self.db.db[x].get_msg(), addon))

class Messenger(Service):
    def __init__(self):
        super().__init__()
        self.name = "Messenger"
        self.db = MSGdb()
        self.msg_server = None
        self.history = MSGdb()

    def input(self, packet : DataPacket):
        if (packet.get_service() == "msg_to_dst"):
            self.get_msg(packet)
        if (packet.get_service() == "msg_history"):
            self.get_history(packet)
        return

    def set_msg_server(self, msg_server):
        self.msg_server = msg_server

    def send_msg(self, dst, data):
        if not self.msg_server:
            return "No connection"
        msg = Message(self.get_host().services["Timer"].time, self.get_host().interface.address, dst, data)
        self.db.push_msg(msg)
        return self.get_host().interface.net.input(DataPacket("200", "msg_to_srv", self.get_host().interface.address, dst, data, self.msg_server))

    def get_msg(self, packet):
        msg = Message(self.get_host().services["Timer"].time, packet.get_src(), packet.get_dst(), packet.get_data())
        self.db.push_msg(msg)

    def download_history(self):
        self.get_host().interface.net.input(DataPacket("300", "download_history", self.get_host().interface.address, self.msg_server, None, self.msg_server))

    def get_history(self, packet):
        if packet.get_opcode() == "201":
            msg = Message(self.get_host().services["Timer"].time, packet.get_dst(), packet.get_addon(), packet.get_data())
        msg = Message(self.get_host().services["Timer"].time, packet.get_addon(), packet.get_dst(), packet.get_data())
        self.history.push_msg(msg)
