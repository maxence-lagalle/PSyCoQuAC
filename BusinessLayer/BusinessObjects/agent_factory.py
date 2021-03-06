from BusinessLayer.BusinessObjects.gestionnaire import Gestionnaire
from BusinessLayer.BusinessObjects.superviseur import Superviseur


class AgentFactory:
    @staticmethod
    def from_dict(data: dict):
        """
            Cette méthode permet de transformer un dictionnaire en Business Object Agent,
            dont les paramètres sont les valeurs du dictionnaire.

            :param data:
            un dictionnaire de données correspondant aux informations sur l'agent que l'on va créer
            :return:
            renvoie un objet de type agent
        """
        if data["est_superviseur"]:
            agent = Superviseur(data["prenom"], data["nom"], data["quotite"], data["identifiant_agent"])
        else:
            agent = Gestionnaire(data["prenom"], data["nom"], data["quotite"],
                                 superviseur_id=data["identifiant_superviseur"], agent_id=data["identifiant_agent"])
        return agent
