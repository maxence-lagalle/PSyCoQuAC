from BusinessLayer.BusinessObjects.agent import Agent


class Gestionnaire(Agent):

    def __init__(self, prenom : str, nom : str, superviseur_id : int, agent_id: int = None):
        super().__init__(prenom, nom, agent_id)
        self._superviseur_id = superviseur_id

    @property
    def superviseur_id(self) -> int:
        return self._superviseur_id

    def as_dict(self) -> dict:
        data = super().as_dict()
        data["identifiant_superviseur"] = self._superviseur_id
        data["est_superviseur"] = False
        return data
