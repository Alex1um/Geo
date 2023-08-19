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
    q = -1  # unit flow rate m3/s
    B = 1  # volume factor
    mu = 1e-3  # viscosity

    part = np.zeros_like(Pwd)
    for i in range(len(Pwd)):
        part[i] = q * B * mu * Pwd[i] / (2 * np.pi * k * h)
    return part


def solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, Fcd, Pi, N=50):
    q = -1  # unit flow rate m3/s
    Ct = 3e-6 / 6894.759  # total compressibility
    mu = 1e-3  # viscosity
    B = 1  # volume factor

    # преобразование типа с дататайма в инт (секунды)
    # T = np.array(Tinput, dtype=f"datetime64[s]").astype(np.int64)
    T = Tinput

    # манипуляции с закачкой
    Q = np.zeros_like(Qinput)
    for i in range(len(Qinput)):
        if i == 0:
            Q[i] = Qinput[i]
        else:
            Q[i] = Qinput[i] - Qinput[i - 1]

    # перевод закачки из м3/сут в м3/с
    Q /= (24 * 3600)

    # массив времени
    tt = np.linspace(1, T[-1]+1, N)

    # обезразмеривание времени и Cd
    # tD = (k * tt) / (poro * mu * Ct * (xf ** 2))
    Cd = Cs / (2 * np.pi * poro * Ct * h * (xf ** 2))

    # массив изначального давления
    p = np.zeros_like(tt) + Pi

    # главный расчетный цикл по ступеням закачки
    for i in range(0, len(Q)):
        print(round(i / (len(Q)) * 100), "%")

        after = tt >= T[i]
        tt1 = tt[after] - T[i]
        td1 = (k * tt1) / (poro * mu * Ct * (xf ** 2))
        pwd1 = pwd(S, Cd, Fcd, td1)
        pwd1 = np.array(pwd1.tolist(), dtype=float)
        p[after] += Q[i] * Pwd_dimension(pwd1)

    print(100, "%")

    # p - Pa
    # tt - seconds

    time = pd.to_datetime(tt, unit='s')

    return p, time


if __name__ == "__main__":

    # Parametrs
    xf = 10 * 0.3048           # fracture half-length from ft to m


    poro = 0.1          # rock porosity

    h = 30 * 0.3048              # total formation thickness from ft to m

    k = 321 * 1.02e-15          # permeability m2
    S = -2               # skin factor
    Cs = 0.0123 / 6894.759 * 0.158987            # wellbore storage coefficient

    Fc = 2790 * 1.02e-15     # dimension fracture conductivity
    Fcd = 0.5             # dimensionless fracture conductivity

    Pi = 3910.78 * 6894.759            # пластовое давление из psia в Па

    Qinput = np.array([789, 850, 816, 2450, 2410, 976, 942, 920, 912, 865, 835, 830, 0, 0], dtype=float)    # закачка в м3/сут
    Tinput = np.array([0, 1.005, 2.393, 3.800, 5.167, 7.1, 9.484, 11.488, 13.414, 15.804, 18.501, 20.968, 23.55, 41.55])   # время в часах

    Qinput *= 0.158987
    Tinput *= 3600

    N = 50                # кол-во расчетных точек

    # применение функции solve_kpd
    pressure, time = solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, Fcd, Pi, N)
    print(pressure)
    print(time)


    fig, axs = plt.subplots(2, 1, figsize=[8,5])
    axs[0].plot(time, pressure, color='red', linewidth=0.5)
    # axs[0].plot(time, np.ones_like(time)*Pi, color='blue', linewidth=1)
    axs[1].step((Tinput), Qinput, where='post', color='orange', marker='o')

    Trealdata = pd.to_datetime(df['t'], unit='h')

    axs[0].plot(Trealdata, df['p, Pa'], color='blue', linewidth=0.5)

    plt.show()