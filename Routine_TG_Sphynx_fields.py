"""This code is a routine to see the fields in Taylor-Green simulations made in SPHYNX

We call for now :
    -Pres1 : initial pressure field given by the code
    -Pres2 : analytical initial pressure field
    -R1 : cartesian repartition of the particles
    -R2 : cartesian repartion of the particles + random move
"""

####Packages to use
import numpy as np
import csv
import matplotlib.pyplot as plt

##Physical parameters
"""B:TO CHANGE(0)"""
nu = 0.01
dt = 0.008
wF = 1
L = 1
psi =2*np.pi/L# 1/L#
rho = 1000
"""E:TO CHANGE(0)"""

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
        for row in lec:
            #print(len(row))
            #print(row)
            #print(row, row[indice_paraview_vit_vert])
            if (row != []):
                cond_test = (row[6][0] != 'D')
            
            if (row != [])and cond_test:
                if (data == "vit_vert"):
                    data_tab.append(float(row[indice_paraview_vit_vert]))
                
                if (data == "vit_hor"):
                    data_tab.append(float(row[indice_paraview_vit_hor]))
                    
                if (data == "press"):
                    data_tab.append(float(row[indice_paraview_press]))
        fichier.close()
        #Data we need
        data_tab = np.array(data_tab)
        mean_tab = np.mean(data_tab)
        max_tab = np.amax(data_tab)
        min_tab = np.amin(data_tab)
        
        # print(data)
        # print("Mean", mean_tab)
        # print("Max", max_tab)
        # print("Min", min_tab)
        
        return [mean_tab, max_tab, min_tab]
        
        
###Visualisation


#Theory
#Amplitude variation exp(gamma*t)
def gamma_f(data):
    if (data == "press"):
        gamma = -4 *nu*psi*psi
    else:
        gamma =-2 *nu*psi*psi
    return gamma
    
def amplitude_th_f(data, time):
    gamma = gamma_f(data)
    A = 1
    if (data == "press"):
        A = 0.5*rho
    return A * np.exp(gamma*time)
    
#Plot graphics

def plot_graphics(name, abs_tab, ord_tab, label_tab, color_tab, xtitle, ytitle):
    plt.figure()
    n = len(ord_tab)
    for i in range(n):
        plt.plot(abs_tab[i], ord_tab[i], color_tab[i], label = label_tab[i])
    plt.title(name)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.legend()
    plt.show()

##Parameters
"""B:TO CHANGE(1)"""
number_tab = np.arange(1, 4000, 50) #table of number of timesteps
#For links towards results
Root = "E:/Stage_EDF_Lab/TaylorGreenVortices/TG_Numerical_Test/Cas_test_4/"
Case_1 = "TaylorGreenVortices2D_Pres1_R1_nu_10m2_p0_0"
Case_1n = "Pres1_R1_nu_10m2_p0_0"
Case_2 = "TaylorGreenVortices2D_Pres1_R1_nu_10m2_p0_10"
Case_2n = "Pres1_R1_nu_10m2_p0_10"
Case_3 = "TaylorGreenVortices2D_Pres1_R1_nu_10m2_p0_40"
Case_3n = "Pres1_R1_nu_10m2_p0_40"
Case_4 = "TaylorGreenVortices2D_Pres1_R1_nu_10m2_p0_1000"
Case_4n = "Pres1_R1_nu_10m2_p0_1000"
data = "press"

nb_cases = 3

"""E:TO CHANGE(1)"""

x_title = "Physical time (s)"
y_title_error = "Relative error (%)"
y_title_time = "Characteristic Time (s)"
x_title_scaled = "Physical Time/ Characteristic Time $\tau$ (No dimension)"

if (data == "vit_vert"):
    y_title = "Velocity on the Z-axis ($m.s^{-1}$)"
    
if (data == "vit_hor"):
    y_title = "Velocity on the X-axis ($m.s^{-1}$)"
    
if (data == "press"):
    y_title = "Pressure (Pa)"

###Generation of the data tables
##Functions to help getting data
#for physical time (because adaptative timestep)
#time_liste are the physical times used in the whole simulation -- time_liste_graph := those used in the plotting (in number tab)
#Beware : timelog : first line = first time_step so time[0] <-> number = 1 --> that s why no number = 0 in number_tab

def extraction_table_times(adresse, number_tab):
    fichier = open(adresse, "r")
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

##Getting the data (velocities, ...)
#case = [[],[],[],[], [], [], [], [], []]#mean, max, min, amplitude, ln_amplitude, 1/charac_time, charca_time, max value_centered, min_value_centered
table_values = []
table_times = []

for i in range(nb_cases+1):#cases + theory
    table_values.append([[],[],[],[], [], [], [], [], []])
 
"""B:TO CHANGE(2)"""   
#table of times for each case
#Link towards Sphynx timme used
linkTime1 = Root+Case_1+"/timelog.txt"
linkTime2 = Root+Case_2+"/timelog.txt"
linkTime3 = Root+Case_3+"/timelog.txt"
linkTime4 = Root+Case_4+"/timelog.txt"
adresseTime_tab = [linkTime2, linkTime3, linkTime4]
"""E:TO CHANGE(2)"""


