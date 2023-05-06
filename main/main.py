from classes.api_samolet import SamoletAPIGetFlats, SamoletAPIGetProjects
from classes.db_manager import PGDBSamoletManager
from classes.db_connector import PGDBBaseConnector
from utils.timer import timer


@timer
def main():
    SamoletAPIGetProjects().append_project_to_dict()

    for project in SamoletAPIGetProjects.projects_list:
        SamoletAPIGetFlats.clear_flats_list()
        offset = 0

        while True:
            SamoletAPIGetFlats(project_id=project, offset=offset).append_flat_to_list()
            if SamoletAPIGetFlats.flats_count == 0:
                break
            offset += 250

        if not SamoletAPIGetFlats.flats_list:
            continue

        data = SamoletAPIGetFlats.reformat_flats_list()

        samolet_connection = PGDBBaseConnector()
        PGDBSamoletManager(samolet_connection).group_insert(data)

        SamoletAPIGetFlats.print_flats_info()


if __name__ == '__main__':
    main()

