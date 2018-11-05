"""This code is a Sphynx Routine for Taylor Green. Just to visualize the position of the particles. No color map necessary. Just visualisation of the strings or not"""

"""PBS!!! Les indices ne sont pas les meme qu'avant.... PK?! Deois-je tt refaire? Est-ce que c'est juste sur ce cas??"""

####Packages to use
import numpy as np
import csv
import matplotlib.pyplot as plt
import os

##Physical parameters
nu = 0.01
dt = 0.08
wF = 1
L = 1
psi =2*np.pi/L# 1/L#
rho = 1000
p0 = 10.

# #Physical time consideres--Wrong cause adaptative time
# time = dt * number * wF

###Indexes in a paraviex file

indice_paraview_pos_vert = 44 #if cond_paraview depl vertical
indice_paraview_vit_vert = 41 #if cond_paraview vit vertical
indice_paraview_vit_hor = 39 #if cond_paraview  vit hor
indice_paraview_press = 0 #if cond_paraview pressure
indice_paraview_dens = 1 #if cond_paraview density
indice_paraview_pos_hor = 42

##For one file
#.amax : max of a np/amin:min/ .mean : arithmetic mean

def data_file(adresse, data):

        #Reading file
        fichier = open(adresse, "r")
        lec = csv.reader(fichier)
        
        data_tab = []
        #print(lec)
        #print(adresse)
        for row in lec:
            #print(row)
            if (row != []):
                cond_test = (row[6][0] != 'D')
            
            if (row != [])and cond_test:
                
                if (data == "vit_vert"):
                    data_tab.append(float(row[indice_paraview_vit_vert]))
                
                if (data == "vit_hor"):
                    data_tab.append(float(row[indice_paraview_vit_hor]))
                    
                if (data == "press"):
                    data_tab.append(float(row[indice_paraview_press]))
                    
                if (data == "pos_vert"):
                    data_tab.append(float(row[indice_paraview_pos_vert]))
                    
                if (data == "pos_hor"):
                    data_tab.append(float(row[indice_paraview_pos_hor]))
        fichier.close()
        
        return data_tab
        
        

##Parameters
"""B:TO CHANGE(1)"""
number_tab = np.arange(2, 4000, 10) #table of number of timesteps
#For links towards results
Root = "E:/Stage_EDF_Lab/TaylorGreenVortices/TG_Numerical_Test/Cas_test_4/"
Case = "TaylorGreenVortices2D_Pres1_R1_nu_10m2_p0_1000"
Case_n = "Pres1_R1_nu_10m2_p0_1000"

#table of times for each case
#Link towards Sphynx timme used
linkTime = Root+Case+"/timelog.txt"

#Root to save

RootSave = Root+Case+"/Figures/"
    
"""E:TO CHANGE(1)"""

x_title = "Horizontal position/X-position (m) "
y_title = "Vertical position/Z-position (m)"


###Generation of the data tables
##Functions to help getting data
#for physical time (because adaptative timestep)
#time_liste are the physical times used in the whole simulation -- time_liste_graph := those used in the plotting (in number tab)
#Beware : timelog : first line = first time_step so time[0] <-> number = 1 --> that s why no number = 0 in number_tab

def extraction_table_times(link, number_tab):
    fichier = open(link, "r")
    time_liste = []
    for ligne in fichier:
        liste = ligne.split(' ')
        if (liste[0] == 'Time'):
            time_liste.append(float(liste[-2]))
        
    fichier.close()
    time_liste_graph = []
    
    for number in number_tab:
        time_liste_graph.append(time_liste[number-1])
    return time_liste_graph
    
##Getting the date (x-pos, y-pos)
"""B:TO CHANGE(2)"""
show_graph = False
save_graph = not show_graph
"""B:TO CHANGE(2)"""

compteur = 0

#timelist
time_list = extraction_table_times(linkTime, number_tab)
#graphs
for number in number_tab:
    
    #link
    link = Root+Case+"/CSV_files/CSV_"+Case_n+"_."+str(number)+".csv"
    #getting the data
    ord = data_file(link, "pos_vert")
    abs =  data_file(link, "pos_hor")
    
    
    #plot
    plt.figure()
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.plot(abs, ord, "ko", markersize = 1)
    plt.title("t = " +str(time_list[compteur])+" s")
    
    if (show_graph):
        plt.show()
        
    if (save_graph):
        file_name = RootSave+"imag."+str(compteur)+".png"
        #print(number)
        plt.savefig(file_name)
        plt.close()
        compteur=compteur+1