#remplissage tab de temps
for adresseT in adresseTime_tab:
    table_times.append(extraction_table_times(adresseT, number_tab))

#table for the theory
min_tab = []
max_tab = []
for j in range(len(table_times)):
    min_tab.append(table_times[j][0])
    max_tab.append(table_times[j][-1])
theory_time = np.linspace(np.amin(min_tab), np.amax(max_tab), len(table_times[0]))

#table of times
table_times.append(theory_time)

for number in number_tab:
    
    """B:TO CHANGE(3)""" 
    #Link towards Sphynx results###TOCHANGE
    adresse1 = Root+Case_1+"/CSV_files/CSV_"+Case_1n+"_."+str(number)+".csv"
    adresse2 = Root+Case_2+"/CSV_files/CSV_"+Case_2n+"_."+str(number)+".csv"
    adresse3 = Root+Case_3+"/CSV_files/CSV_"+Case_3n+"_."+str(number)+".csv"
    adresse4 = Root+Case_4+"/CSV_files/CSV_"+Case_4n+"_."+str(number)+".csv"
    
    adresse_tab = [adresse2, adresse3, adresse4]
    """E:TO CHANGE(3)"""
    
    if (len(adresse_tab) != len(table_values)-1):
        print("There is a problem")
    
    else:
        #test cases
        for k in range(len(adresse_tab)):
            
            #getting the data 
            adresse = adresse_tab[k]
            result = data_file(adresse, data)
            case = table_values[k]
            
            #getting time
            time = table_times[k][len(case[0])]
            
            #values
            case[0].append(result[0])
            case[1].append(result[1])
            case[2].append(result[2])
            case[3].append(0.5*(case[1][-1]-case[2][-1]))
            if (data != "press"):
                case[4].append(-np.log(case[3][-1]))
            else:
                case[4].append(np.log(0.5*rho)-np.log(case[3][-1]))
            case[5].append(case[4][-1]/time)
            case[6].append(1./case[5][-1])
            case[7].append(case[1][-1] - case[0][-1])
            case[8].append(case[2][-1] - case[0][-1])

for time in theory_time:
            
    #theoretical values expected
    theory = table_values[-1]
    theory[1].append(amplitude_th_f(data, time))
    theory[2].append(-amplitude_th_f(data, time))
    theory[3].append(amplitude_th_f(data, time))
    theory[4].append(-gamma_f(data)*time)
    theory[5].append(-gamma_f(data))
    theory[6].append(-1./gamma_f(data))
    theory[7].append(theory[1][-1])
    theory[8].append(theory[2][-1])

#Tables
table_values = np.array(table_values)
time_tab = table_times
time_tab_scaled = theory[5][-1] * np.array(table_times) #table of times scaled by the characteristic time

"""B:TO CHANGE(4)""" 
#To change depending on the cases
name_curves =  ["p0 = 10", "p0 = 40", "p0 = 1000"]
color_curves = ["b.", "g.", "c."]
"""E:TO CHANGE(4)"""

"""B:TO CHANGE(5)""" 
#Choice if show time_scaled_abscissa or Physical time
Physical_time = True
"""E:TO CHANGE(5)"""

if (Physical_time):
    ##Graphs
    #Mean value--all but theory
    plot_graphics("Mean value ", time_tab[:-1] , table_values[:,0][:-1], name_curves, color_curves,x_title, y_title)
    
    #Max value--all but theory
    plot_graphics("Max value ", time_tab[:-1] , table_values[:,1][:-1], name_curves, color_curves, x_title, y_title)
    
    #Min value--all but theory
    plot_graphics("Min value ", time_tab[:-1] , table_values[:,2][:-1], name_curves, color_curves, x_title, y_title)
    
    #Max and Min value
    plot_graphics("Max and min value", np.concatenate((time_tab, time_tab)) , np.concatenate((table_values[:,1], table_values[:,2]), axis=0), name_curves+["Theory"]+name_curves+["Theory"],color_curves+["k-."]+color_curves+["k-."], x_title, y_title)
    
    #Max and Min - centered a (Min + Mean value and Max - mean value)
    plot_graphics("Max and min value centered around 0", np.concatenate((time_tab, time_tab)) , np.concatenate((table_values[:,7], table_values[:,8]), axis=0), name_curves+["Theory"]+name_curves+["Theory"],color_curves+["k-."]+color_curves+["k-."], x_title, y_title)
    
    
    #Amplitude
    plot_graphics("Amplitude", time_tab , table_values[:,3], name_curves+["Theory"], color_curves+["k-."], x_title, y_title)
    
    #Amplitude
    plot_graphics("- Log (Amplitude)", time_tab , table_values[:,4], name_curves+["Theory"], color_curves+["k-."], x_title, "No dimension")
    
    #Inverse of characteristic time
    plot_graphics("1/Tau", time_tab , table_values[:,5], name_curves+["Theory"], color_curves+["k-."], x_title, "$s^{-1}$")
    
    #Characteristic time
    plot_graphics("Tau", time_tab, table_values[:,6], name_curves+["Theory"], color_curves+["k-."], x_title, y_title_time)
    
    #Relative error for amplitude 
    err_relative = []
    
    for i in range(nb_cases):
        err_relative.append([])
        
        for k in range(len(table_values[i][3])):
            ampl_th = amplitude_th_f(data, time_tab[i][k])
            err_relative[-1].append(abs((table_values[i][3][k] - ampl_th ))/ampl_th )
            #wrong cause not the same time_steps
            #err_relative[-1].append(abs((table_values[i][3][k] - table_values[-1][3][k]))/table_values[-1][3][k])
            
    #for value in %
    err_relative = 100*np.array(err_relative)
    
    plot_graphics("Relative error for amplitude", time_tab[:-1] , err_relative, name_curves, color_curves,x_title, y_title_error)
    
    #Relative error for characteristic time
    
    err_relative = []
    
    for i in range(nb_cases):
        err_relative.append([])
        
        for k in range(len(table_values[i][3])):
            err_relative[-1].append(abs((table_values[i][6][k] - table_values[-1][6][k])/table_values[-1][6][k]))
        
    #for value in %
    err_relative = 100*np.array(err_relative)   
    
    plot_graphics("Relative error for characteristic time", time_tab[:-1]  , err_relative, name_curves, color_curves,x_title, y_title_error)


