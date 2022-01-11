class DataPacket:
    def __init__(self, opcode, service, src, dst, data, addon = None):
        self.opcode = opcode
        self.service = service
        self.src = src
        self.dst = dst
        self.data = data
        self.addon = addon

    def get_opcode(self):
        return self.opcode

    def get_service(self):
        return self.service

    def get_src(self):
        return self.src

    def get_dst(self):
        return self.dst

    def get_data(self):
        return self.data

    def get_addon(self):
        return self.addon

class Service:
    def __init__(self):
        self.host = None
        self.name = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

class Computer:
    def __init__(self):
        self.interface = NetworkInterface(self)
        self.services = {}

    def input(self, packet : DataPacket):
        if (packet.get_service() == "msg_to_srv"):
            return self.services["MSGServer"].input(packet)
        if (packet.get_service() == "msg_to_dst"):
            return self.services["Messenger"].input(packet)
        if (packet.get_service() == "download_history"):
            return self.services["MSGServer"].input(packet)
        if (packet.get_service() == "msg_history"):
            return self.services["Messenger"].input(packet)
        return

    def ping(self, address):
        return self.interface.input(DataPacket("300", "ping", "localhost", "NET", address))

    def resolve(self, name):
        return self.interface.input(DataPacket("300", "resolve", "localhost", self.interface.address, name)).get_data()

    def get_service(self, service : Service):
        self.services[service.get_name()] = service

class NetworkInterface:
    def __init__(self, computer : Computer):
        self.net = None
        self.address = None
        self.dns = None
        self.computer = computer

    def input(self, packet : DataPacket):
        if (packet.get_service() == "set_net"):
            return self.set_net(packet.get_data(), packet.get_addon())
        if (packet.get_service() == "disconnect"):
            return self.disconnect()
        if (packet.get_service() == "ping"):
            if not self.net:
                return "No network"
            return self.net.input(DataPacket("300", "ping", self.address, "NET", packet.get_data()))
        if (packet.get_service() == "resolve"):
            if not self.net:
                return "No network"
            return self.net.input(DataPacket("300", "resolve", self.address, "NET", packet.get_data()))
        return

    def set_net(self, net, address):
        if self.net:
            self.disconnect()
        self.net = net
        self.address = address

    def get_dns(self):
        if not self.net:
            return "No network"
        self.dns = self.net.input(DataPacket("300", "get_dns", self.address, "NET", None)).get_data()

    def disconnect(self):
        if self.net:
            self.net.input(DataPacket("300", "delete_host", self.address, "NET", self.address))
        self.net = None
        self.address = None

class Network:
    def __init__(self):
        self.hosts = {}
        self.logs = []
        self.dns = "8.8.8.8"
        self.ntp = None

    def input(self, packet : DataPacket):
        self.logs.append(packet)
        if (packet.get_service() == "delete_host"):
            return self.delete_host(packet.get_data())
        if (packet.get_service() == "ping"):
            return DataPacket("200", "pong", "NET", packet.get_src(), self.ping(packet.get_data()))
        if (packet.get_service() == "get_dns"):
            return DataPacket("200", "get_dns", "NET", packet.get_src(), self.dns)
        if (packet.get_service() == "resolve"):
            return DataPacket("200", "resolved", "NET", packet.get_src(), self.resolve(packet.get_data(), self.dns))
        if (packet.get_service() == "add_host"):
            return self.add_host(packet.get_data(), packet.get_addon())
        if (packet.get_service() == "get_time"):
            return self.get_time()
        if (packet.get_service() == "msg_to_srv"):
            if not packet.get_addon() in self.hosts:
                return DataPacket("500", "msg_to_dst", "NET", self.get_src(), "No connection")
            self.hosts[packet.get_addon()].input(packet)
        if (packet.get_service() == "msg_to_dst"):
            if not packet.get_dst() in self.hosts:
                return "Unknown host"
            self.hosts[packet.get_dst()].input(packet)
        if (packet.get_service() == "download_history"):
            if not packet.get_addon() in self.hosts:
                return DataPacket("500", "msg_to_dst", "NET", self.get_src(), "No connection")
            self.hosts[packet.get_addon()].input(packet)
        if (packet.get_service() == "msg_history"):
            self.hosts[packet.get_dst()].input(packet)
        return

    def delete_host(self, address):
        if address in self.hosts:
            self.hosts[address].interface.net = None
            self.hosts[address].interface.address = None
            self.hosts.pop(address)

    def add_host(self, comp : Computer, address):
        if address in self.hosts:
            return "Busy address"
        self.hosts[address] = comp
        comp.interface.input(DataPacket("300", "set_net", "NET", comp.interface.address, self, address))

    def ping(self, address):
        if address in self.hosts:
            return "PONG"
        return "Unknown host"

    def resolve(self, address, dns):
        if not dns:
            return "Unknown host"
        if (self.hosts[dns].services["DNS_SERVER"].input(DataPacket("300", "resolve", "NET", dns, address)).get_opcode() == "305"):
            return self.resolve(address, self.hosts[dns].services["DNS_SERVER"].input(DataPacket("300", "resolve", "NET", dns, address)).get_data())
        return self.hosts[dns].services["DNS_SERVER"].input(DataPacket("300", "resolve", "NET", dns, address)).get_data()

    def set_ntp(self, ntp):
        self.ntp = ntp

    def get_time(self):
        if not self.ntp:
            return DataPacket("500", "time_is", "NET", "NET", "X", "X")
        return self.hosts[self.ntp].services["NTP_SERVER"].input(DataPacket("300", "get_time", "NET", self.ntp, None))
