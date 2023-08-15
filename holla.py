import pandas as pd
import numpy as np


# input data: <pandas.DataFrame> татнефтевских экселек
# output data: <pandas.DataFrame> с добавленными столбцами ["Q_м3_мес", "W", "dP", 'HI", "DHI"]
def makeHolla(dataframe):
    df = dataframe
    df.insert(len(df.columns), "Q_м3_мес", np.array(df['Q_м3_сут'] / 24 * df['Т_раб']))
    df.insert(len(df.columns), "W", np.cumsum(np.array(df['Q_м3_мес'])))
    df.insert(len(df.columns), "dP", np.array(df['Р_заб'] - np.array(df['Р_пласт'])))
    df.insert(len(df.columns), "HI", np.cumsum(np.array(df['dP'])))
    DHI = np.zeros(len(df))
    for i in range(0, len(df)-1):
        DHI[i] = (df['HI'][i+1] - df['HI'][i]) / ((np.log(df['W'][i+1] / df['W'][i])))
    df.insert(len(df.columns), "DHI", DHI)
    return df


if __name__ == "__main__":
    from dash import Dash, dcc, html

    # example data
    df = pd.read_excel("/Users/lnrsmglln/Downloads/85.xlsx", header=1, parse_dates=[[0,1]])

    # call function
    df = makeHolla(df)

    # example visualization in Dash.plotly
    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(
            figure={
                'data': [
                    {'x': df["W"], 'y': df["HI"], 'type': 'line', 'name': 'HI'},
                    {'x': df["W"][0:-1], 'y': df["DHI"][0:-1], 'type': 'line', 'name': 'DHI'},
                ],
                'layout': {
                    'title': 'График Холла'
                }
            }
        )
    ])

    app.run(debug=True)


