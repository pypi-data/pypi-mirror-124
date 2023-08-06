""" Тесты основного класса. """

import unittest
from wserver_qdk.main import WServerQDK
from wserver_qdk import tools
import uuid


class MainTest(unittest.TestCase):
    """ Test Case """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qdk = WServerQDK('192.168.100.118', 8888, login='Test1',
                              password='jupiter3')
        self.qdk.make_connection()
        result = self.qdk.make_auth()
        result = self.qdk.get_data()
        print('auth_result', result)
        self.qdk.make_connection()

    def test_set_act(self):
        self.qdk.set_act(auto_id=102150, gross=5000, tare=3000, cargo=2000,
                         time_in='2021.08.24 13:44:13',
                         time_out='2021.08.24 14:33:31',
                         carrier_id=507970, trash_cat_id=36,
                         trash_type_id=12,
                         polygon_id=9, operator=22, ex_id=127)
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))

    def test_get_auto_id(self):
        self.qdk.get_auto_id(car_number='В060ХА702')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))
        self.qdk.get_auto_id(car_number='0101010101')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and not response['info'])

    def test_get_carrier_id(self):
        """ Вернуть ID перевозчика """
        self.qdk.get_carrier_id(carrier_name='test_company_1')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))
        self.qdk.get_carrier_id(carrier_name='0')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and not response['info'])

    def test_set_photo(self):
        photo_obj = tools.encode_photo('test_act_photo.png')
        self.qdk.set_photo(record_id=784663, photo_obj=str(photo_obj),
                           photo_type=1)
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))

    def test_set_operator(self):
        self.qdk.set_operator('FULLNAME', 'someLogin', 'somePassword', 9)
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))

    def test_set_auto(self):
        random_car_num = str(uuid.uuid4())[:9]
        self.qdk.set_auto(car_number=random_car_num, polygon=9,
                          id_type='tails')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info'], int))
        self.qdk.set_auto(car_number=random_car_num, polygon=9,
                          id_type='tails')
        response = self.qdk.get_data()
        self.assertTrue(not response['info']['status'])

    def test_set_carrier(self):
        self.qdk.set_carrier('test_carrier_n', inn='123', kpp='456',
                             polygon=9,
                             status=True, active=True, ex_id=None)
        response = self.qdk.get_data()
        self.assertTrue(response['status'])

    def test_set_operator_notes(self):
        self.qdk.set_operator_notes(record=784663,
                                    note='TEST_COMM_FROM_QDK',
                                    note_type=1)
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info']['info'], int))

    def test_set_trash_cat(self):
        random_name = str(uuid.uuid4())[:10]
        self.qdk.set_trash_cat(name=random_name, polygon=9, active=False)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'] and
                        isinstance(response['info']['info'], int))
        self.qdk.set_trash_cat(name=random_name, polygon=9, active=False)
        response = self.qdk.get_data()
        self.assertTrue(not response['info']['status'])

    def test_set_trash_type(self):
        random_name = str(uuid.uuid4())[:10]
        self.qdk.set_trash_type(name=random_name, category=None, polygon=9)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'] and
                        isinstance(response['info']['info'], int))

    def test_get_rfid_num(self):
        self.qdk.get_rfid_id(rfid='FFFF000160')
        response = self.qdk.get_data()
        self.assertTrue(response['status'] and
                        isinstance(response['info'], int))
        self.qdk.get_rfid_id(rfid='a00240sf')
        response = self.qdk.get_data()
        self.assertTrue(not response['info'])

    def test_update_trash_cat(self):
        self.qdk.update_trash_cat(cat_id=4, name='Прочее_Изм')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_cat(cat_id=4, active=False)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_cat(cat_id=4, active=True)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_cat(cat_id=4, polygon=0)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_cat(cat_id=4, name='Прочее', active=True)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])

    def test_update_trash_type(self):
        self.qdk.update_trash_type(type_id=3, polygon=0)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_type(type_id=3, new_name='Пэт_изм')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_type(type_id=3, new_cat_id=35)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_type(type_id=3, active=False)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_trash_type(type_id=3, new_name='Пэт', new_cat_id=4,
                                   active=True)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])

    def test_update_auto(self):
        self.qdk.update_auto(auto_id=623481, new_car_num='В2')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_auto(auto_id=623481, new_id_type='rfid')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_auto(auto_id=623481, active=False)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_auto(auto_id=623481, new_rg_weight=100)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])
        self.qdk.update_auto(auto_id=623481, new_car_num='ТЕСТ1337',
                             new_id_type='tails', active=True,
                             new_rg_weight=0)
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])

    def test_update_company(self):
        self.qdk.update_company(company_id=507994, name='test_company_izm')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])

    def test_update_operator(self):
        self.qdk.update_operator(22, full_name='Гульнара ФО')
        response = self.qdk.get_data()
        self.assertTrue(response['info']['status'])


if __name__ == '__main__':
    unittest.main()