import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import mat4py
from SupportFunctions import *
import json
import socket
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #A nice stylesheet!
#Now we move on to the app, created using Dash!
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#
server = app.server #app server to deploy the app locally.
if socket.gethostname() == 'Chandramouli':
    path = r'C:\Host Online'
else:
    path = '/home/chandramouli/'

#The data is arranged in such a way that each simulation case is a .mat file from MATLAB.
# Each simulation case corresponds to one particular wind speed. turbulence level and one fault scenario (pitch misalignment etc).
# If any of these changes, it becomes a new simulation case.
# Each .mat file contains the turbine response (rot. speed, thrust, power etc) of that particular simulation

#first we would like to load the necessary .mat files and store them as dataframes. The collection of these dataframes is stored in a dictionary
# 'MainDict'. From this dict, based on the user input in the dashboard, relevant df will be chosen and worked upon.
"""
global MainDict #Declaring as global variable helps in live debugging
CaseOrder = ['NoTurbPitch0', 'NoTurbPitch1', 'Turb1Pitch0', 'Turb1Pitch1'] #No Turb - No Turbulence; Turb1 - Turbulency level 1, Pitchx - Pitch angle x deg
CaseNames = ['M000P000_T0_S4_Wsp10', 'M000P100_T0_S4_Wsp10', 'M000P000_T1_S1_Wsp10', 'M000P100_T1_S1_Wsp10'] #MATLAB file name follwed during execution of thesis.
MainDict = {}
DfHeaders = open(path + '//' + 'Headers.txt', 'r').read().splitlines() #Names of the .mat columns
DfHeadersDesc = open(path + '//' + 'HeadersDescription.txt', 'r').read().splitlines() #Descriptions of the .mat columns
DfHeadersUnits = open(path + '//' + 'HeadersUnits.txt', 'r').read().splitlines() #Units of the .mat columns
for n, Case in enumerate(CaseNames):
    temp = mat4py.loadmat(path + '\\' + Case + '.mat') #mat4py - load .mat to python
    MainDict[CaseOrder[n]] = pd.DataFrame.from_dict(temp['sig'])
    if Case[9:11] == 'T0':
        MainDict[CaseOrder[n]].columns = DfHeaders[:-1] #because for T0 (NoTurb), there is no 'EqWsp' column.
    else:
        MainDict[CaseOrder[n]].columns = DfHeaders
"""
DfHeaders = open(path + '//' + 'Headers.txt', 'r').read().splitlines()  # Names of the .mat columns
DfHeadersDesc = open(path + '//' + 'HeadersDescription.txt',
                     'r').read().splitlines()  # Descriptions of the .mat columns
DfHeadersUnits = open(path + '//' + 'HeadersUnits.txt', 'r').read().splitlines()  # Units of the .mat columns
#get the text dict ready for the layout
Text = Text2DictForLayout(path+'//'+'Text.txt')

dd_options_PitchAngle = create_value_label_for_dropdown(['0 deg', '1 deg','3 deg'], [0, 1,2]) #create_value... function in SupportFunctions.py #drop down options for pitch misalignemnt angles
dd_options_xy = create_value_label_for_dropdown(DfHeadersDesc, DfHeaders) #drop down options for x and y values
r_options_PSD_yaxis = create_value_label_for_dropdown(['Linear','Log'],['linear','log'])
dd_options_Wsp = create_value_label_for_dropdown(['10m/s', '12m/s','14m/s','16m/s','20m/s'],[10,12,14,16,20])
dd_options_Seed_Info = create_value_label_for_dropdown(['Yes','No','Success1'],[1,0,1])

