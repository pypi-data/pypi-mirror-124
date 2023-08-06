""" Модуль содержит основной Singleton для работы. """

from qdk.main import QDK


class WServerQDK(QDK):
    """ Основной класс для взаимодействия с WServer """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_act(self, auto_id, gross, tare, cargo,
                time_in, time_out,
                carrier_id, trash_cat_id, trash_type_id,
                polygon_id, operator, ex_id):
        """
        Добавить новый акт на WServer.

        :param auto_id: ID автомобиля
        :param gross: Вес-брутто
        :param tare: Вес-тара
        :param cargo: Вес-нетто
        :param time_in: Время въезда
        :param time_out: Время выезда
        :param carrier_id: ID перевозчика
        :param trash_cat_id: ID категории груза
        :param trash_type_id: ID вида груза
        :param polygon_id: ID полигона
        :param operator: ID весовщика
        :param ex_id: ID записи в wdb
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_act', auto_id=auto_id, gross=gross, tare=tare,
                            cargo=cargo, time_in=time_in, time_out=time_out,
                            carrier_id=carrier_id, trash_cat_id=trash_cat_id,
                            trash_type_id=trash_type_id, polygon_id=polygon_id,
                            operator=operator, ex_id=ex_id)

    def get_auto_id(self, car_number: str):
        """
        Вернуть ID авто по его гос. номеру.

        :param car_number: гос.номер авто.
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('get_auto_id', car_number=car_number)

    def get_carrier_id(self, carrier_name: str):
        """
        Вернуть ID компании-перевозчика по его названию.

        :param carrier_name: название компании-перевозчика.
        :return:
        """
        self.execute_method('get_company_id', company_name=carrier_name)

    def set_photo(self, record_id: int, photo_obj: str, photo_type: int):
        """
        Сохранить фотографии на WServer.

        :param record_id: ID заезда, к которому относится фотография.
        :param photo_obj: Объект фото в кодировке base64, но в виде строки.
        :param photo_type: Тип фотографии (gdb.photo_types).
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_photos', record=record_id,
                            photo_obj=photo_obj, photo_type=photo_type)

    def set_operator(self, full_name: str, login: str, password: str,
                     polygon: int, active: bool = True):
        """
        Добавить нового весовщика.

        :param full_name: Полное имя весовщика (ФИО).
        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        :param polygon: ID полигона, за которым закреплен весовщик.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_operator', full_name=full_name, login=login,
                            password=password, polygon=polygon, active=active)

    def set_auto(self, car_number, polygon, id_type, rg_weight=None,
                 model=None, rfid_id=None):
        """
        Добавить новое авто.

        :param car_number: Гос. номер
        :param polygon: Полигон, за которым закреплено авто, если авто
            передвигается по всему региону, его стоит закрепить за РО.
        :param id_type: Протокол авто (rfid, NEG, tails)
        :param rg_weight: Справочный вес (тара)
        :param model: ID модели авто из gdb.auto_models
        :param rfid_id: ID RFID метки из gdb.rfid_marks
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_auto', car_number=car_number, polygon=polygon,
                            id_type=id_type, rg_weight=rg_weight, model=model,
                            rfid_id=rfid_id)

    def set_carrier(self, name, inn, kpp, polygon, status, active, ex_id=None):
        """
         Добавить нового перевозчика.

         :param name: Название перевозчика.
         :param inn: ИНН перевозчика.
         :param kpp: КПП перевозчика.
         :param ex_id: ID перевозичка из внешней системы. (1C, например)
         :param status: Действующий или нет? True/False
         :param polygon: ID полигона.
         :param active: Запись по умолчанию активна?
         :return:
             В случае успеха:
                 {'status': True, 'info': *id: int*)
             В случае провала:
                 {'status': False, 'info': Python Traceback}
         """
        self.execute_method('set_company', name=name, inn=inn, kpp=kpp,
                            polygon=polygon, status=status, ex_id=ex_id,
                            active=active)

    def set_operator_notes(self, record: int, note: str, note_type: int):
        """
        Добавить комментарии весовщика к заезду.

        :param record: ID заезда
        :param note: Комментарий
        :param note_type: Тип комментария (при брутто, добавочный и т.д.)
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_notes', record=record, note=note,
                            note_type=note_type)

    def set_trash_cat(self, name, polygon, active=True):
        """
          Добавить новую категорию груза.

          :param name: Название категории груза.
          :param polygon: ID полигона.
          :param active: Запись по умолчанию активна?
          :return:
              В случае успеха:
                  {'status': True, 'info': *id: int*)
              В случае провала:Отп
                  {'status': False, 'info': Python Traceback}
          """
        self.execute_method('set_trash_cat', name=name, polygon=polygon,
                            active=active)

    def set_trash_type(self, name: str, polygon: int, category: int = None,
                       active: bool = True):
        """
        Добавить новый вид груза.

        :param name: Название вида груза.
        :param category: ID категории груза, за которым этот вид закреплен.
        :param polygon: ID полигона.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('set_trash_type', name=name, polygon=polygon,
                            category=category, active=active)

    def get_rfid_id(self, rfid: str):
        """
        Вернуть ID RFID метки по его коду. (10 символов)

        :param rfid: последовательность условной длины, явяляющей частью номера
            RFID метки.
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        self.execute_method('get_rfid_id', rfid=rfid)

    def update_trash_cat(self, cat_id, polygon=None, name=None, active=True):
        """
        Обновить категорию груза.

        :param name: Новое имя категории груза.
        :param active: ID полигона, для которого вносятся изменения
        :param cat_id: ID категории груза, который нужно изменить..
        :return:
              В случае успеха:
                  {'status': True, 'info': *id: int*)
              В случае провала:Отп
                  {'status': False, 'info': Python Traceback}
        """
        self.execute_method('update_trash_cat', cat_id=cat_id, polygon=polygon,
                            new_name=name, active=active)

    def update_trash_type(self, type_id: int, polygon: int = None,
                          new_name: str = None, new_cat_id: int = None,
                          active: bool = True):
        """
        Обновить существующий вид груза.

        :param type_id: ID вида груза.
        :param polygon: Полигон, вид груза которого меняется.
        :param new_name: Новое название вида груза.
        :param new_cat_id: Новая категория для груза.
        :param active: Оставить запись активной?
        :return:
        """
        self.execute_method('update_trash_type', type_id=type_id,
                            polygon=polygon, new_name=new_name,
                            new_cat_id=new_cat_id, active=active)

    def update_auto(self, auto_id: int, new_car_num=None,
                    new_id_type=None, new_rg_weight=None,
                    new_model=None, new_rfid_id=None, active=True):
        """
        Обновить существующее авто.

        :param auto_id: ID автомобиля.
        :param new_car_num: Новый гос. номер.
        :param new_id_type: Новый вид протокола.
        :param new_rg_weight: Новый справочный вес.
        :param new_model: Новая модель.
        :param new_rfid_id: Новый ID метки.
        :param active: Активность записи.
        :return:
        """
        self.execute_method('update_auto', auto_id=auto_id,
                            new_car_number=new_car_num,
                            new_id_type=new_id_type,
                            new_rg_weight=new_rg_weight, new_model=new_model,
                            new_rfid_id=new_rfid_id, active=active)

    def update_company(self, company_id, name: str = None, inn: str = None,
                       kpp: str = None, polygon: int = None,
                       status: bool = None,
                       ex_id: str = None, active: bool = True):
        """
        Обновить компанию-перевозчика.

        :param company_id: ID компании перевозчика.
        :param name: Название компании.
        :param inn: ИНН компании.
        :param kpp: КПП компании.
        :param polygon: ID полигона.
        :param status: Статус компании.
        :param ex_id: ID компании из внешней среды.
        :param active: Активность записи.
        :return:
        """
        self.execute_method('update_company', company_id=company_id, name=name,
                            inn=inn, kpp=kpp, polygon=polygon, status=status,
                            ex_id=ex_id, active=active)

    def update_operator(self, operator_id: int, full_name: str = None,
                        login: str = None, password: str = None,
                        polygon: int = None, active: bool = True,
                        *args, **kwargs):
        """
        Обновить информацию о весовщике.

        :param operator_id: ID весовщика.
        :param full_name: Полное имя.
        :param login: Логин.
        :param password: Пароль.
        :param polygon: Полигон, за которым закреплен весовщик.
        :param active: Активность.
        :return:
        """
        self.execute_method('update_operator', operator_id=operator_id,
                            full_name=full_name, login=login, password=password,
                            polygon=polygon, active=active)

    def set_alerts(self, wserver_id: int, alerts: str):
        """
        Вставить алерты по записи в GDB.

        :param wserver_id: id акта, к котрому относятся алерты.
        :param alerts: Сами алерты в текстовом виде.
        :return:
        """
        self.execute_method('set_alerts', wserver_id=wserver_id, alerts=alerts)

    def check_legit(self, mac_addr: str):
        """Проверяет легитимность мак адреса AR"""
        self.execute_method('check_legit', mac_addr=mac_addr)

