from general import *
from dns import *
import unittest

class TestDns(unittest.TestCase):
    """Тест: записи в пустой базе данных"""
    def test_empty_dns(self):
        d1 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        d1.set_host(cd1)
        result = d1.db.num_records()
        self.assertEqual(result, 0)

    """Тест: добавление запись в базу данных"""
    def test_add_dns_record(self):
        d1 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        d1.set_host(cd1)
        d1.db.form_record("ya.ru", "10.20.30.40")
        result = d1.db.num_records()
        self.assertEqual(result, 1)

    """Тест: удаление записи из базы данных"""
    def test_delete_dns_record(self):
        d1 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        d1.set_host(cd1)
        d1.db.form_record("ya.ru", "10.20.30.40")
        result = d1.db.num_records()
        self.assertEqual(result, 1)
        d1.db.delete_record("ya.ru")
        result = d1.db.num_records()
        self.assertEqual(result, 0)

    """Тест: резолв имени из пустых баз данных рекурсивно"""
    def test_resolve_blank_dns_recursive(self):
        comp1 = Computer()
        d1 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        d2 = DNSRecursive()
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        result = comp1.resolve("any")
        self.assertEqual(result, "Unknown host")

    """Тест: резолв имени из первой базы данных рекурсивно"""
    def test_resolve_1st_dns_recursive(self):
        comp1 = Computer()
        d1 = DNSRecursive()
        d2 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        d1.db.form_record("google.com", "1.2.3.4")
        result = comp1.resolve("google.com")
        self.assertEqual(result, "1.2.3.4")

    """Тест: резолв имени из второй базы данных рекурсивно"""
    def test_resolve_2nd_dns_recursive(self):
        comp1 = Computer()
        d1 = DNSRecursive()
        d2 = DNSRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        d2.db.form_record("google.com", "1.2.3.4")
        result = comp1.resolve("google.com")
        self.assertEqual(result, "1.2.3.4")

    """Тест: резолв имени из пустых баз данных нерекурсивно"""
    def test_resolve_blank_dns_nonrecursive(self):
        comp1 = Computer()
        d1 = DNSNonRecursive()
        d2 = DNSNonRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        result = comp1.resolve("any")
        self.assertEqual(result, "Unknown host")

    """Тест: резолв имени из первой базы данных нерекурсивно"""
    def test_resolve_1st_dns_nonrecursive(self):
        comp1 = Computer()
        d1 = DNSNonRecursive()
        d2 = DNSNonRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        d1.db.form_record("google.com", "1.2.3.4")
        result = comp1.resolve("google.com")
        self.assertEqual(result, "1.2.3.4")

    """Тест: резолв имени из второй базы данных нерекурсивно"""
    def test_resolve_2nd_dns_nonrecursive(self):
        comp1 = Computer()
        d1 = DNSNonRecursive()
        d2 = DNSNonRecursive()
        d1.set_dns("8.8.4.4")
        cd1 = Computer()
        cd1.get_service(d1)
        cd2 = Computer()
        cd2.get_service(d2)
        d1.set_host(cd1)
        d2.set_host(cd2)
        net = Network()
        net.add_host(comp1, "172.10.10.1")
        comp1.interface.get_dns()
        net.add_host(cd1, "8.8.8.8")
        net.add_host(cd2, "8.8.4.4")
        d2.db.form_record("google.com", "1.2.3.4")
        result = comp1.resolve("google.com")
        self.assertEqual(result, "1.2.3.4")


if __name__ == '__main__':
    unittest.main()
