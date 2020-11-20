from mysql_class import Mysql
from random import seed
from random import randint
from inputimeout import inputimeout
import sys
import random
import time

my_sql = Mysql(host='localhost', user='root', password='', database='kasino')

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

rules()
time.sleep(3)

def name():
    name_user = str(input("Je suis Python. Quel est votre pseudo ? \n"))
    my_result = my_sql.select('player', '1 = 1 ', 'username')
    print(my_result)
    if name_user in my_result :
        my_id = my_sql.select('player', 'username = %s', 'id', username=name_user)
        my_sold = my_sql.select('history','player_id = %s order by id DESC limit 1', 'gain', player_id=str(my_id[0]))
        solde = my_sold[0]
        print ('Rebonjour', name_user, ', vous avez ', solde, '.  Installez vous SVP à la table de pari.')
    else:
        print ('Hello', name_user, ', vous avez ', solde,'€, Très bien ! Installez vous SVP à la table de pari. Je vous expliquerai le principe du jeu :')
    return name_user, solde
name()
time.sleep(3)

def levelRules(level=2):
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

levelRules()
time.sleep(3)

def balance(nb_coup=2, solde=10, mise=2, name_user="Robin", level=3, player_1=1):
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

balance()
time.sleep(3)

def bet(range_number=20, solde=15):
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
bet()
time.sleep(3)


def nbPython(range_number=30):
    nb_python  = random.randint(1, range_number)
    print("Je viens de penser à un nombre entre 1 et ", range_number, ". Devinez lequel ?\n")
    print("nb alea:", nb_python)
    return nb_python

nbPython()
time.sleep(3)

def nbUser(range_number=10, nb_coup=2, nb_essaie=3, solde=10, mise=4, level=1, nb_python=6):
    while True:
        try:
           nb_user = int(inputimeout('Alors mon nombre est : ?\n', timeout=10))
        except:
            nb_coup +=1
            nb_essaie -= 1
            print("Vous avez dépassé le délai de 10 secondes ! Vous perdez l'essai courant et il vous reste ", nb_essaie," essai(s) !")
            if nb_coup == 3:
                solde = solde - mise
                print("vous avez perdu")
                break
        else:
            if nb_user <= range_number:
                nb_coup +=1
                return nb_user, nb_coup
            else:
                print("/!\ Nombre Invalide /!\ Entrer SVP un nombre entre 1 et", range_number, ":\n")
nbUser()
time.sleep(3)

def moreLess(nb_python=5, nb_user=2):
    if nb_user < nb_python:
        print("Votre nbre est trop petit !\n")
    elif nb_user > nb_python:
        print("Votre nbre est trop grand !\n")

moreLess()
time.sleep(3)

def moreLess(nb_python=5, nb_user=10):
    if nb_user < nb_python:
        print("Votre nbre est trop petit !\n")
    elif nb_user > nb_python:
        print("Votre nbre est trop grand !\n")
moreLess()
time.sleep(3)

def win(level=1, range_number=10, nb_coup=3, nb_essaie=3, mise=5, nb_python=9, solde=10, name_user="Robin"):
    print("Bingo", name_user, " vous avez gagné en ", nb_coup," coup(s) et vous avez emporté ", solde,"€ !")
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

win()
time.sleep(3)

def gameOver(solde=10, mise=5, level=1, nb_coup=2, nb_essaie=3, range_number=10, nb_python=6, name_user="Robin"):
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
        print("vous recommncez au level precédent")
    elif choix == 2:
        my_sql.insert('player', username=name_user, level=level)
        print("Vous repartez avec la somme de :", solde, "€")
        sys.exit()
    else:
        print("Veuillez choisir entre le choix 1 et le choix 2 ?")
gameOver()
time.sleep(3)

def game(solde=15, nb_coup=2, nb_essaie=3, name_user="Robin", player_1=1):
    level = 1
    range_number = 10*level
    nb_python = 6   

    while nb_coup < nb_essaie:
        nb_user = 6
        if nb_user <= range_number and nb_user >= 1:
            if nb_user == nb_python:
                solde = solde
                if level == 3:
                    print("Félicitation vous venez de remporter le gros lot")
                    sys.exit()
                else:
                    level += 1
                    print("vous avez gagnez")
                    print("Vous accédez donc au niveau supérieur : Niveau ", level) 
                
            elif nb_user != nb_python:
                print("Ce n'est pas le bon numéro. Retente ta chance")     
    else :
         print("vous avez perdu")
game()