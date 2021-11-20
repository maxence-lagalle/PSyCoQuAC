from PyInquirer import prompt
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from ViewLayer.CLI.controler_view import ControlerView
from ViewLayer.CLI.reprendre_view import ReprendreView
from ViewLayer.CLI.menu import MenuPrincipalView


class ConsulterPotView(AbstractView):
    def __init__(self, id_agent: int = None, controle: bool = False, reprise: bool = False, curseur: int = 0) -> None:
        if id_agent is None:
            self.__id_agent = Session().agent.agent_id
        else:
            self.__id_agent = id_agent
        if controle or reprise:
            self.__work = True
            self.pot = ControleRepriseService().consulter_pot_controle_reprise(self.__id_agent, controle, reprise)
        else:
            self.__work = False
            self.pot = ControleRepriseService().consulter_pot(self.__id_agent)
        self.__curseur = curseur

    def display_info(self):
        if len(self.pot) > 0:
            self.__curseur = self.__curseur % len(self.pot)
            fiche = self.pot[self.__curseur]
            print(fiche)
        else:
            print("Le pot de fiches à traiter est vide.")

    def make_choice(self):
        if len(self.pot) > 0:
            fiche = self.pot[self.__curseur]
            questions = [{'type': 'list', 'name': 'choix', 'message': 'Que voulez-vous faire ?', 'choices': []}]
            if len(self.pot) > 1:
                questions[0]['choices'].append("P) Retourner à la fiche précédente")
                questions[0]['choices'].append("S) Passer à la fiche suivante")
            if self.__id_agent == Session().agent.agent_id:
                if fiche.code_res == "TC":
                    questions[0]['choices'].append("C) Contrôler la fiche")
                elif fiche.code_res == "TR":
                    questions[0]['choices'].append("R) Reprendre la fiche")
            questions[0]['choices'].append('Q) Retourner au menu principal')
            answers = prompt(questions)
            if str.upper(answers['choix'][0]) == "P":
                self.__curseur = (self.__curseur - 1) % len(self.pot)
                return self
            elif str.upper(answers['choix'][0]) == "S":
                self.__curseur = (self.__curseur + 1) % len(self.pot)
                return self
            elif str.upper(answers['choix'][0]) in ["C", "R"]:
                if fiche.code_res == "TC":
                    modal = ControlerView(self, fiche)
                elif fiche.code_res == "TR":
                    modal = ReprendreView(self, fiche)
                else:
                    return self
                modal.display_info()
                res, nouv_fiche, caller = modal.make_choice()
                if res:
                    if self.__work:
                        caller.pot.remove(fiche)
                    else:
                        caller.pot[caller.pot.index(fiche)] = nouv_fiche
                return caller
            elif str.upper(answers['choix'][0]) == "Q":
                return MenuPrincipalView()
            else:
                raise ValueError
        else:
            return MenuPrincipalView()