image_filename = path + '//'+ 'DTU10MWresized.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([                                             #html layout of the app. Verrry similar to standard html components
    html.Div([html.H1(Text['Main Heading'],style = {'display':'block'}),
              html.P(Text['Bold Welcome'], style={'display': 'block','font-weight':'bold'}),
              html.P(Text['What is pitch misalignment']),
              html.P('What is this webpage about?', style={'display': 'block','font-weight':'bold'}),
              html.P(Text['Page description']),
              html.Br(),
              html.P(Text['Disclaimer'], style={'display': 'block'}),
              html.H5('Notes Before getting Started'),
              html.P('Turbine Information',style={'font-weight':'bold'}),
              html.P(Text['Turbine Info'], style={'display': 'block'}),
              html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
              #html.P('Wind conditions',style={'font-weight':'bold'}),
              html.P(Text['Varying wind'],style = {'display':'block'}),
              html.P('Shear',style = {'font-weight':'bold'}),
              html.P(Text['Shear']),
              html.P('Turbulence Intensity',style = {'font-weight':'bold'}),
              html.P(Text['TI']),
              html.P('Imbalance - Effect and Detection',style = {'font-weight':'bold'}),
              html.P(Text['Imbalance Description'])
              ]),
              #html.P('Let\'s get started!', style={'display': 'block','font-weight':'bold'}),
    html.Div([#html.H4('No Pitch Misalignment'),
        #html.P(Text['No misalignment block']),
#html.P('Let\'s get started!', style={'display': 'block','font-weight':'bold'}),
        #html.P(Text['PSD plot description'])
        ]),

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

    html.Div([#html.H4(Text['TI and wind conditions description']),
              html.H4('Let\'s get started!'),
              html.P(Text['Scenario description'], style={'display': 'block'}),
              html.P(Text['Enter values and description']),
              html.P('Scenario 1:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='TurbPitch1', options=dd_options_PitchAngle
                           , value='Scenario 1', style={'width': '150px', 'verticalAlign':'middle','display': 'inline-block',
                                                        'margin-right': '30px'}),
              html.P('Scenario 2:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='TurbPitch2', options=dd_options_PitchAngle
                           , value='Scenario 2', style={'width': '150px','verticalAlign':'middle', 'display': 'inline-block','margin-right': '30px'}),
              html.P('Wind Speed:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='Wsp', options=dd_options_Wsp
                           , value=10, style={'width': '150px','verticalAlign':'middle', 'display': 'inline-block','margin-right': '30px'}),
              html.P('Exactly same wind conditions?:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='SeedInfo', options=dd_options_Seed_Info
                           , style={'width': '150px', 'verticalAlign': 'middle', 'display': 'inline-block'}),
              html.H4('Visualizing turbine responses for the considered wind conditions'),
              dcc.Loading(id = 'LoadingIcon2',children = html.Div(id = 'Loading2',style={'width':'45%','display':'inline-block'}),type = 'cube'),
              html.P(Text['XY plot description']),
              html.P('x:',style={'display':'inline-block','margin-left': '75px','margin-right': '15px'}),
              dcc.Dropdown(id='Turbxdd', options=dd_options_xy
                           , value='Time', style={'width': '400px','display':'inline-block','margin-right': '30px','verticalAlign':'middle'}),
              html.P('y:',style={'display':'inline-block','margin-right': '15px'}),
              dcc.Dropdown(id='Turbydd', options=dd_options_xy
                           , value='NAcx',style={'width': '400px','display':'inline-block','margin-right': '15px','verticalAlign':'middle'}),
              html.Br(),
              dcc.Loading(id = 'LoadingIcon',children = [dcc.Graph(id='InputTurb',style={'width':'45%','right-margin':'5%','display':'inline-block'}),
              dcc.Graph(id='xyTurb',style={'width':'45%','display':'inline-block'})]
                                ,type='default'),
    html.Div(id='MainDict',style={'display': 'none'})]
              , style={'width': '100%', 'display': 'block'}),

    html.Div([ html.H5('Power Spectral Density'),
        #html.P( Text['PSD plot description']),
        html.P('Y axis type: ',style={'display':'inline-block','margin-right': '15px'}),
        dcc.RadioItems(id='PSDTurbaxis-type', options=r_options_PSD_yaxis,
                value='log', labelStyle={'display': 'inline-block'},style={'display':'inline-block'}),
        #html.Button('Update PSD', id='PSDButtonTurb',n_clicks=1),
        dcc.Graph(id='PSDTurb',style={'width':'100%'})],style={'width': '100%', 'display': 'inline-block'}),

    html.Div([html.H5 ('References'),
              html.P(Text['References'])])
])

