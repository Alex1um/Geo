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
    kvd_time_start = -1

    j = 0
    for i in range(len(Qinput)):
        if i == 0:
            Q = np.append(Q, Qinput[i])
            j += 1
        else:
            if Qinput[i] != Q[j-1]:
                Q = np.append(Q, Qinput[i] - np.sum(Q[:i-1]))
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
        print(round(i / (len(Q)) * 100), "%")
        after = tt >= T[i]
        tt1 = tt[after] - T[i]
        td1 = (k * tt1) / (poro * mu * Ct * (xf ** 2))
        pwd1 = pwd(S, Cd, Fcd, td1)
        pwd1 = np.array(pwd1.tolist(), dtype=float)
        p[after] -= Q[i] * Pwd_dimension(pwd1, k, h)
    print(100, "%")
    
    # tt = np.array([1.0, 3836.3846153846152, 7671.7692307692305, 11507.153846153846, 15342.538461538461, 19177.923076923078,
    #       23013.30769230769, 26848.692307692305, 30684.076923076922, 34519.46153846154, 38354.846153846156,
    #       42190.230769230766, 46025.61538461538, 49861.0, 53696.38461538461, 57531.76923076923, 61367.153846153844,
    #       65202.53846153846, 69037.92307692308, 72873.30769230769, 76708.69230769231, 80544.07692307692,
    #       84379.46153846153, 88214.84615384616, 92050.23076923077, 95885.61538461538, 99721.0, 103556.38461538461,
    #       107391.76923076922, 111227.15384615384, 115062.53846153845, 118897.92307692308, 122733.30769230769,
    #       126568.6923076923, 130404.07692307692, 134239.46153846153, 138074.84615384616, 141910.23076923075,
    #       145745.61538461538, 149581.0])

    # p = np.array([26954280.8144143, 26434470.252233457, 26399742.89518385, 26405712.922623422, 25427357.131658737,
    #      25355867.573864568, 25317554.450483505, 26123417.679987136, 26190439.2279156, 26224109.460986204,
    #      26235316.892299447, 26251480.57728031, 26254936.752421543, 26260839.231092878, 26261514.355615646,
    #      26287001.827897854, 26290894.45255737, 26291566.53694003, 26309782.677265055, 26310700.11781603,
    #      26313699.560711943, 26313747.046480596, 26313537.220194597, 26832174.302518718, 26858078.097053878,
    #      26872207.73074058, 26881734.409450937, 26888941.652309243, 26894668.87988621, 26899239.73582232,
    #      26903161.28473018, 26906573.64454287, 26909475.290901355, 26912189.854606807, 26914464.41997173,
    #      26916523.73674312, 26918369.57409275, 26920069.89452821, 26921559.22323988, 26923118.288254134])

    Pstart = p[kvd_ind_start]
    deltaP = np.zeros_like(p[kvd_ind_start:]) - Pstart + p[kvd_ind_start:]
    logdP = bourdet_derivative(deltaP, tt[kvd_ind_start:])



    # обратный перевод в datetime
    time = pd.to_datetime(tt, unit='s')

    return p, time, deltaP, logdP


if __name__ == "__main__":
    from dash import Dash, dcc, html
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # example visualization in Dash.plotly
    app = Dash(__name__)

    # --------------------------------------------------------------------------------

    # Parametrs
    xf = 3.67 * 0.3048           # fracture half-length from ft to m
    poro = 0.1          # rock porosity
    h = 30 * 0.3048              # total formation thickness from ft to m
    k = 386 * 1.02e-15          # permeability m2
    S = 0.294684               # skin factor
    Cs = 0.014 / 6894.759 * 0.158987            # wellbore storage coefficient
    kfwf = 4.40421492e-13
    Pi = 3910.03 * 6894.759            # пластовое давление из psia в Па

    Qinput = np.array([789, 789, 850, 816, 2450, 2410, 976, 942, 920, 912, 865, 835, 830, 0, 0], dtype=float)    # закачка тут в барелл/сут
    Tinput = np.array([0, 0.5, 1.005, 2.393, 3.800, 5.167, 7.1, 9.484, 11.488, 13.414, 15.804, 18.501, 20.968, 23.55, 41.55])   # время в часах

    Tinput = pd.to_datetime(Tinput, unit='h')

    Qinput *= 0.158987      # закачка в м3/сут

    # кол-во расчетных точек
    N = 20

    # применение функции solve_kpd
    pressure, time, deltaP, log_derP = solve_kpd(Tinput, Qinput, xf, poro, h, k, S, Cs, kfwf, Pi, N)

    df = pd.read_excel("saphir2.xlsx", sheet_name="Лист2")
    Trealdata = pd.to_datetime(df['t'], unit='h')

    # --------------------------------------------------------------------------------


    fig = make_subplots(rows=2, cols=2,
                        specs=[[{}, {"rowspan": 2}],
                               [{}, None]],
                        row_heights=[0.7, 0.3],
                        column_widths=[0.6, 0.4])

    fig.add_trace(go.Scatter(x=Trealdata, y=df['p, Pa'], name='Real Data', mode='markers',
                             marker={'line' : {'color' : '#87cefa', 'width' : 1}, 'size' : 3, 'symbol' : 'x-thin'},
                             ),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=pressure, line_shape='spline', name='Num Data'), row=1, col=1)
    fig.add_trace(go.Scatter(x=Tinput, y=Qinput, line_shape='hv', name='Flow Rate'), row=2, col=1)

    fig.add_trace(go.Scatter(x=np.array(Tinput, dtype=f"datetime64[h]").astype(np.int64), y=deltaP), row=1, col=2)
    print(deltaP)
    fig.add_trace(go.Scatter(x=np.array(Tinput, dtype=f"datetime64[h]").astype(np.int64), y=log_derP), row=1, col=2)

    fig.update_xaxes(type="log", row=1, col=2)
    fig.update_yaxes(type="log", row=1, col=2)


    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run(debug=True)