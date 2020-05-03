import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import mat4py
from SupportFunctions import *

path = r'C:\Host Online'

#The data is arranged in such a way that each simulation case is a .mat file from MATLAB.
# Each simulation case corresponds to one particular wind speed. turbulence level and one fault scenario (pitch misalignment etc).
# If any of these changes, it becomes a new simulation case.
# Each .mat file contains the turbine response (rot. speed, thrust, power etc) of that particular simulation

#first we would like to load the necessary .mat files and store them as dataframes. The collection of these dataframes is stored in a dictionary
# 'MainDict'. From this dict, based on the user input in the dashboard, relevant df will be chosen and worked upon.

global MainDict #Declaring as global variable helps in live debugging
CaseOrder = ['NoTurbPitch0', 'NoTurbPitch1', 'Turb1Pitch0', 'Turb1Pitch1'] #No Turb - No Turbulence; Turb1 - Turbulency level 1, Pitchx - Pitch angle x deg
CaseNames = ['M000P000_T0_S4_Wsp10', 'M000P100_T0_S4_Wsp10', 'M000P000_T1_S1_Wsp10', 'M000P100_T1_S1_Wsp10'] #MATLAB file name follwed during execution of thesis.
MainDict = {}
DfHeaders = open(path + '//' + 'Headers.txt', 'r').read().splitlines() #Names of the .mat columns
for n, Case in enumerate(CaseNames):
    temp = mat4py.loadmat(path + '\\' + Case + '.mat') #mat4py - load .mat to python
    MainDict[CaseOrder[n]] = pd.DataFrame.from_dict(temp['sig'])
    if Case[9:11] == 'T0':
        MainDict[CaseOrder[n]].columns = DfHeaders[:-1] #because for T0 (NoTurb), there is no 'EqWsp' column.
    else:
        MainDict[CaseOrder[n]].columns = DfHeaders

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #A nice stylesheet!
#Now we move on to the app, created using Dash!
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server #app server to deploy the app locally.