@app.callback([Output('MainDict','children'),Output('Loading2','children')],[Input('TurbPitch1','value'), Input('TurbPitch2','value'),
                                             Input('Turbxdd', 'value'), Input('Turbydd', 'value'),Input('Wsp','value'),
                                                Input('SeedInfo','value')])
def dynamic_load(Pitch1,Pitch2,Turbxdd,Turbydd,Wsp,SeedInfo):
    Seed1,Seed2 = (1,1) if SeedInfo ==1 else (1,0)
    CaseNames = ['M000P'+str(Pitch1)+'00_T1_S1_Wsp'+str(Wsp)+'_s'+str(Seed1),'M000P'+str(Pitch2)+'00_T1_S1_Wsp'+str(Wsp)+'_s'+str(Seed2)]
    CaseOrder = ['Turb1Pitch'+str(Pitch1),'Turb1Pitch'+str(Pitch2)]
    Dict = {}
    MainDict={}
    for n, Case in enumerate(CaseNames):
        temp = mat4py.loadmat(path + '\\' + Case + '.mat')  # mat4py - load .mat to python
        Dict[CaseOrder[n]] = pd.DataFrame.from_dict(temp['sig'])
        if Case[9:11] == 'T0':
            Dict[CaseOrder[n]].columns = DfHeaders[:-1]  # because for T0 (NoTurb), there is no 'EqWsp' column.
        else:
            Dict[CaseOrder[n]].columns = DfHeaders
        list = GetUniqueinList([Turbxdd,Turbydd,'Time','Vo','Omega']) #Time, Omega and Vo are always needed because of the input V figure and PSD
        Dict[CaseOrder[n]] = Dict[CaseOrder[n]][list]
    for key in Dict.keys():
         MainDict[key] = Dict[key].to_json(orient='split')

    return json.dumps(MainDict),[]

"""
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
"""

# Input V figure for Turb
@app.callback(Output('InputTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                              Input('MainDict','children')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2,MainDict1):
    MainDict = json.loads(MainDict1)
    df1 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch1)],orient='split')
    df2 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch2)],orient='split')

    name1 =str(TurbChosenPitch1) + ' deg' if TurbChosenPitch1!=2 else str(TurbChosenPitch1+1) + ' deg'
    name2 = str(TurbChosenPitch2)+ ' deg' if TurbChosenPitch2!= 2 else str(TurbChosenPitch2 + 1)+ ' deg'
    figure = {'data': [go.Scatter(
        y=df1['Vo'],
        x=df1['Time'], name=name1),  #first trace (curve) of the graph
        go.Scatter(
            y=df2['Vo'],
            x=df2['Time'], name=name2)], #Second trace (curve) of the graph
        'layout': go.Layout(
            yaxis=dict(automargin=True),
            title='Input velocity profiles',
            xaxis_title='Time',
            yaxis_title='Wind speed [m/s]'
        )
    }
    return figure


