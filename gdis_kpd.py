import numpy as np
import pandas as pd
from scipy.special import k0
import scipy.integrate as integrate
import math
from mpmath import invertlaplace


# The Bourdet derivative
def bourdet_derivative(p,t):
    n = np.size(p)
    lnt = np.log(t)
    bd = np.zeros(n)
    for i in range(1,n-1):
        bd[i] = (p[i]-p[i-1])*(lnt[i+1]-lnt[i])/(lnt[i]-lnt[i-1]) + \
        (p[i+1]-p[i])*(lnt[i]-lnt[i-1])/(lnt[i+1]-lnt[i]) / (lnt[i+1]-lnt[i-1])
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
def Pwd_dimension(Pwd, k, h):
    q = 1  # unit flow rate m3/s
    B = 1  # volume factor
    mu = 1e-3  # viscosity

    part = np.zeros_like(Pwd)
    for i in range(len(Pwd)):
        part[i] = q * B * mu * Pwd[i] / (2 * np.pi * k * h)
    return part


def solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, kfwf, Pi, N=50):
    """

    :param Tinput: массив времени, datetime
    :param Qinput: массив закачек, np.array
    :param xf: полудлина трещины, float
    :param poro: коэффициент пористости, float
    :param h: мощность пласта, float
    :param k: проницаемость пласта, float
    :param S: скин-фактор, float
    :param Cs: wellbore storage коэффициент, float
    :param kfwf: произведение проницаемости трещины на ее раскрытие, float
    :param Pi: пластовое давление, float
    :param N: число точек, int
    :return: Pressure array, Time array, delta Pressure array, log derivative Pressure array
    """
    Fcd = kfwf / (k * xf)
    Ct = 3e-6 / 6894.759  # total compressibility
    mu = 1e-3  # viscosity

    # преобразование типа с дататайма в инт (секунды)
    T = np.array(Tinput, dtype=f"datetime64[s]").astype(np.int64)

    # манипуляции с закачкой
    Q = np.array([])
    tt = np.array([])
    Qt = np.array([])
    kvd_time_start = -1

    j = 0
    for i in range(len(Qinput)):
        if i == 0:
            Q = np.append(Q, Qinput[i])
            Qt = np.append(Qt, T[i])
            j += 1
        else:
            if Qinput[i] != np.sum(Q):
                Q = np.append(Q, Qinput[i] - np.sum(Q[:i-1]))
                Qt = np.append(Qt, T[i])
                j += 1

        if Qinput[i] == 0 and kvd_time_start == -1:
            kvd_time_start = T[i]
        if Qinput[i] != 0 and kvd_time_start != -1:
            kvd_time_start = -1

    # meanrangeQ = np.mean(np.abs(Q))
    # for i in range(1, len(Qinput)):
    #     num = round((T[i] - T[i - 1]) / T[-1] * np.abs(Q[i]) / meanrangeQ * 10 + 5)
    #     if i == 1:
    #         tt = np.append(tt, np.logspace(start=-1,
    #                                        stop=np.log10(T[i]),
    #                                        num=num))
    #     else:
    #         tt = np.append(tt, np.logspace(start=np.log10(T[i-1]),
    #                                        stop=np.log10(T[i]),
    #                                        num=num))
    #
    # print(len(tt))
    # tt = np.sort(tt)

    # перевод закачки из м3/сут в м3/с
    Q /= (24 * 3600)

    # массив времени
    tt = np.linspace(1, T[-1]+1, N)

    # # hardcode добавления точек для более детального LOG графика
    # tt = np.append(tt, np.logspace(np.log10(84781), np.log10(tt[-1]), 100))
    # tt = np.sort(tt)
    # print(len(tt))

    kvd_ind_start = -1
    for i in range(len(tt)):
        if tt[i] >= kvd_time_start and kvd_ind_start == -1:
            kvd_ind_start = i

    # обезразмеривание и Cd
    Cd = Cs / (2 * np.pi * poro * Ct * h * (xf ** 2))

    # массив изначального давления
    p = np.zeros_like(tt) + Pi

    # главный расчетный цикл по ступеням закачки
    for i in range(0, len(Q)):
        print(round(i / float(len(Q)) * 100), "%")
        after = tt >= Qt[i]
        tt1 = tt[after] - Qt[i]
        td1 = (k * tt1) / (poro * mu * Ct * (xf ** 2))
        pwd1 = pwd(S, Cd, Fcd, td1)
        pwd1 = np.array(pwd1.tolist(), dtype=float)
        p[after] -= Q[i] * Pwd_dimension(pwd1, k, h)
    print(100, "%")

    # print("tt = [", end='')
    # for i in tt:
    #     print(i, ", ", end='')
    # print(']')
    #
    # print("p = [", end='')
    # for i in p:
    #     print(i, ", ", end='')
    # print(']')

    # np.save("tt.npy", tt)
    # np.save("p.npy", p)

    # tt = np.load("tt_n250_s0.2947.npy")
    # p = np.load("p_n250_s0.2947.npy")

    def log_data(S, Cd, Fcd, tD, tt):
        # Building a solution with a variation of the skin factor
        pwd_sol = pwd(S, Cd, Fcd, tD)  # more time lost here
        deltaP = np.array(Pwd_dimension(pwd_sol, k, h).tolist(), dtype=float)
        log_derivative_P = bourdet_derivative(deltaP, tt)
        return deltaP, log_derivative_P

    deltaP, log_derivative_P = log_data(S, Cd, Fcd, td1, tt)

    # log_p_start = p[kvd_ind_start]
    # deltaP = p[kvd_ind_start:] - p[kvd_ind_start]
    # deltaP[0] = 1
    t_for_log = tt[kvd_ind_start:] - tt[kvd_ind_start]
    # t_for_log[0] = 1
    # logdP = bourdet_derivative(deltaP, t_for_log)

    # обратный перевод в datetime
    time = pd.to_datetime(tt, unit='s')

    return p, time #, deltaP, log_derivative_P, t_for_log


