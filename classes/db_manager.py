from classes.db_connector import PGDBBaseConnector
from abc import ABC, abstractmethod


class PGDBManager(ABC):
    """Аббстрактный класс работы с БД PostgreSQL"""
    @abstractmethod
    def __init__(self) -> None:
        """Абстракция инициализации"""
        pass

    @abstractmethod
    def adhoc_query(self, query) -> list:
        """Абстракция свободный SQL-запрос"""
        pass


class PGDBSamoletManager(PGDBManager):
    """Класс работы с БД PostgreSQL - схема samolet"""
    __slots__ = ('connection', 'query')

    def __init__(self, connection: PGDBBaseConnector) -> None:
        """Инициализация. Объект класса PGDBBaseConnector (подключение к БД)"""
        self.connection = connection

    def adhoc_query(self, query: str) -> list:
        """Возвращает список кортежей (строки из БД) по введенному SQL-запросу"""
        self.connection.connect()
        self.connection.cur.execute(query)
        result = self.connection.cur.fetchall()
        self.connection.disconnect()

        return result

    def group_insert(self, data: str) -> None:
        """
        Групповая вставка данных в таблицу samolet.flats.
        Формат data - строка в виде кортежей через ','
        """
        self.connection.connect()
        self.connection.cur.execute(
            f"""
            INSERT INTO samolet.flats(
              flat_id
            , project_name
            , floor_number
            , total_floors
            , flat_url
            , rooms_cnt
            , base_price
            , clean_price
            , delivery_date
            , flat_area
            )
            VALUES {data};
            """
        )
        self.connection.disconnect()
