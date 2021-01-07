#Realized by Alexandru-Andrei Carmici and Mihai Necula

import numpy as np
from scipy.optimize import curve_fit 
from matplotlib import pyplot as plt
import csv
from os import system
from os import path

def logistic(x, L, k , x0): 
    return L / (1 + np.exp(-k * (x - x0)))

name=input("Enter country code (RO, HU, IT, CH): ")

if name=="RO":
    way = "./database/RomaniaDatabase.csv"
    backupway = "../database/RomaniaDatabase.csv"
elif name=="HU":
    way = "./database/HungaryDatabase.csv"
    backupway = "../database/HungaryDatabase.csv"
elif name=="IT":
    way = "./database/ItalyDatabase.csv"
    backupway = "../database/ItalyDatabase.csv"
elif name=="CH":
    way = "./database/ChinaDatabase.csv"
    backupway = "../database/ChinaDatabase.csv"
else:
    print("ERROR! THIS IS NOT A GOOD COUNTRY ID!")
    name=input()
    exit()


if not path.exists(way) and not path.exists(backupway):
    print("ERROR! THE FILE DOES NOT EXIST!")
    input()
    exit()
elif not path.exists(way):
    way = backupway

x=0
cases=[]
deads=[]

with open(way, 'r') as csvfile:
    reader = csv.reader(csvfile, skipinitialspace = True)
    for row in reader:
        x = x + 1
        deads.append(row[-2])
        cases.append(row[-4])

cases=np.array(cases)
deads=np.array(deads)

X=[]

for i in range(x):
    X.append(i)

X=np.array(X)

param_cases, param_cov_cases = curve_fit(logistic, X, cases)
param_deads, param_cov_deads = curve_fit(logistic, X, deads)

ans_cases = logistic(X, param_cases[0], param_cases[1], param_cases[2])
ans_deads = logistic(X, param_deads[0], param_deads[1], param_deads[2])

way = "./prediction/"
backupway = "../prediction/"

if not path.exists(way) and not path.exists(backupway):
    print("ERROR! THE FILE DOES NOT EXIST!")
    input()
    exit()
elif not path.exists(way):
    way = backupway

with open(way + "cases_prediction.csv", 'w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([name])
    for i in range(x,x+30):
        writer.writerow([i-x+1, int(logistic(i,param_cases[0],param_cases[1],param_cases[2]))])

with open(way + "deads_prediction.csv", 'w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([name])
    for i in range(x,x+30):
        writer.writerow([i-x+1, int(logistic(i,param_deads[0],param_deads[1],param_deads[2]))])

plt.subplot(3, 1, 1)
plt.plot(X, ans_cases, color ='blue', label ="Cases Fitting") 
plt.legend() 
plt.subplot(3, 1, 2)
plt.plot(X, ans_deads, color ='red', label ="Deads Fitting")
plt.legend() 
plt.subplot(3, 1, 3)
plt.plot(X, ans_cases, color ='blue', label ="Cases Fitting") 
plt.plot(X, ans_deads, color ='red', label ="Deads Fitting")
plt.legend() 
plt.show()