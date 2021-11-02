import sqlite3
from DataLayer.DAO.interface_connexion import InterfaceConnexion


class SQLiteConnexion(InterfaceConnexion):
    
    def ouvrir_connexion(self, host, port, database, user, password):
        try:
            connexion = sqlite3.connect(host)
            connexion.row_factory = sqlite3.Row
            return connexion
        except Exception as e:
            raise e

    def fermer_connexion(self, connexion):
        connexion.close()
