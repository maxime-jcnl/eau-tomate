from prettytable import PrettyTable


class Automate:
    def __init__(self, alphabet, nb_etats, nb_init, lst_init, nb_term, lst_term, nb_trans, lst_trans):
        self.alphabet = alphabet
        self.nb_etats = nb_etats
        self.nb_init = nb_init
        self.lst_init = lst_init
        self.nb_term = nb_term
        self.lst_term = lst_term
        self.nb_trans = nb_trans
        self.lst_trans = lst_trans

    def show(self):
        x = PrettyTable()
        x.field_names = ["i/o", "state"] + alphaliste(self.alphabet)

        for i in range(self.nb_etats):  #On parcourt pour chaque état existant

            # Vérification etat initial final
            if (i in self.lst_init):
                io = "i"
            elif i in self.lst_term:
                io = "o"
            else:
                io = " "
            addedrow=False
            for trans in self.lst_trans: # On parcourt toute la liste de transition

                trans_state_liste = [' '] * self.alphabet
                if trans[0]==str(i):  # Si une transition est liée à l'état observé
                    trans_state_liste[alph_to_num(trans[1])]=str(trans[2])
                    x.add_row([io, i] + trans_state_liste)
                    addedrow = True
            if addedrow==False:
                x.add_row([io, i] + trans_state_liste)

        print(x)


def str_to_int(list):
    intliste = []
    for elm in list:
        intliste.append(int(elm))
    return intliste

def alph_to_num(lettre):
    lettre = lettre.lower()  # Convertir en minuscule pour gérer les lettres majuscules
    if lettre.isalpha() and len(lettre) == 1:  # Vérifier si la lettre est alphabétique et de longueur 1
        return ord(lettre) - ord('a')  # Retourner le numéro correspondant
    else:
        raise ValueError("Entrée invalide: Veuillez entrer une seule lettre alphabétique")


def alphaliste(n):
    if n <= 0:
        return []

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return [alphabet[i] for i in range(n)]


def lire_fichier_automate(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
        alphabet = int(lignes[0].strip())  # Strip permet de supprimer les caractères de retour à la ligne
        nb_etats = int(lignes[1].strip())
        lst_init = str_to_int(lignes[2].split())  # Split forme une liste d'élément séparé d'espace
        nb_init = lst_init.pop(0)
        lst_term = str_to_int(lignes[3].split())
        nb_term = lst_term.pop(0)
        nb_trans = int(lignes[4].strip())
        lst_trans = []
        for i in range(5, len(lignes)):
            newTrans = lignes[i].split()
            lst_trans.append(newTrans)
        automate = Automate(alphabet, nb_etats, nb_init, lst_init, nb_term, lst_term, nb_trans, lst_trans)
    return automate


# Utilisation du programme
if __name__ == '__main__':
    newAuto = lire_fichier_automate("test.txt")
    newAuto.show()
