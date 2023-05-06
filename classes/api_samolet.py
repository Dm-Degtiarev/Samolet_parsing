import requests
from abc import ABC, abstractmethod
from datetime import datetime, date


class SamoletAPI(ABC):
    """Абстрактный класс взаимодействия с samolet API"""
    @abstractmethod
    def __init__(self) -> None:
        """Абстракция инициализации"""
        pass

    @abstractmethod
    def get_request(self) -> dict:
        """Абстракция получения данных по API"""
        pass


class SamoletAPIGetProjects(SamoletAPI):
    """Класс получения информации о проектах строительства"""
    __slots__ = ('api_url')
    projects_list = []

    def __init__(self) -> None:
        """Инициализация: URL проектов строительства"""
        self.api_url = 'https://samolet.ru/api_redesign/projects/'

    def get_request(self) -> dict:
        """Возвращает информацию о проектах строительства"""
        self.response = requests.get(self.api_url).json()
        return self.response

    @classmethod
    def clear_projects_list(cls) -> None:
        """Очищает список объектов строительства (атрибут класса)"""
        cls.projects_list.clear()

    def append_project_to_dict(self) -> None:
        """Добавляет идентификаторы объектов строительства в список проектов (атрибут класса)"""
        self.get_request()
        self.clear_projects_list()
        for project in self.response:
            self.projects_list.append(project['pk'])


class SamoletAPIGetFlats(SamoletAPI):
    """Класс получения информации о квартирах проектов строительства"""
    __slots__ = ('api_url')
    flats_list = []
    flats_count = 0

    def __init__(self, project_id: int, offset: int, limit: int = 250) -> None:
        """Инициализация: URL квартир проекта"""
        self.api_url = f"https://samolet.ru/api_redesign/flats/?project={project_id}&rooms=0,1,2,3,4&limit={limit}&offset={offset}"

    def get_request(self) -> dict:
        """Возвращает информацию о квартирах проекта"""
        self.response = requests.get(self.api_url).json()
        self.__class__.flats_count = len(self.response['results'])
        return self.response

    @classmethod
    def print_flats_info(cls) -> None:
        """Выводит в консоль информацию а загруженном проекте и кол-ву кывартир по нему"""
        try:
            project_name = cls.flats_list[0][1]
            flats_count = len(cls.flats_list)
            current_time = datetime.now().strftime('%H:%M:%S')

            message = f"[{current_time}]: Проект \"{project_name}\" успешно загружен! " \
                      f"Всего квартир: {flats_count}"

            print(message)

        except IndexError:
            pass

    @classmethod
    def clear_flats_list(cls) -> None:
        """Очищает список квартир (атрибут класса)"""
        cls.flats_list.clear()

    @classmethod
    def reformat_flats_list(cls) -> str:
        """Возвращает реоформатированную строку из списка квартир под insert в БД"""
        return ",\n".join(map(str, cls.flats_list))

    def append_flat_to_list(self) -> None:
        """Добавляет квартиры в список квартир (атрибут класса)"""
        self.get_request()

        for flat in self.response['results']:
            self.flats_list.append(
                (
                    flat['id'],
                    flat['project'],
                    flat['floor_number'],
                    flat['total_floors'],
                    flat['url'],
                    flat['rooms'],
                    flat['price'],
                    flat['price_with_kitchen_markup'],
                    flat['settling_date_formatted'],
                    flat['area']
                )
            )
