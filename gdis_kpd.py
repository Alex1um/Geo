import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import k0
import scipy.integrate as integrate
import math
from mpmath import invertlaplace


df = pd.read_excel("saphir2.xlsx", sheet_name="Лист2")


# The Bourdet derivative
def bourdet_derivative(p,t):
    n = np.size(p)
    lnt = np.log(t)
    bd = np.zeros(n)
    for i in range(1,n-1):
        bd[i] = [(p[i]-p[i-1])*(lnt[i+1]-lnt[i])/(lnt[i]-lnt[i-1]) +
        (p[i+1]-p[i])*(lnt[i]-lnt[i-1])/(lnt[i+1]-lnt[i])] / (lnt[i+1]-lnt[i-1])
    bd[0] = bd[1]
    bd[n-1] = bd[n-2]
    return bd

# Solution in Laplace space
def laplace_solution(S, Cd, Fcd, s):
    part_1_1 = s*np.sqrt(2*Fcd)*(s**(1/4))*math.tanh(np.sqrt(2/Fcd)*(s**(1/4)))
    part_1 = np.pi/part_1_1
    part_2 = np.pi/(2*s*np.sqrt(s))
    part_3 = 0.4063/(s*(Fcd+0.8997+(4/np.pi)*0.4063*s))
    part_4_1 = integrate.quad(lambda x: k0(math.sqrt((0.732-x)**2 * s)), -1, 1)
    part_4 = (1/(2*s))*float(part_4_1[0])
    res1 = part_1 - part_2 + part_3 + part_4
    part_5_1 = s*res1 + S
    part_5_2 = s + Cd*(s**2)*(s*res1 + S)
    result = part_5_1/part_5_2
    return result

# Inverse laplace transform
def pwd(S, Cd, Fcd, tD, degree=6, method='stehfest'):
    fp = lambda s: laplace_solution(S, Cd, Fcd, s)
    Pwd = np.array([invertlaplace(fp, tti, method=method, degree=degree) for tti in tD])
    return Pwd

# Solution in dimensional parameters
def Pwd_dimension(Pwd):
    part = np.zeros_like(Pwd)
    for i in range(len(Pwd)):
        part[i] = q * B * mu * Pwd[i] / (2 * np.pi * k * h)
    return part


# Parametrs
xf = 5 * 0.3048           # fracture half-length from ft to m
Ct = 5e-10          # total compressibility
mu = 1e-3           # viscosity
poro = 0.3          # rock porosity
B = 1               # volume factor
h = 30 * 0.3048              # total formation thickness from ft to m
q = -1   # flow rate (1 for unit!!!) m3/s
k = 10900 * 1.02e-15          # permeability m2
S = 5               # skin factor
Cs = 1e-7           # wellbore storage coefficient
Fcd = 2             # dimensionless fracture conductivity
Pi = 3910.78 * 6894.759            # пластовое давление из psia в Па

Qinput = np.array([789, 850, 816, 2450, 2410, 976, 942, 920, 912, 865, 835, 830, 0, 0], dtype=float)    # закачка в м3/сут
Tinput = np.array([0, 1.005, 2.393, 3.800, 5.167, 7.1, 9.484, 11.488, 13.414, 15.804, 18.501, 20.968, 23.55, 41.55])   # время в часах

Qinput *= 0.158987
Tinput /= 24

N = 200                # кол-во расчетных точек

t_max = Tinput[-1] + 1     # последнее время отрисовки

# манипуляции с закачкой
Q = np.zeros_like(Qinput)
for i in range(len(Qinput)):
    if i == 0:
        Q[i] = Qinput[i]
    else:
        Q[i] = Qinput[i] - Qinput[i-1]
print(Q)

# перевод времени и закачки в с и м3/с
T = Tinput * 24 * 3600
t_max *= 24 * 3600
Q /= (24 * 3600)

# массив времени
tt = np.linspace(1, t_max, N)

# обезразмеривание времени и Cd
tD = (k * tt) / (poro * mu * Ct * (xf**2))
Cd = Cs / (2*np.pi*poro*Ct*h*(xf**2))

# массив изначального давления
p = np.zeros_like(tt) + Pi

for i in range(0, len(Q)):
    after = tt >= T[i]
    tt1 = tt[after] - T[i]
    td1 = (k * tt1) / (poro * mu * Ct * (xf**2))
    pwd1 = pwd(S, Cd, Fcd, td1)
    pwd1 = np.array(pwd1.tolist(), dtype=float)
    p[after] += 24 * Q[i] * Pwd_dimension(pwd1)

    print(round(i+1/(len(Q))*100), "%")

print(p)

fig, axs = plt.subplots(2, 1, figsize=[8,5])
axs[0].plot((tt/(24*3600)), p, color='red', linewidth=0.5)
axs[0].plot((tt/(24*3600)), np.ones_like(tt)*Pi, color='blue', linewidth=1)
axs[1].step((T / (24 * 3600)), Q, where='post', color='orange', marker='o')

axs[0].plot((df['t']/24), df['p, Pa'], color='blue', linewidth=0.5)

plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
#
# from scipy.special import k0
# import scipy.integrate as integrate
#
# import math
# from mpmath import invertlaplace, exp
#
# # Solution in Laplace space
# def laplace_solution(S, Cd, Fcd, s):
#     part_1_1 = np.sqrt(2*Fcd)*(s**(5/4))*math.tanh(np.sqrt(2/Fcd)*(s**(1/4)))
#     part_1 = np.pi/part_1_1
#     part_2 = np.pi/(2*s*np.sqrt(s))
#     part_3 = 0.4063/(s*(Fcd+0.8997+(4/np.pi)*0.4063*s))
#     part_4_1 = integrate.quad(lambda x: k0(math.sqrt((0.732-x)**2 * s)), -1, 1)
#     part_4 = (1/(2*s))*float(part_4_1[0])
#     res1 = part_1 - part_2 + part_3 + part_4
#     part_5_1 = s*res1 + S
#     part_5_2 = s + Cd*(s**2)*(s*res1 + S)
#     result = part_5_1/part_5_2
#
#     # умножение на скобку
#     part6 = skobka(s)
#     result *= part6
#
#     return result
#
#
# def skobka(s):
#     part = QQ[0] * exp(-tD[0]*s)
#     for i in range(1, len(QQ)):
#         part += (QQ[i] - QQ[i-1]) * exp(-tD[i] * s)
#     return part
#
# # Inverse laplace transform
# # def pwd(S, Cd, Fcd, tD, degree=6, method='stehfest'):
# #     fp = lambda s: laplace_solution(S, Cd, Fcd, s)
# #     Pwd = np.array([invertlaplace(fp, tti, method=method, degree=degree) for tti in tD])
# #     return Pwd
#
# # Inverse laplace transform
# def pwd(S, Cd, Fcd, t, degree=6, method='stehfest'):
#     fp = lambda s: laplace_solution(S, Cd, Fcd, s)
#     Pwd = invertlaplace(fp, t, method=method, degree=degree)
#     return Pwd
#
# # Solution in dimensional parameters
# def Pwd_dimension(Pwd, q, B, mu, k, h):
#     return (q*B*mu*Pwd/(2*np.pi*k*h))
#
#
# # Parametrs
# xf = 100            # fracture half-length
# Ct = 1e-10          # total compressibility
# mu = 1e-3           # viscosity
# poro = 0.1          # rock porosity
# B = 1               # volume factor
# h = 10              # total formation thickness,
# q = -10/24/3600      # flow rate
# k = 1e-15           # permeability
# S = 5               # skin factor
# Cs = 1e-7           # wellbore storage coefficient
# Fcd = 2             # dimensionless fracture conductivity
# Pi = 2e7            # пластовое давление
#
#
# N = 100              # кол-во точек
#
# # История закачки   q        t
# table = np.array([[-1,       0],
#                   [0,      20*24*3600],
#                   [0,      60*24*3600]])
#
# # модуль заполнения массива закачки и времени
# Q = table[:, 0]
# T = table[:, 1]
# tt = np.linspace(1, T[-1]*1.5, N)
# QQ = np.ones_like(tt)
# i = 0
# for ti in tt:
#     for j in range(len(T)):
#         if ti >= T[j]:
#             QQ[i] = Q[j]
#     i += 1
#
# # обезразмеривание времени и Cd
# tD = (k * tt) / (poro * mu * Ct * (xf**2))
# Cd = Cs / (2*np.pi*poro*Ct*h*(xf**2))
#
# PWD = []
# P = []
# for ti in tD:
#     pwd_pa = pwd(S, Cd, Fcd, ti)
#     p = Pi - Pwd_dimension(pwd_pa, q, B, mu, k, h)
#     PWD.append(pwd_pa)
#     P.append(p)
#
# # решение задачи в безразмерной постановке
# # pwd_pa = pwd(S, Cd, Fcd, tD)
#
# # обезразмеривание
# # p = Pi - Pwd_dimension(pwd_pa, q, B, mu, k, h)
#
# # after1 = tt >= t_prod
# # tt2 = tt[after1] - t_prod
# # td2 = (k * tt2) / (poro * mu * Ct * (xf**2))
# # pwd2 = pwd(S, Cd, Fcd, td2)
# # p[after1] += Pwd_dimension(pwd2, q, B, mu, k, h)
#
# fig, axs = plt.subplots(2, 1, figsize=[8,5])
# axs[0].plot((tt/(24*3600)), PWD, color='red', linewidth=2, marker='o')
# # axs[0].plot((tt/(24*3600)), np.ones_like(tt)*Pi, color='blue', linewidth=1)
# axs[1].plot((tt/(24*3600)), QQ, color='orange', linewidth=2, marker='o')
# plt.show()
#
# # plt.plot(tt/(24*3600), p, color='red', linewidth=2, marker='o')
# # plt.xlabel("Time[Days]")
# # plt.ylabel("Pressure[Pa]")
# # # plt.legend(loc='best')
# # plt.grid(True)
# # plt.show()