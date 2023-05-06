import psycopg2
from abc import ABC, abstractmethod
from config.pg_config import dbname, user, password, host, port


class DBConnector(ABC):
    """Абстрактный класс подключения к БД"""
    @abstractmethod
    def __init__(self) -> None:
        """Абстракция инициализации"""
        pass

    @abstractmethod
    def connect(self) -> None:
        """Абстракция подключения к БД"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Абстракция отключения от БД"""
        pass


class PGDBBaseConnector(DBConnector):
    """Класс подключения к БД PostgreSQL"""
    __slots__ = ('dbname', 'user', 'password', 'host', 'port', 'conn', 'cur')

    def __init__(self,
            dbname: str = dbname,
            user: str = user,
            password: str = password,
            host: str = host,
            port: int = port,
    ) -> None:
        """Инициализация. Данные для подключения к БД"""
        self.dbname = dbname
        self.user = user
        self.__password = password
        self.host = host
        self.port = port

    def connect(self) -> None:
        """Устанавливает соединение с БД PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.__password,
                host=self.host,
                port=self.port
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except psycopg2.Error as _ex:
            print(f"Ошибка подключения к БД: {_ex}")

    def disconnect(self) -> None:
        """Закрывает соединение с БД PostgreSQL"""
        if self.conn:
            self.cur.close()
            self.conn.close()
