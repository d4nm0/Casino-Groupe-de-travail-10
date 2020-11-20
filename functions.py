from mysql_class import Mysql
from random import seed
from random import randint
from inputimeout import inputimeout
import sys
import random
import time
import inquirer

my_sql = Mysql(host='localhost', user='root', password='', database='kasino')

level = 1
solde = 10
nb_coup = 0
nb_essaie = 3

# Stat par level
def show_level_stats(my_sql, player, level = 1):
    player_sql = my_sql.select('player', "username = %s", "id", username=player)
    stats = my_sql.select('history', "player_id = %s AND level= %s", "MAX(gain)", "MAX(bet)", "MIN(gain)", "MIN(bet)", "AVG(bet)", "AVG(nb_try)", player_id=str(player_sql[0]), level=level)

    print("Les statistiques du level", level, "sont les suivantes :\n")
    print("\t- Vos meilleures statistiques :\r")
    print("\t\t- Le gain le plus elevé est", stats[0][0], "\r")
    print("\t\t- La mise la plus elevé est", stats[0][1], "\r")
    print("\t- Vos pires statistiques :\r")
    print("\t\t- Le gain le plus elevé est", stats[0][2], "\r")
    print("\t\t- La mise la plus elevé est", stats[0][3], "\r")
    print("\t- Vos moyennes :\r")
    print("\t\t- La mise moyenne est de", stats[0][4], "\r")
    print("\t\t- Le nombre moyen de tentatives pour trouver le bon nombre est :", stats[0][5], "\r")

# Stat global
def show_global_stats(my_sql, player):
    player_sql = my_sql.select('player', "username = %s", "id", "created_at", username=player)
    stats = my_sql.select('history', "player_id = %s", "MAX(level)", "(SELECT COUNT(id) FROM history WHERE nb_try = 1 AND player_id = '"+ str(player_sql[0][0]) +"')", "MAX(gain)", "MAX(bet)", "MIN(level)", "MIN(gain)", "MIN(bet)", "AVG(bet)", "AVG(nb_try)", player_id=player_sql[0][0])

    print("Voici statistiques, depuis la 1è fois", player_sql[0][1].strftime("%d/%m/%Y %H:%M"), ":\n")
    print("\t- Vos meilleures statistiques :\r")
    print("\t\t- Level le plus élevé atteint est", stats[0][0], "\r")
    print("\t\t- Vous avez réussi à trouver le bon nombre dès le 1è coup", stats[0][1], "fois.\r")
    print("\t\t- Le gain le plus elevé est", stats[0][2], "\r")
    print("\t\t- La mise la plus elevé est", stats[0][3], "\r")
    print("\t- Vos pires statistiques :\r")
    print("\t\t- Level le plus élevé atteint est", stats[0][4], "\r")
    print("\t\t- Le gain le plus elevé est", stats[0][5], "\r")
    print("\t\t- La mise la plus elevé est", stats[0][6], "\r")
    print("\t- Vos moyennes :\r")
    print("\t\t- La mise moyenne est de", stats[0][7], "\r")
    print("\t\t- Le nombre moyen de tentatives pour trouver le bon nombre est :", stats[0][8], "\r")

# Affichage des règles du jeux et du lieu où il est stocké

def rules():
    rules = input("Voulez vous afficher les regles ?  Y / N  : ")
    if rules == 'Y' or rules == 'y':
        print("Voici les régles: ")
        mon_fichier = open("regles.txt", "r")
        contenu = mon_fichier.read()
        print(contenu)
        mon_fichier.close()
    elif rules == 'N' or rules == 'n': 
        print("Vous avez décidé de ne pas Regarder les régles")
    else:
        print("Vous devez faire un choix Y / N")
        rules()

# Fonction pour start le jeux

def start():
    rules()
    name_user, solde, level = name()
    player_1 = my_sql.insert('player', username=name_user, level=level)
    game(solde, nb_coup, nb_essaie, name_user, player_1, level)

#Fonction du choix du level si le User à déjà dépassé les différents niveaux

def chooseLevel(player_id):
    level = my_sql.select('history','player_id = %s order by id DESC limit 1', 'level', player_id=player_id)
    if level[0] > 1:
        choices = []

        for value in range(level[0]):
            choices.append("Niveau " + str(value + 1))

        levels = [
            inquirer.List('lvls',
                message="Choisissez votre niveau ?",
                choices=choices,
            ),
        ]

        answers = inquirer.prompt(levels)

        new_level = int(answers["lvls"][-1:])

        return new_level

