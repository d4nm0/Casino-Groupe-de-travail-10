# Stat par level 
def show_level_stats(my_sql, player, level = 1):
    stats = my_sql.select('history', "player_id = %s AND level= %s", "MAX(gain)", "MAX(bet)", "MIN(gain)", "MIN(bet)", "AVG(bet)", "AVG(nb_try)", player_id=player, level=level)

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
    date_debut = my_sql.select('player', "id = %s", "created_at", id=player)
    stats = my_sql.select('history', "player_id = %s", "MAX(level)", "(SELECT COUNT(id) FROM history WHERE nb_try = 1 AND player_id = '"+ str(player) +"')", "MAX(gain)", "MAX(bet)", "MIN(level)", "MIN(gain)", "MIN(bet)", "AVG(bet)", "AVG(nb_try)", player_id=player)

    print("Voici statistiques, depuis la 1è fois", date_debut[0].strftime("%d/%m/%Y %H:%M"), ":\n")
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