dd_options_PitchAngle = create_value_label_for_dropdown(['0 deg', '1 deg'], [0, 1]) #create_value... function in SupportFunctions.py #drop down options for pitch misalignemnt angles
dd_options_xy = create_value_label_for_dropdown(DfHeaders, DfHeaders) #drop down options for x and y values
app.layout = html.Div([                                             #html layout of the app. Verrry similar to standard html components
    html.Div([html.H1('Pitch Misalignment Simulator',style = {'display':'block'}),
              html.P('Welcome to the pitch misalignemnt simulator!', style={'display': 'block'}),
              html.P('Here you can visualize the behaviour of a wind turbine under pitch misalignemnt of one of the blades. '
                     'The turbine used here is the DTU 10MW reference turbine. The results you see here are from a '
                     'database of HAWC2 simulation results. If you wish to know more about the simulations, '
                     'get the data or wish to contribute, please send an email to onerevatatime@gmail.com', style={'display': 'block'}),
              html.P('This webpage is still under developement. Options to simulate more pitch misalignment angles, different levels of turbulence,'
                     'different levels of shear etc. will be added. If you would like to notify errors, wishes for features or wish to contribute, '
                    'please send an email to onerevatatime@gmail.com',style = {'display':'block'})]),

    html.Div([html.H2('No Turbulence'),
              html.P('Enter the two values of the misalignment you wish to analyse in the boxes below'),
              dcc.Dropdown(id='NoTurbPitch1', options=dd_options_PitchAngle
                           , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
              dcc.Dropdown(id='NoTurbPitch2', options=dd_options_PitchAngle
                           , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
              html.P('Enter the x and y variables you wish to visualize in the text boxes below'),
              html.P('x:'),
              dcc.Dropdown(id='NoTurbxdd', options=dd_options_xy
                           , value='Time', style={'width': '50%'}),
              html.P('y:'),
              dcc.Dropdown(id='NoTurbydd', options=dd_options_xy
                           , value='Theta', style={'width': '50%'}),
              dcc.Graph(id='xyNoTurb')], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([html.H1(' '), html.H2('Turbulence'),
              html.P('Enter the two values of the misalignment you wish to analyse in the text boxes below'),
              dcc.Dropdown(id='TurbPitch1', options=dd_options_PitchAngle
                           , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
              dcc.Dropdown(id='TurbPitch2', options=dd_options_PitchAngle
                           , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
              html.P('Enter the x and y variables you wish to visualize in the text boxes below'),
              html.P('x:'),
              dcc.Dropdown(id='Turbxdd', options=dd_options_xy
                           , value='Time', style={'width': '50%'}),
              html.P('y:'),
              dcc.Dropdown(id='Turbydd', options=dd_options_xy
                           , value='Theta', style={'width': '50%'}),
              dcc.Graph(id='xyTurb')
              ], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([
        html.P('PSD of the time series of the chosen y value',
            style={'display': 'inline', 'float': 'left'}),
        #html.Button('Update PSD', id='PSDButtonNoTurb'),
        dcc.Graph(id='PSDNoTurb')],style={'width': '45%','float':'left'}),

    html.Div([
        html.P( 'PSD of the timeseries of the chosen y value'),
        #html.Button('Update PSD', id='PSDButtonTurb',n_clicks=1),
        dcc.Graph(id='PSDTurb')],style={'width': '45%', 'display': 'inline-block'})
])

#calling using the decorator helps extend the functionality of the callback function temporarily
# XY figure for No Turb
@app.callback(Output('xyNoTurb', 'figure'), [Input('NoTurbPitch1', 'value'), Input('NoTurbPitch2', 'value'),
                                             Input('NoTurbxdd', 'value'), Input('NoTurbydd', 'value')])
def update_graph(NoTurbChosenPitch1, NoTurbChosenPitch2, NoTurbChosenxdd, NoTurbChosenydd):
    df1 = MainDict['NoTurbPitch' + str(NoTurbChosenPitch1)]
    df2 = MainDict['NoTurbPitch' + str(NoTurbChosenPitch2)]

    figure = {'data': [go.Scatter(
        y=df1[NoTurbChosenydd],
        x=df1[NoTurbChosenxdd], name=str(NoTurbChosenPitch1) + ' deg'), #first trace (curve) of the graph
        go.Scatter(
            y=df2[NoTurbChosenydd],
            x=df2[NoTurbChosenxdd], name=str(NoTurbChosenPitch2) + ' deg')], #Second trace (curve) of the graph
        'layout': go.Layout(
            yaxis=dict(automargin=True),
            title=NoTurbChosenxdd + ' vs ' + NoTurbChosenydd,
            xaxis_title=NoTurbChosenxdd,
            yaxis_title=NoTurbChosenydd
        )
    }
    return figure


# XY figure for Turb
@app.callback(Output('xyTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                           Input('Turbxdd', 'value'), Input('Turbydd', 'value')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2, TurbChosenxdd, TurbChosenydd):
    df1 = MainDict['Turb1Pitch' + str(TurbChosenPitch1)]
    df2 = MainDict['Turb1Pitch' + str(TurbChosenPitch2)]

    figure = {'data': [go.Scatter(
        y=df1[TurbChosenydd],
        x=df1[TurbChosenxdd], name=str(TurbChosenPitch1) + ' deg'),  #first trace (curve) of the graph
        go.Scatter(
            y=df2[TurbChosenydd],
            x=df2[TurbChosenxdd], name=str(TurbChosenPitch2) + ' deg')], #Second trace (curve) of the graph
        'layout': go.Layout(
            yaxis=dict(automargin=True),
            title=TurbChosenxdd + ' vs ' + TurbChosenydd,
            xaxis_title=TurbChosenxdd,
            yaxis_title=TurbChosenydd
        )
    }
    return figure


# PSD for No Turb  plot
@app.callback(Output('PSDNoTurb', 'figure'), [Input('NoTurbPitch1', 'value'), Input('NoTurbPitch2', 'value'),
                                              Input('NoTurbydd', 'value')])
def update_graph(NoTurbChosenPitch1, NoTurbChosenPitch2, NoTurbChosenydd):
    df1 = MainDict['NoTurbPitch' + str(NoTurbChosenPitch1)]
    df2 = MainDict['NoTurbPitch' + str(NoTurbChosenPitch2)]
    f1, PSD1 = CalcPSD(df1['Time'], df1[NoTurbChosenydd], 0.025)  # delta t is 0.025s always
    f2, PSD2 = CalcPSD(df2['Time'], df2[NoTurbChosenydd], 0.025)  # delta t is 0.025s always
    omega1, omega2 = df1['Omega'].mean() / (2 * np.pi), df2['Omega'].mean() / (2 * np.pi)
    figure = {'data': [go.Scatter(y=PSD1, x=f1, name=str(NoTurbChosenPitch1) + ' deg'),  #PSD of 1st y value in XY plot
                       go.Scatter(y=PSD2, x=f2, name=str(NoTurbChosenPitch2) + ' deg'),  #PSD of 2nd y value in XY plot
                       go.Scatter(y=[PSD2.min(), PSD2.max()], x=[omega1, omega1],        #vertical line to indicate avg. 1P frequency
                                  name = 'Av. rot. speed of ' + str(NoTurbChosenPitch1)+ ' deg',line={'dash':'dash'})],
              'layout': go.Layout(yaxis=dict(automargin = True),
                                  xaxis = dict(range = [0,1]),
                                  title='PSD of ' + NoTurbChosenydd,
                                  xaxis_title='Frequency [Hz]',
                                  yaxis_title='PSD of ' + NoTurbChosenydd + '[Units^2 / Hz]',
                                  yaxis_type='log',
                                  annotations=[dict(x=omega1 * 0.95, y=PSD1.max() * 0.35, text='1P', textangle=-90)])}
    return figure

# PSD of the Turbulent XY plot.
@app.callback(Output('PSDTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                              Input('Turbydd', 'value')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2, TurbChosenydd):
    df1 = MainDict['Turb1Pitch' + str(TurbChosenPitch1)]
    df2 = MainDict['Turb1Pitch' + str(TurbChosenPitch2)]
    f1, PSD1 = CalcPSD(df1['Time'], df1[TurbChosenydd], 0.025)  # delta t is 0.025s always
    f2, PSD2 = CalcPSD(df2['Time'], df2[TurbChosenydd], 0.025)  # delta t is 0.025s always
    omega1, omega2 = df1['Omega'].mean() / (2 * np.pi), df2['Omega'].mean() / (2 * np.pi)
    figure = {'data': [go.Scatter(y=PSD1, x=f1, name=str(TurbChosenPitch1) + ' deg'), #PSD of 1st y value in XY plot
                       go.Scatter(y=PSD2, x=f2, name=str(TurbChosenPitch2) + ' deg'), #PSD of 2nd y value in XY plot
                       go.Scatter(y=[PSD2.min(), PSD2.max()], x=[omega1, omega1],     #vertical line to indicate avg. 1P frequency
                                  name = 'Av. rot. speed of ' + str(TurbChosenPitch1)+ ' deg',line={'dash':'dash'})],
              'layout': go.Layout(yaxis=dict(automargin = True),
                                  xaxis = dict(range = [0,1]),
                                  title='PSD of ' + TurbChosenydd,
                                  xaxis_title='Frequency [Hz]',
                                  yaxis_title='PSD of ' + TurbChosenydd + '[Units^2 / Hz]',
                                  yaxis_type='log',
                                  annotations=[dict(x=omega1 * 0.95, y=PSD1.max() * 0.85, text='1P', textangle=-90)])}
    return figure

app.run_server()
if __name__ == '__main__':
    app.run_server(debug=True) #debug=True -> Live changes in the app as code is being changed!
