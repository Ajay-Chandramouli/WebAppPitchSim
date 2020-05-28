import sys
packages_path = '/home/chandramouli/.local/lib/python3.6/site-packages/'
if packages_path not in sys.path:
    sys.path.append(packages_path)

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import mat4py
import base64
from SupportFunctions import *

path = '/home/chandramouli/'
global MainDict #Declaring as global variable helps in live debugging
CaseOrder = ['NoTurbPitch0', 'NoTurbPitch1', 'Turb1Pitch0', 'Turb1Pitch1'] #No Turb - No Turbulence; Turb1 - Turbulency level 1, Pitchx - Pitch angle x deg
CaseNames = ['M000P000_T0_S4_Wsp10', 'M000P100_T0_S4_Wsp10', 'M000P000_T1_S1_Wsp10', 'M000P100_T1_S1_Wsp10'] #MATLAB file name follwed during execution of thesis.
MainDict = {}
DfHeaders = open(path  + '//'+'Headers.txt', 'r').read().splitlines() #Names of the .mat columns
DfHeadersDesc = open(path  + 'HeadersDescription.txt', 'r').read().splitlines() #Descriptions of the .mat columns
DfHeadersUnits = open(path  + 'HeadersUnits.txt', 'r').read().splitlines() #Units of the .mat columns