# XY figure for Turb
@app.callback(Output('xyTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                           Input('Turbxdd', 'value'), Input('Turbydd', 'value'),Input('MainDict','children')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2, TurbChosenxdd, TurbChosenydd,MainDict1):
    MainDict = json.loads(MainDict1)
    df1 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch1)],orient='split')
    df2 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch2)],orient='split')

    #For the title and units
    idx_x = IndicesinList(DfHeaders,TurbChosenxdd)[0]
    idx_y = IndicesinList(DfHeaders,TurbChosenydd)[0]
    TurbChosenxddLabel = DfHeadersDesc[idx_x]
    TurbChosenyddLabel = DfHeadersDesc[idx_y]
    TurbChosenxddUnits = DfHeadersUnits[idx_x]
    TurbChosenyddUnits = DfHeadersUnits[idx_y]
    name1 =str(TurbChosenPitch1) + ' deg' if TurbChosenPitch1!=2 else str(TurbChosenPitch1+1) + ' deg'
    name2 = str(TurbChosenPitch2)+ ' deg' if TurbChosenPitch2!= 2 else str(TurbChosenPitch2 + 1)+ ' deg'
    figure = {'data': [go.Scatter(
        y=df1[TurbChosenydd],
        x=df1[TurbChosenxdd], name=name1),  #first trace (curve) of the graph
        go.Scatter(
            y=df2[TurbChosenydd],
            x=df2[TurbChosenxdd], name=name2)], #Second trace (curve) of the graph
        'layout': go.Layout(
            yaxis=dict(automargin=True),
            title=TurbChosenxddLabel + ' vs ' + TurbChosenyddLabel,
            xaxis_title=TurbChosenxdd+ ' ' +TurbChosenxddUnits,
            yaxis_title=TurbChosenydd+ ' ' +TurbChosenyddUnits
        )
    }
    return figure

"""
# PSD for No Turb  plot
@app.callback(Output('PSDNoTurb', 'figure'), [Input('NoTurbPitch1', 'value'), Input('NoTurbPitch2', 'value'),
                                              Input('NoTurbydd', 'value'),Input('MainDict','children')])
def update_graph(NoTurbChosenPitch1, NoTurbChosenPitch2, NoTurbChosenydd,MainDict):
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
"""

# PSD of the Turbulent XY plot.
@app.callback(Output('PSDTurb', 'figure'), [Input('TurbPitch1', 'value'), Input('TurbPitch2', 'value'),
                                              Input('Turbydd', 'value'), Input('MainDict','children'), Input('PSDTurbaxis-type','value')])
def update_graph(TurbChosenPitch1, TurbChosenPitch2, TurbChosenydd,MainDict1,AxisType):
    MainDict = json.loads(MainDict1)
    df1 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch1)],orient='split')
    df2 = pd.read_json(MainDict['Turb1Pitch' + str(TurbChosenPitch2)],orient='split')
    #For Title and units
    idx_y = IndicesinList(DfHeaders,TurbChosenydd)[0]
    TurbChosenyddLabel = DfHeadersDesc[idx_y]
    TurbChosenyddUnits = DfHeadersUnits[idx_y]
    #AxisType = 'linear' if AxisType == 'Linear' else 'log'
    f1, PSD1 = CalcPSD(df1['Time'], df1[TurbChosenydd], 0.025)  # delta t is 0.025s always
    f2, PSD2 = CalcPSD(df2['Time'], df2[TurbChosenydd], 0.025)  # delta t is 0.025s always
    omega1, omega2 = df1['Omega'].mean() / (2 * np.pi), df2['Omega'].mean() / (2 * np.pi)
    name1 =str(TurbChosenPitch1) + ' deg' if TurbChosenPitch1!=2 else str(TurbChosenPitch1+1) + ' deg'
    name2 = str(TurbChosenPitch2)+ ' deg' if TurbChosenPitch2!= 2 else str(TurbChosenPitch2 + 1)+ ' deg'

    figure = {'data': [go.Scatter(y=PSD1, x=f1, name=name1), #PSD of 1st y value in XY plot
                       go.Scatter(y=PSD2, x=f2, name=name2), #PSD of 2nd y value in XY plot
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

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

#app.run_server()
if __name__ == '__main__':
    app.run_server(debug=True) #debug=True -> Live changes in the app as code is being changed!
