from general import *

class DNSRecord:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

class Database:
    def __init__(self):
        self.records = {}

    def add_record(self, record : DNSRecord):
        if self.check_record(record.get_name()):
            self.delete_record(record.get_name())
        self.records[record.get_name()] = record.get_address()

    def delete_record(self, name):
        if self.check_record(name):
            return self.records.pop(name)
        return "No record"

    def num_records(self):
        return len(self.records)

    def resolve(self, name):
        if name in self.records:
            return self.records[name]
        return False

    def check_record(self, name):
        if name in self.records:
            return True
        return False

    def form_record(self, name, address):
        if name in self.records:
            self.delete_record(name)
        self.records[name] = address

class DNSRecursive(Service):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dns = None
        self.set_name("DNS_SERVER")

    def input(self, packet: DataPacket):
        if (packet.get_service() == "resolve"):
            return self.resolve(packet.get_data())
        return

    def set_dns(self, address):
        self.dns = address

    def resolve(self, name):
        if not self.db.resolve(name):
            return self.find(name)
        return DataPacket("200", "resolved", self.get_host().interface.address, "NET", self.db.resolve(name))

    def find(self, name):
        if not self.dns:
            return DataPacket("500", "resolved", self.get_host().interface.address, "NET", "Unknown host")
        return self.get_host().interface.net.hosts[self.dns].services["DNS_SERVER"].resolve(name)

class DNSNonRecursive(Service):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dns = None
        self.set_name("DNS_SERVER")

    def input(self, packet: DataPacket):
        if (packet.get_service() == "resolve"):
            return self.resolve(packet.get_data())
        return

    def set_dns(self, address):
        self.dns = address

    def resolve(self, name):
        if not self.db.resolve(name):
            return DataPacket("305", "resolved", self.get_host().interface.address, "NET", self.dns)
        return DataPacket("200", "resolved", self.get_host().interface.address, "NET", self.db.resolve(name))