else :
    ##Same graphs but with the time_scaled abscissa 
    
    #Mean value--all but theory
    plot_graphics("Mean value ", time_tab_scaled[:-1] , table_values[:,0][:-1], name_curves, color_curves,x_title_scaled , y_title)
    
    #Max value--all but theory
    plot_graphics("Max value ", time_tab_scaled[:-1] , table_values[:,1][:-1], name_curves, color_curves, x_title_scaled , y_title)
    
    #Min value--all but theory
    plot_graphics("Min value ", time_tab_scaled[:-1] , table_values[:,2][:-1], name_curves, color_curves, x_title_scaled , y_title)
    
    #Max and Min value
    plot_graphics("Max and min value", np.concatenate((time_tab_scaled, time_tab_scaled)) , np.concatenate((table_values[:,1], table_values[:,2]), axis=0), name_curves+["Theory"]+name_curves+["Theory"],color_curves+["k-."]+color_curves+["k-."], x_title_scaled , y_title)
    
    #Max and Min - centered a (Min + Mean value and Max - mean value)
    plot_graphics("Max and min value centered around 0", np.concatenate((time_tab_scaled, time_tab_scaled)) , np.concatenate((table_values[:,7], table_values[:,8]), axis=0), name_curves+["Theory"]+name_curves+["Theory"],color_curves+["k-."]+color_curves+["k-."], x_title_scaled , y_title)
    
    
    #Amplitude
    plot_graphics("Amplitude", time_tab_scaled , table_values[:,3], name_curves+["Theory"], color_curves+["k-."], x_title_scaled , y_title)
    
    #Amplitude
    plot_graphics("- Log (Amplitude)", time_tab_scaled , table_values[:,4], name_curves+["Theory"], color_curves+["k-."], x_title_scaled , "No dimension")
    
    #Inverse of characteristic time
    plot_graphics("1/Tau", time_tab_scaled , table_values[:,5], name_curves+["Theory"], color_curves+["k-."], x_title_scaled , "$s^{-1}$")
    
    #Characteristic time
    plot_graphics("Tau", time_tab_scaled, table_values[:,6], name_curves+["Theory"], color_curves+["k-."], x_title_scaled , y_title_time)
    
    #Relative error for amplitude 
    err_relative = []
    
    for i in range(nb_cases):
        err_relative.append([])
        
        for k in range(len(table_values[i][3])):
            ampl_th = amplitude_th_f(data, time_tab[i][k])
            err_relative[-1].append(abs((table_values[i][3][k] - ampl_th ))/ampl_th )
            #wrong cause not the same time_steps
            #err_relative[-1].append(abs((table_values[i][3][k] - table_values[-1][3][k]))/table_values[-1][3][k])
            
    #for value in %
    err_relative = 100*np.array(err_relative)
    
    plot_graphics("Relative error for amplitude", time_tab_scaled[:-1] , err_relative, name_curves, color_curves,x_title_scaled , y_title_error)
    
    #Relative error for characteristic time
    
    err_relative = []
    
    for i in range(nb_cases):
        err_relative.append([])
        
        for k in range(len(table_values[i][3])):
            err_relative[-1].append(abs((table_values[i][6][k] - table_values[-1][6][k])/table_values[-1][6][k]))
        
    #for value in %
    err_relative = 100*np.array(err_relative)   
    
    plot_graphics("Relative error for characteristic time", time_tab_scaled[:-1]  , err_relative, name_curves, color_curves,x_title_scaled , y_title_error)