if __name__ == "__main__":
    from dash import Dash, dcc, html
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # example visualization in Dash.plotly
    app = Dash(__name__)

    # --------------------------------------------------------------------------------

    # Parametrs
    xf = 1.118          # fracture half-length from ft to m = 1.118
    poro = 0.1          # rock porosity
    h = 9.144              # total formation thickness from ft to m
    k = 3.9372e-13          # permeability m2
    S = 0.294684               # skin factor
    Cs = 3.228e-07    #  0,0000003228275274016104      # wellbore storage coefficient
    kfwf = 4.404e-13
    Pi = 26958714.5       # пластовое давление из psia в Па    26958000

    Qinput = np.array([789, 789, 850, 816, 2450, 2410, 976, 942, 920, 912, 865, 835, 830, 0, 0], dtype=float)    # закачка тут в барелл/сут
    Tinput = np.array([0, 0.5, 1.005, 2.393, 3.800, 5.167, 7.1, 9.484, 11.488, 13.414, 15.804, 18.501, 20.968, 23.55, 41.55])   # время в часах

    # Qinput = np.array([789,x 789, 850, 816, 2450, 2410, 976], dtype=float)    # закачка тут в барелл/сут
    # Tinput = np.array([0, 0.5, 1.005, 2.393, 3.800, 5.167, 7.1])   # время в часах

    Tinput = pd.to_datetime(Tinput, unit='h')

    Qinput *= 0.158987      # закачка в м3/сут

    # кол-во расчетных точек
    N = 20

    # применение функции solve_kpd
    pressure, time = solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, kfwf, Pi, N)

    df = pd.read_excel("saphir2.xlsx", sheet_name="Лист2")
    Trealdata = pd.to_datetime(df['t'], unit='h')

    # --------------------------------------------------------------------------------

    fig = make_subplots(rows=2, cols=1,
                        # specs=[[{}, {"rowspan": 2}],
                        #        [{}, None]],
                        row_heights=[0.7, 0.3])
                        # column_widths=[0.6, 0.4])

    fig.add_trace(go.Scatter(x=Trealdata, y=df['p, Pa'], name='Real Data', mode='markers',
                             marker={'line' : {'color' : 'blue', 'width' : 1}, 'size' : 3, 'symbol' : 'x-thin'},
                             ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=pressure, line_shape='spline', name='Solve Data'), row=1, col=1)
    fig.add_trace(go.Scatter(x=Tinput, y=Qinput, line_shape='hv', name='Flow Rate'), row=2, col=1)

    # fig.add_trace(go.Scatter(x=time_for_log, y=deltaP), row=1, col=2)
    #
    # fig.add_trace(go.Scatter(x=time_for_log, y=log_derP), row=1, col=2)
    #
    # fig.update_xaxes(type="log", row=1, col=2)
    # fig.update_yaxes(type="log", row=1, col=2)
    #
    # fig.update_xaxes(type="log", row=2, col=2)
    # fig.update_yaxes(type="log", row=2, col=2)


    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run(debug=True)