# Fonction Name qui vérifie le User rentré dans la BDD et récupération du name et de l'id de cette user et de son solde

def name():
    name_user = str(input("Je suis Python. Quel est votre pseudo ? \n"))
    my_result = my_sql.select('player', '1 = 1 ', 'username')
    level = 1

    if name_user in my_result :
        my_id = my_sql.select('player', 'username = %s', 'id', username=name_user)
        my_sold = my_sql.select('history','player_id = %s order by id DESC limit 1', 'gain', player_id=str(my_id[0]))
        level = chooseLevel(str(my_id[0]))
        solde = my_sold[0]
        print ('Rebonjour', name_user, ', vous avez ', solde, '.  Installez vous SVP à la table de pari.')
    else:
        print ('Hello', name_user, ', vous avez ', solde,'€, Très bien ! Installez vous SVP à la table de pari. Je vous expliquerai le principe du jeu :')
    
    return name_user, solde, level

# fonction sur les règles en fonction du level 

def levelRules(level):
    if level == 1:
        print("""
Att : vous avez le droit à trois essais ! :
\t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !
\t- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !
\t- Si vous le devinez au 3è coup, vous gagnez la moitié de votre mise !
\t- Si vous ne le devinez pas au 3è coup, vous perdez votre mise
             """)
    elif level == 2:
        print("""
Att : vous avez le droit à cinq essais ! :
\t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !
\t- Si vous le devinez au 2è coup, vous gagnez exactement votre de mise !
\t- Si vous le devinez au 3è coup, vous gagnez la moitié de votre mise !    
\t- Si vous le devinez au 4è coup, vous gagnez 1/3 de votre mise !  
\t- Si vous le devinez au 5è coup, vous gagnez 1/4 de votre mise !   
\t- Si vous ne le devinez pas au 5è coup, vous perdez votre mise
             """)
    elif level == 3:
        print("""
Att : vous avez le droit à sept essais ! :
\t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !
\t- Si vous le devinez au 2è coup, vous gagnez exactement votre de mise !
\t- Si vous le devinez au 3è coup, vous gagnez la moitié de votre mise !   
\t- Si vous le devinez au 4è coup, vous gagnez 1/3 de votre mise !  
\t- Si vous le devinez au 5è coup, vous gagnez 1/4 de votre mise ! 
\t- Si vous le devinez au 6è coup, vous gagnez 1/5 de votre mise !  
\t- Si vous le devinez au 7è coup, vous gagnez 1/6 de votre mise ! 
\t- Si vous ne le devinez pas au 7è coup, vous perdez votre mise
             """)
    return level

# fonction sur les gains obtenu à la fin du level en fonction du nombre de coups

def balance(nb_coup, solde, mise, name_user, level, player_1):
    print("vous avez gagner")
    if nb_coup == 1:
        print("Vous avez remporté : ", mise*2, "€")
        solde = solde + mise
    elif nb_coup == 2:
        print("Vous avez remporté : ", mise, "€")
        solde = solde
    elif nb_coup == 3:
        print("Vous avez remporté : ", mise/2, "€")
        solde = solde + mise/2
    elif nb_coup == 4:
        print("Vous avez remporté : ", mise/3, "€")
        solde = solde + mise/3
    elif nb_coup == 5:
        print("Vous avez remporté : ", mise/4, "€")
        solde = solde + mise/4
    elif nb_coup == 6:
        print("Vous avez remporté : ", mise/5, "€")
        solde = solde + mise/5
    else:
        print("Vous avez remporté : ", mise/6, "€")
        solde = solde + mise /6
    my_sql.insert('history', player_id=player_1, level=level, bet=mise, nb_try=nb_coup, gain=solde)
    return solde


# fonction sur la mise rentrée pour voir si elle est correcte en fonction du solde que le User a

def bet(range_number, solde):
    while True:
        try:
            mise = int(input("Le jeu commence, entrez votre mise : ?\n"))
        except ValueError:
            print("Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et", solde, ": ?\n")
        else:
            if mise <= range_number and mise >= 1:
                print ("La mise est bonne")
                return mise
            else:
                print("Votre mise est trop fort ! Entrer SVP un montant entre 1 et ", range_number)

# Fonction sur le nombre à trouver aléatoire en fonction du level 