for n, Case in enumerate(CaseNames):
    temp = mat4py.loadmat(path + Case + '.mat') #mat4py - load .mat to python
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
dd_options_xy = create_value_label_for_dropdown(DfHeadersDesc, DfHeaders) #drop down options for x and y values
r_options_PSD_yaxis = create_value_label_for_dropdown(['Linear','Log'],['linear','log']) #radio options for PSD yaxis scale
dd_options_Wsp = create_value_label_for_dropdown(['10m/s', '12m/s','14m/s','16m/s','20m/s'],[10,12,14,16,20])
dd_options_Seed_Info = create_value_label_for_dropdown(['Yes','No'],[1,0])
#DTU 10 MW turbine file image
image_filename = path + 'DTU10MWresized.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
app.layout = html.Div([                                             #html layout of the app. Verrry similar to standard html components
    html.Div([html.H1('Wind Turbine Pitch Angle Misalignment Simulator',style = {'display':'block'}),
              html.P('Welcome to the pitch angle misalignment simulator!', style={'display': 'block','font-weight':'bold'}),
              html.P('Pitch angle misalignment or pitch misalignment for short is a faulty state of operation of the wind turbine in which atleast one of the blades is not '
                     'oriented at the optimal pitch angle. Because of this, the torque on the rotating shaft will not be balanced, leading to aerodynamic asymmetry in addition to sub optimal power production of the turbine. '
                     'According to some studies, each degree of deviation from the optimal pitch angle setting can cause a 2-3% decrease in the Annual Energy Production. Broadly, there are two kinds of pitch misalignment - individual pitch misalignment '
                     'and collective pitch misalignment. In individual pitch imbalance, the blades are misaligned relative to each other and at least one of the blades may or may not be aligned at the  '
                     'optimal pitch angle. In collective pitch imbalance, all the blades are simultaneously misaligned from the optimal pitch angle. In the rest of this page, we will deal with individual '
                     'pitch misalignment. '),
              html.P('What this webpage is about', style={'display': 'block','font-weight':'bold'}),
              html.P(' In this webpage, you can interactively visualize yourself the response of a wind turbine under pitch angle misalignment of one of the blades and different environmental conditions. '
                     ' By response, it is meant of the forces, moments etc. at specific points on the turbine. We will also discuss some methods to detect pitch angle misalignment '
                      'based on the response of the turbine. '),
              html.P(
                  'This app is relatively more friendly to use for people with a background in wind turbine loads (Sorry for that! It is being updated to target a wider audience). '
                  'This webpage is still under developement. More context to the situation, background, options to simulate more pitch misalignment angles, more wind speeds, different levels of turbulence,'
                  'different levels of shear etc. will be added. The results you see here are from a database of HAWC2 simulation results. If you would like to notify errors, convey wishes for features, wish to '
                  'contribute, or get the data of the simulations, please send an email to onerevatatime@gmail.com', style={'display': 'block'}),
            html.P('Turbine Information', style={'display': 'block','font-weight':'bold'}),
             html.P('The turbine analysed here is the DTU 10MW virtual turbine. More details about the turbine can be found at the HAWC2 website. The figure below shows a sketch of the '
             'turbine, along with the different local co-ordinate systems formulated relative to the components of the turbine. Responses measured with reference to these '
             'co-ordinate systems will be used throughout in this webpage.  ', style={'display': 'block'}),
             html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),

              html.P(
                  'Let\'s get started!', style={'display': 'block','font-weight':'bold'}),

              html.P('Let us start by defining a \'scenario\' which is a state of a turbine with pitch angle misalignment of one of the blades. You can simulate the response of the turbine for '
                  'two scenarios with different pitch angle misalignements, to compare the results for both scenarios. For ex. if you choose a value \'x deg\' for a scenario, it means that in that '
                  'scenario, ONE OF THE BLADES, specifically, the blade number 1 is is relatively misaligned by x deg with respect to the other two blades. Each scenario corresponds to a 10 minute period of incident wind on the turbine. '
                  , style={'display': 'block'}),
              html.P(' ')]),

    # html.Div([html.H2('No Turbulence'),
    #           html.P('Enter the two values of the misalignment you wish to analyse in the boxes below'),
    #           dcc.Dropdown(id='NoTurbPitch1', options=dd_options_PitchAngle
    #                        , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
    #           dcc.Dropdown(id='NoTurbPitch2', options=dd_options_PitchAngle
    #                        , value='0 deg', style={'width': '50%', 'display': 'inline-block'}),
    #           html.P('Enter the x and y variables you wish to visualize in the text boxes below'),
    #           html.P('x:'),
    #           dcc.Dropdown(id='NoTurbxdd', options=dd_options_xy
    #                        , value='Time', style={'width': '50%'}),
    #           html.P('y:'),
    #           dcc.Dropdown(id='NoTurbydd', options=dd_options_xy
    #                        , value='Theta', style={'width': '50%'}),
    #           dcc.Graph(id='xyNoTurb')], style={'width': '45%', 'display': 'inline-block'}),

    html.Div([html.H1(' '), html.H5('For now let us consider a turbulent wind with a mean wind speed of 10m/s and a turbulence intensity of 12% for a 10 min period. '),
              html.P('Enter the two values of the pitch angle misalignment of ONE OF THE BLADES you wish to analyse '
                     'in the boxes below. The two values correspond to the two different scenarios. (Tip: If you choose the value as 0 deg for one scenario and x deg )'),
              html.P('Scenario 1:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='TurbPitch1', options=dd_options_PitchAngle
                           , value='Scenario 1', style={'width': '150px', 'verticalAlign':'middle','display': 'inline-block',
                                                        'margin-right': '30px'}),
              html.P('Scenario 2:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='TurbPitch2', options=dd_options_PitchAngle
                           , value='Scenario 2', style={'width': '150px','verticalAlign':'middle', 'display': 'inline-block','margin-right': '30px'}),
              html.P('Wind Speed:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='Wsp', options=dd_options_Wsp
                           ,value=10, style={'width': '150px','verticalAlign':'middle', 'display': 'inline-block','margin-right': '30px'}),
              html.P('Exactly same wind conditions?:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='SeedInfo', options=dd_options_Seed_Info
                           , style={'width': '150px', 'verticalAlign': 'middle', 'display': 'inline-block'}),
              html.H5('X-Y plot'),
              html.P('Enter the x and y variables you wish to visualize in the text boxes below. The graph below will show you the variation of the chosen y vs x for the two different scenarios.'),
              html.P('x:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='Turbxdd', options=dd_options_xy
                           , value='Time', style={'width': '300px','display':'inline-block','margin-right': '110px','verticalAlign':'middle'}),
              html.P('y:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='Turbydd', options=dd_options_xy
                           , value='NAcx',style={'width': '300px','display':'inline-block','margin-right': '15px','verticalAlign':'middle'}),
              dcc.Loading(id = 'LoadingIcon',children = [dcc.Graph(id='xyTurb')],type = 'default')
              ], style={'width': '90%', 'display': 'block'}),

    # html.Div([
    #     html.P('PSD of the time series of the chosen y value',
    #         style={'display': 'inline', 'float': 'left'}),
    #     #html.Button('Update PSD', id='PSDButtonNoTurb'),
    #     dcc.Graph(id='PSDNoTurb')],style={'width': '45%','float':'left'}),

    html.Div([html.H5('Power Spectral Density plots'),
        html.P( 'A Power Spectral Density (PSD) is often very useful to identify frequencies which contain the most energy of a timeseries. '
                'PSD of the timeseries of the chosen y values are shown below. Analysing such frequencies of the various channels '
                '(y values) can help identify  the vibrations that can be used to detect pitch angle misalignment. '
                'For ex. if the chosen pitch misalignments are 0 deg and 1 deg and y value as NAcx, a clear peak in the PSD of the 1 deg scenario as compared to 0 deg can be seen at a certain frequency '
                '(specifically, the average 1P frequency = the average rotor speed in Hz). '
                'Other y values can be experimented with to identify suitable channels for detection. Kindly also note the option to change the y-axis type '),
        #html.Button('Update PSD', id='PSDButtonTurb',n_clicks=1),
        dcc.RadioItems(id='PSDTurbaxis-type', options=r_options_PSD_yaxis,
                value='log', labelStyle={'display': 'inline-block'},style={'display':'inline-block'}),
        dcc.Loading(id = 'LoadingIcon2',children = [dcc.Graph(id='PSDTurb')],type = 'default')],style={'width': '90%', 'display': 'inline-block'})
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

    #For the title and units
    idx_x = IndicesinList(DfHeaders,TurbChosenxdd)[0]
    idx_y = IndicesinList(DfHeaders,TurbChosenydd)[0]
    TurbChosenxddLabel = DfHeadersDesc[idx_x]
    TurbChosenyddLabel = DfHeadersDesc[idx_y]
    TurbChosenxddUnits = DfHeadersUnits[idx_x]
    TurbChosenyddUnits = DfHeadersUnits[idx_y]

    figure = {'data': [go.Scatter(
        y=df1[TurbChosenydd],
        x=df1[TurbChosenxdd], name=str(TurbChosenPitch1) + ' deg'),  #first trace (curve) of the graph
        go.Scatter(
            y=df2[TurbChosenydd],
            x=df2[TurbChosenxdd], name=str(TurbChosenPitch2) + ' deg')], #Second trace (curve) of the graph
        'layout': go.Layout(
            yaxis=dict(automargin=True),
            title=TurbChosenxddLabel + ' vs ' + TurbChosenyddLabel,
            xaxis_title=TurbChosenxdd+ ' ' +TurbChosenxddUnits,
            yaxis_title=TurbChosenydd+ ' ' +TurbChosenyddUnits
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
                                  name = 'Av. 1P freq ',line={'dash':'dash'})],
              'layout': go.Layout(yaxis=dict(automargin = True),
                                  xaxis = dict(range = [f1[1],1]),
                                  title='PSD of ' + NoTurbChosenydd,
                                  xaxis_title='Frequency [Hz]',
                                  yaxis_title='PSD of ' + NoTurbChosenydd + '[Units^2 / Hz]',
                                  yaxis_type='log',
                                  annotations=[dict(x=omega1 * 0.95, y=PSD1.max() * 0.35, text='1P', textangle=-90)])}
    return figure

