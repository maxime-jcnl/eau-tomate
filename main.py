from prettytable import PrettyTable


class Automate:
    def __init__(self, alphabet, nb_state, nb_init, lst_init, nb_term, lst_term, nb_trans, lst_trans):
        self.alphabet = alphabet
        self.nb_state = nb_state
        self.nb_init = nb_init
        self.lst_init = lst_init
        self.nb_term = nb_term
        self.lst_term = lst_term
        self.nb_trans = nb_trans
        self.lst_trans = lst_trans

    def show(self):
        x = PrettyTable()
        x.field_names = ["i/o", "state"] + alphaListe(self.alphabet)

        for i in range(self.nb_state):  # Pour chaque état
            io=""
            if i in self.lst_init:
                io += "i"
            if i in self.lst_term:
                io += "o"
            if i not in self.lst_init and i not in self.lst_term:
                io = " "

            # Création d'une liste vide pour les transitions de l'état actuel
            trans_state_liste = [' '] * self.alphabet

            # Récupération des transitions de l'état actuel depuis lst_trans
            for trans in self.lst_trans[i]:
                # Ajout de la destination à la liste des transitions
                if trans_state_liste[alph_to_num(trans[1])] == ' ':
                    trans_state_liste[alph_to_num(trans[1])] = str(trans[2])
                else:
                    trans_state_liste[alph_to_num(trans[1])] += ',' + str(trans[2])

            # Ajout de la ligne dans la table
            x.add_row([io, i] + trans_state_liste)

        print(x)

    def isDeter(self):
        for state_index in range(self.nb_state):
            trans_list = []
            for trans in self.lst_trans[state_index]:
                if trans[1] not in trans_list:
                    trans_list.append(trans[1])
                else:
                    return False
        return True

    def addState(self):
        self.nb_state += 1
        self.lst_trans.append([]) # car sinon out of range
        return self.nb_state
    def addInput(self,state):
        if state not in self.lst_init:
            self.nb_init += 1
            self.lst_init.append(state)
        else:
            print("déjà initial")

    def addOutput(self,state):
        if state not in self.lst_term:
            self.nb_term += 1
            self.lst_term.append(state)
        else:
            print("déjà initial")

    def isStandard(self):
        if self.nb_init != 1:
            return False
        entrant_states = []
        for trans in self.lst_trans:
            entrant_states.append(int(trans[2]))

        # Vérifier que l'unique état initial n'est pas une cible de transition
        if self.lst_init[0] in entrant_states:
            return False

        return True

    def standardize(self):

        if self.isStandard():
            print("Automate déjà standardisé")
            return

        c_trans=[]
        c_state = self.addState()

        #  Récupération des transitions qui concerne les états initiaux
        for i in range(self.nb_state):
            if i in self.lst_init:
                for j in range(len(self.lst_trans[i])):
                    c_trans.append(self.lst_trans[i][j])

        self.nb_trans += len(c_trans)
        self.nb_init = 1
        self.lst_init = [c_state-1]

        #  Modification des états de départ des transitions
        for i in range(len(c_trans)):
            c_trans[i][0] = str(c_state)
        self.lst_trans[c_state-1] = c_trans


    def isComplete(self):
        for state_trans in self.lst_trans:
            # Compter le nombre de transitions sortantes pour l'état
            num_transitions = len(state_trans)
            # Vérifier s'il manque des transitions pour certaines lettres de l'alphabet
            if num_transitions < self.alphabet:
                return False
        return True

    def addTrans(self,state,letter,dest):
        new_trans=[state,letter,dest]
        if new_trans in self.lst_trans[state]:
            print("Transition déjà éxistente")
            return

        self.nb_trans += 1
        self.lst_trans[state].append(new_trans)
def str_to_int(lst):
    int_liste = []
    for elm in lst:
        int_liste.append(int(elm))
    return int_liste


def alph_to_num(letter):
    letter = letter.lower()  # Convertir en minuscule pour gérer les lettres majuscules
    if letter.isalpha() and len(letter) == 1:  # Vérifier si la lettre est alphabétique et de longueur 1
        return ord(letter) - ord('a')  # Retourner le numéro correspondant
    else:
        raise ValueError("Entrée invalide: Veuillez entrer une seule lettre alphabétique")


def alphaListe(n):
    if n <= 0:
        return []

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return [alphabet[i] for i in range(n)]


def importAutomate(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        alphabet = int(lignes[0].strip())  # Strip permet de supprimer les caractères de retour à la ligne
        nb_state = int(lignes[1].strip())
        lst_init = str_to_int(lignes[2].split())  # Split forme une liste d'élément séparé d'espace
        nb_init = lst_init.pop(0)
        lst_term = str_to_int(lignes[3].split())
        nb_term = lst_term.pop(0)
        nb_trans = int(lignes[4].strip())

        # Initialisation de lst_trans comme une liste de liste vide
        lst_trans = [[] for _ in range(nb_state)]

        for i in range(5, len(lignes)):
            new_trans = lignes[i].split()
            state_index = int(new_trans[0])
            lst_trans[state_index].append(new_trans)

        automate = Automate(alphabet, nb_state, nb_init, lst_init, nb_term, lst_term, nb_trans, lst_trans)
    return automate


# Utilisation du programme
if __name__ == '__main__':
    newAuto = importAutomate("test.txt")
    newAuto.show()
    print(newAuto.isDeter())
    print(newAuto.isStandard())
    print(newAuto.isComplete())
    newAuto.show()
    newAuto.addInput(3)
    newAuto.addOutput(0)
    newAuto.show()
    newAuto.standardize()
    newAuto.show()
