from BusinessLayer.LocalServices.IO.csv_exportation import CSVExportation

class DBExportation:

    def __init__(self):
        dotenv.load_dotenv(override=True)
        if type_fichier == "CSV":
            self.__type_fichier = CSVExportation()
        self.__exportation = self.__type_fichier.exportation(os.environ["HOST"], os.environ["PORT"],
                                                             os.environ["DATABASE"],
                                                             os.environ["USER"], os.environ["PASSWORD"])

    @property
    def exportation(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__exportation
        