# PSD of the Turbulent XY plot.
@app.callback(Output('PSDTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                              Input('Turbydd', 'value'),Input('PSDTurbaxis-type','value')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2, TurbChosenydd, AxisType):
    df1 = MainDict['Turb1Pitch' + str(TurbChosenPitch1)]
    df2 = MainDict['Turb1Pitch' + str(TurbChosenPitch2)]
    #For Title and units
    idx_y = IndicesinList(DfHeaders,TurbChosenydd)[0]
    TurbChosenyddLabel = DfHeadersDesc[idx_y]
    TurbChosenyddUnits = DfHeadersUnits[idx_y]
    #AxisType = 'linear' if AxisType1 == 'Linear' else 'log'
    f1, PSD1 = CalcPSD(df1['Time'], df1[TurbChosenydd], 0.025)  # delta t is 0.025s always
    f2, PSD2 = CalcPSD(df2['Time'], df2[TurbChosenydd], 0.025)  # delta t is 0.025s always
    omega1, omega2 = df1['Omega'].mean() / (2 * np.pi), df2['Omega'].mean() / (2 * np.pi)
    figure = {'data': [go.Scatter(y=PSD1, x=f1, name=str(TurbChosenPitch1) + ' deg'), #PSD of 1st y value in XY plot
                       go.Scatter(y=PSD2, x=f2, name=str(TurbChosenPitch2) + ' deg'), #PSD of 2nd y value in XY plot
                       go.Scatter(y=[PSD2.min(), PSD2.max()], x=[omega1, omega1],     #vertical line to indicate avg. 1P frequency
                                  name = 'Av. 1P freq ',line={'dash':'dash'})],
              'layout': go.Layout(yaxis=dict(automargin = True),
                                  xaxis = dict(range = [f1[1],1]),
                                  title='PSD of ' + TurbChosenyddLabel,
                                  xaxis_title='Frequency [Hz]',
                                  yaxis_title='PSD ' + '[('+ TurbChosenyddUnits[1:-1]+')' + '<sup>2</sup>' + '/Hz]',
                                  yaxis_type=AxisType)}
                                  #,annotations=[dict(x=omega1 * 0.95, y=PSD1.max() * 0.35, text='1P', textangle=-90)])}
    return figure

#app.run_server()
if __name__ == '__main__':
    app.run_server(debug=True) #debug=True -> Live changes in the app as code is being changed!
