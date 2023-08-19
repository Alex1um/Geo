import numpy as np
import pandas as pd


def makeTangs(x_date, y, x_type="s"):
    x = np.array(x_date, dtype=f"datetime64[{x_type}]").astype(np.int64)
    dots = np.sort(np.column_stack((x, y)), axis=0)

    left = np.array([])
    right = np.array([])

    sum_R = 0

    for i in range(2, len(dots) - 1):
        # коэф-ты линии тренда в массиве kx + m вида [k, m]
        k_left, m_left = np.polyfit(dots[:i, 0], dots[:i, 1], 1)

        # функция numpy.poly1d
        left_trend = np.poly1d([k_left, m_left])
        # print('x: ', dots[:i, 0], '\ny: ', dots[:i, 1], '\ntrend: ', left_trend)

        y_left = np.zeros_like(x)
        # y_left = np.full_like(x, x.min())
        for j in range(len(x)):
            y_left[j] = k_left * x[j] + m_left

        R_left = np.corrcoef(y_left[:i], y[:i])[0][1]
        # print('R = ', R_left)
        # print("~~~~~")


        k_right, m_right = np.polyfit(dots[i:, 0], dots[i:, 1], 1)

        right_trend = np.poly1d([k_right, m_right])
        # print('x: ', dots[:i, 0], '\ny: ', dots[:i, 1], '\ntrend: ', left_trend)

        y_right = np.zeros_like(x)
        # y_right = np.full_like(x, x.min())
        for j in range(len(x)):
            y_right[j] = k_right * x[j] + m_right

        R_right = np.corrcoef(y_right[i:], y[i:])[0][1]
        # print('R = ', R_right)

        # print("-----------------")

        if R_left + R_right > sum_R:
            # print(f"соотношение {i} : {len(x) - i}")
            # print(f"R = {R_left} + {R_right} = {R_left + R_right} > {sum_R}")
            left = [k_left, m_left]
            right = [k_right, m_right]
            sum_R = R_left + R_right
        # else:
        #     print(f"соотношение {i} : {len(x) - i}")
        #     print(f"R = {R_left} + {R_right} = {R_left + R_right} < {sum_R}")

    for i in range(len(x)):
        y_left[i] = left[0] * x[i] + left[1]
        y_right[i] = right[0] * x[i] + right[1]

    k1 = left[0]
    k2 = right[0]
    m1 = left[1]
    m2 = right[1]
    y_ = (m1 * k2 - m2 * k1) / (k2 - k1)
    x_ = (y_ - m1) / k1
    cross = [pd.to_datetime(x_, unit=x_type), y_]
    # print(cross)

    return y_left, y_right, cross


if __name__ == "__main__":
    from dash import Dash, dcc, html
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    # example data
    y = [30578602.76661648, 27942638.217440456, 33452413.573210157, 36498284.40489721, 39679580.7463391,
         41985151.10131766, 42530774.84989407, 43084317.89541166, 43636282.715523936]
    x = [518400, 259200, 777600, 1036800, 1296000, 1555200, 1814400, 2073600, 2332800]

    # 5 dots
    # y = [27942638.217440456, 33452413.573210157, 36498284.40489721, 39679580.7463391,
    #      41985151.10131766, 43084317.89541166, 43536282.715523936]
    # x = [259200, 1036800, 1296000, 1555200, 1814400, 2073600, 2332800]

    # call function
    y_left, y_right, cross = makeTangs(x, y)

    # example visualization in Dash.plotly
    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(
            figure={
                'data': [
                    {'x': x, 'y': y, 'type': 'scatter', 'name': 'input data'},
                    {'x': x, 'y': y_left, 'mode': 'lines', 'opacity': 0.5, 'name': 'left trend'},
                    {'x': x, 'y': y_right, 'mode': 'lines', 'opacity': 0.5, 'name': 'right trend'},
                    {'x': cross[0], 'y': cross[1], 'type': 'scatter', 'name': 'P fracture'}
                ],
                'layout': {
                    'title': 'SRTest'
                }
            }
        )]
    )

    app.run(debug=True)