def nbPython(range_number):
    nb_python  = random.randint(1, range_number)
    print("Je viens de penser à un nombre entre 1 et ", range_number, ". Devinez lequel ?\n")
    print("nb alea:", nb_python)
    return nb_python

# Fonction sur le nombre que le User rentre pour trouver le chiffre aléatoire

def nbUser(range_number, nb_coup, nb_essaie, solde, mise, level, nb_python):
    while True:
        try:
           nb_user = int(inputimeout('Alors mon nombre est : ?\n', timeout=10))
        except:
            nb_coup +=1
            nb_essaie -= 1
            print("Vous avez dépassé le délai de 10 secondes ! Vous perdez l'essai courant et il vous reste ", nb_essaie," essai(s) !")
            if nb_coup == 3:
                solde = solde - mise
                gameOver(solde, mise, level, nb_coup, nb_essaie, range_number, nb_python, "")
                break
        else:
            if nb_user <= range_number:
                nb_coup +=1
                return nb_user, nb_coup
            else:
                print("/!\ Nombre Invalide /!\ Entrer SVP un nombre entre 1 et", range_number, ":\n")

# Fonction pour afficher si le nombre rentré est trop petit ou trop grand

def moreLess(nb_python, nb_user):
    if nb_user < nb_python:
        print("Votre nbre est trop petit !\n")
    elif nb_user > nb_python:
        print("Votre nbre est trop grand !\n")

# Fonction loose, perd la mise et le level redescend, vous avez le choix de fermer le jeux ou de rejouer

def gameOver(solde, mise, level, nb_coup, nb_essaie, range_number, nb_python, name_user):
    solde = solde - mise
    print("Vous avez perdu ! Mon nombre est ", nb_python," !")
    if level == 1:
        print("vous etes au level ", level)
    else:
        level -= 1
        range_number = 10*level
        print("Vous retournez au level précédent : level", level)        

    print ("Votre solde est de : ", solde)
    print("\nVous avez le droit : ")
    print("1 : de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu.")
    print("2 : de quitter le jeu.")     

    choix = int(input("\nVeuillez faire votre choix : 1 ou 2 ? "))
    if choix == 1:
        nb_coup = 0
        print("vous recommncez avec un solde de : ", solde, "€")
        game(solde, nb_coup, nb_essaie, '', '', 1)
    elif choix == 2:
        my_sql.insert('player', username=name_user, level=level)
        print("Vous repartez avec la somme de :", solde, "€")
        show_global_stats(my_sql, name_user)
        sys.exit()
    else:
        print("Veuillez choisir entre le choix 1 et le choix 2 ?")

# Fonction de win qui passe au niveau superieur qui rajoute le solde 

def win(level, range_number, nb_coup, nb_essaie, mise, nb_python, solde, name_user):
    print("Bingo", name_user, " vous avez gagné en ", nb_coup," coup(s) et vous avez emporté ", solde,"€ !")
    show_level_stats(my_sql, name_user, level)
    level += 1
    range_number = 10*level
    print("Range :", range_number)
    nb_coup = 0
    nb_essaie += 2
    print("Vous accédez donc au niveau supérieur : Niveau ", level) 
    levelRules(level)  
    mise = bet(range_number, solde)
    nb_python = nbPython(range_number)
    return level, range_number, nb_python, mise, nb_essaie

# Fonction du game avec l'affichage des règles en fonction du level,  appelle des différentes fonctions en fonction de la réussite ou de la loose

def game(solde, nb_coup, nb_essaie, name_user, player_1, level):
    levelRules(level)
    range_number = 10*level
    mise = bet(range_number, solde)
    nb_python = nbPython(range_number)    

    while nb_coup < nb_essaie:
        nb_user, nb_coup = nbUser(range_number, nb_coup, nb_essaie, solde, mise, level, nb_python)
        if nb_user <= range_number and nb_user >= 1:
            if nb_user == nb_python:
                solde = balance(nb_coup, solde, mise, name_user, level, player_1)
                if level == 3:
                    print("Félicitation vous venez de remporter le gros lot")
                    sys.exit()
                else:
                    level, range_number, nb_python, mise, nb_essaie = win(level, range_number, nb_coup, nb_essaie, mise, nb_python, solde, name_user)

            elif nb_user != nb_python:
                print("Ce n'est pas le bon numéro. Retente ta chance")
                moreLess(nb_python, nb_user)
    else :
        gameOver(solde, mise, level, nb_coup, nb_essaie, range_number, nb_python, name_user)