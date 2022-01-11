from general import *
import unittest

class TestComputer(unittest.TestCase):
    """Тест: адрес компьютера"""
    def test_ip(self):
        comp = Computer()
        net = Network()
        net.add_host(comp, "172.10.10.1")
        result = comp.interface.address
        self.assertEqual(result, "172.10.10.1")

    """Тест: пинг без сети"""
    def test_ping_without_net(self):
        comp = Computer()
        result = comp.ping("172.10.10.10")
        self.assertEqual(result, "No network")

    """Тест: пинг"""
    def test_ping(self):
        comp1 = Computer()
        comp2 = Computer()
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        net.add_host(comp2, "172.10.10.2")
        result = comp1.ping("172.10.10.2").get_data()
        self.assertEqual(result, "PONG")

class TestNetworkInterface(unittest.TestCase):
    """Тест: адрес компьютера"""
    def test_set_net(self):
        comp = Computer()
        net = Network()
        address = "1.2.3.4"
        comp.interface.set_net(net, address)
        result = comp.interface.address
        self.assertEqual(result, "1.2.3.4")

    """Тест: установить DNS сервер"""
    def test_set_dns(self):
        comp = Computer()
        net = Network()
        net.add_host(comp, "172.10.10.1")
        comp.interface.get_dns()
        result = comp.interface.dns
        self.assertEqual(result, "8.8.8.8")

    """Тест: отключение от сети"""
    def test_disconnect(self):
        comp = Computer()
        net = Network()
        net.add_host(comp, "172.10.10.1")
        result = comp.interface.address
        self.assertEqual(result, "172.10.10.1")
        comp.interface.disconnect()
        result = comp.interface.address
        self.assertEqual(result, None)

    """Тест: получение DNS из сети без сети"""
    def test_get_dns_without_net(self):
        comp = Computer()
        result = comp.interface.get_dns()
        self.assertEqual(result, "No network")

class TestNetwork(unittest.TestCase):
    """Тест: количество хостов в сети"""
    def test_hosts_num(self):
        comp1 = Computer()
        comp2 = Computer()
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        net.add_host(comp2, "172.10.10.2")
        result = len(net.hosts)
        self.assertEqual(result, 2)
        comp3 = Computer()
        net.add_host(comp3, "172.10.10.3")
        result = len(net.hosts)
        self.assertEqual(result, 3)

    """Тест: добавление компьютера с занятым адресом"""
    def test_busy_address(self):
        comp1 = Computer()
        comp2 = Computer()
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        result = net.add_host(comp2, "172.10.10.1")
        self.assertEqual(result, "Busy address")

    """Тест: повторное добавление компьютера с другим адресом"""
    def test_rewrite_address(self):
        comp = Computer()
        net = Network()
        net.add_host(comp, "172.10.10.1")
        net.add_host(comp, "172.10.10.2")
        result = comp.interface.address
        self.assertEqual(result, "172.10.10.2")
        result = len(net.hosts)
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
