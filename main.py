from tableau import *
import os

command = input('for the first query or to renew the database, enter "r"\nfor further queries in the same database, enter "c":\n')
T = Tableau()
chemin_mem = os.getcwd()
if command =='r':
    chemin_bdd = input('enter the path of your database :\n')
    T.initialisation(chemin_bdd,0)
    T.save(chemin_mem+'/save.txt')

else:
    T=load(chemin_mem+'/save.txt')
T.search()
