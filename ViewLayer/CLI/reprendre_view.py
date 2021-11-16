from BusinessLayer.BusinessObjects.adresse import Adresse
from ViewLayer.CLI.abstract_view import AbstractView
from ViewLayer.CLI.session import Session
from BusinessLayer.WebServices.BANClient import BANClient
from BusinessLayer.LocalServices.Gestion.agent_service import AgentService
from BusinessLayer.LocalServices.TraitementFA.controle_reprise_service import ControleRepriseService
from PyInquirer import prompt

class ReprendreView(AbstractView):

    def __init__(self, session : Session) -> None:

        self.__questions = [{'type': 'list','name': 'choix','message': 'Que voulez-vous faire ?',
                            'choices': ["a) Modifier l'adresse",'c) Modifier les coordonnées GPS', 'v) Valider la fiche', 'd) Marquer la fiche en déchet',  'p) Passer à la fiche précédente', 's) Passer à la fiche suivante', 'm) Retourner au menu principal']}]
        self.__questions2 = [{'type':'list', 'name':'choix', 'message': 'Confirmez-vous ?', 'choices':['Oui', 'Non']}]
        self.__questions3 = [{'type': 'input','name': 'numero','message': 'Numéro de voie :'}, {'type': 'input','voie': 'nom','message': 'Nom de la voie',},
            {'type': 'input','name': 'cd','message': 'Code postal :'}, {'type': 'input','name': 'ville','message': 'Ville :'}]
        self.__questions4 = [{'type': 'list', 'name' : 'choix', 'message': "Voulez vous resoumettre la fiche à l'API ?", 'choices':['Oui', 'Non']}]
        self.__questions5 = [{'type': 'input','name': 'lat','message': 'Latitude :'}, {'type': 'input','name': 'lon','message': 'Longitude :'}]
    
    def make_choice(self, session : Session, curseur : int = 0): # curseur = l'emplacement de la fiche en contrôle dans la liste
        pot = AgentService.recupere_pot(session.agent_id) 
        fiche = pot[curseur] # On récupère la fiche dans le pot de l'agent
        print('Fiche adresse n°' + str(fiche.fiche_id) + 'Données initiales : adresse initiale : ' + str(fiche.adresse_initiale) + 'Données API : Adresse finale : '  + str(fiche.adresse_finale) + 'Coordonnées GPS :' + str(fiche.coords_wgs84))
        answers = prompt(self.__questions)
        if 'a)' in str.lower(answers['choix']) :
            answers3 = prompt(self.__questions3)
            nouvelle_adresse = Adresse('numero', 'voie', 'cd', 'ville')
            res = ControleRepriseService.modifier_fiche(fiche.fiche_id, { 'adresse_finale': nouvelle_adresse})
            answers4 = prompt(self.__questions4)
            if str.lower(answers4['choix']) == 'Oui' :
                # Resoumettre à l'API
                score, fiche = BANClient.geocodage_par_fiche(fiche)
                print("Le score de l'API est" + str(score))
            elif str.lower(answers4['choix']) == 'Non' :
                return ReprendreView(session)
        elif 'c)' in str.lower(answers['choix']) :
            answers5 = prompt(self.__questions5)
            nouvelles_coords = ('lat', 'lon')
            res = ControleRepriseService.modifier_fiche(fiche.fiche_id, { 'coords_wgs84': nouvelles_coords})
            answers4 = prompt(self.__questions4)
            if str.lower(answers4['choix']) == 'Oui' :
                # Resoumettre à l'API
                score, fiche = BANClient.geocodage_par_fiche(fiche)
                print("Le score de l'API est" + str(score))
            elif str.lower(answers4['choix']) == 'Non' :
                return ReprendreView(session)
        elif 'v)' in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = ControleRepriseService.modifier_fiche(fiche.fiche_id, {'code_res' : 'VR'})
                return ReprendreView(session)
            elif str.lower(answers2['choix']) == 'Non':
                return ReprendreView(session)
        elif 'd)'in str.lower(answers['choix']) :
            answers2 = prompt(self.__questions2)
            if str.lower(answers2['choix']) == 'Oui' :
                res = ControleRepriseService.modifier_fiche(fiche.fiche_id, {'code_res' : 'DR'})
                return ReprendreView(session)
            elif str.lower(answers2['choix']) == 'Non':
                return ReprendreView(session)
        elif 'p)' in str.lower(answers['choix']) :
            curseur = (curseur-1) % len(pot)
            return ReprendreView(session)
        elif 's)'in str.lower(answers['choix']) :
            curseur = (curseur+1) % len(pot)
            return ReprendreView(session)
        elif 'm)' in str.lower(answers['choix']) :
            from ViewLayer.CLI.menu import MenuPrincipalView
            return MenuPrincipalView(session)