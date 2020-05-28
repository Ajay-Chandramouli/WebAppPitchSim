import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from SupportFunctions import *
import json
import base64
from sqlalchemy import create_engine

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] #A nice stylesheet!

Servers= {'Local' :dict(host = 'localhost',user = 'root', pwd = 'usausb12',database = 'PitchMisalignment'),
               'Azure': dict(host = 'windturbinefaultsaz.mysql.database.azure.com',user = 'chandramouli@windturbinefaultsaz',
                             pwd = 'Parsyd123',database = 'PitchMisalignment')}
#Haha using both syntaxes to create a dictionary

ServerType = 'Azure'
SQLServer = Servers[ServerType]

engine = create_engine('mysql+mysqlconnector://{user}:{pwd}@{host}/{database}'
                       .format(user=SQLServer['user'], pwd=SQLServer['pwd'], host=SQLServer['host'], database=SQLServer['database']))


#Now we move on to the app, created using Dash!
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server #app server to deploy the app locally.
path = r'C:\Host Online'

#The data is arranged in such a way that each simulation case is a .mat file from MATLAB.
# Each simulation case corresponds to one particular wind speed. turbulence level and one fault scenario (pitch misalignment etc).
# If any of these changes, it becomes a new simulation case.
# Each .mat file contains the turbine response (rot. speed, thrust, power etc) of that particular simulation

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
dd_options_Seed_Info = create_value_label_for_dropdown(['Yes','No'],[1,0])

image_filename = path + '//'+ 'DTU10MWresized.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([                                             #html layout of the app. Dash html components are Verrry similar to standard html components
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

    html.Div([ ]),


    html.Div([html.H4('Let\'s get started!'),
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
        html.P('Y axis type: ',style={'display':'inline-block','margin-right': '15px'}),
        dcc.RadioItems(id='PSDTurbaxis-type', options=r_options_PSD_yaxis,
                value='log', labelStyle={'display': 'inline-block'},style={'display':'inline-block'}),
        #html.Button('Update PSD', id='PSDButtonTurb',n_clicks=1),
        dcc.Graph(id='PSDTurb',style={'width':'100%'})],style={'width': '100%', 'display': 'inline-block'})
])

@app.callback([Output('MainDict','children'),Output('Loading2','children')],[Input('TurbPitch1','value'), Input('TurbPitch2','value'),
                                             Input('Turbxdd', 'value'), Input('Turbydd', 'value'),Input('Wsp','value'),
                                                Input('SeedInfo','value')])
def dynamic_load(PitchLevel1,PitchLevel2,Turbxdd,Turbydd,Wsp,SeedInfo):
    Seed = (1,1) if SeedInfo ==1 else (1,0)
    Dict = {}
    MainDict={}
    Colslist = GetUniqueinList([Turbxdd, Turbydd, 'Time', 'Vo', 'Omega'])  # Time, Omega and Vo are always needed because of the input V figure and PSD
    for n, Cols in enumerate(Colslist):
        ColslistStr = Cols if n == 0 else ColslistStr + ',' + Cols
    CaseOrder = ['Turb1Pitch'+str(PitchLevel1),'Turb1Pitch'+str(PitchLevel2)]

    for n,PitchLevel in enumerate([PitchLevel1,PitchLevel2]):
        PitchAngle = 3 if PitchLevel==2 else PitchLevel
        dbtable = 'deg' + str(PitchAngle)  # Database table to be connected to
        SQLQuery = 'SELECT {} FROM {} WHERE Wsp = %s AND Seed = %s '.format(ColslistStr,dbtable)  # SQL query to be executed
        Dict[CaseOrder[n]]  = pd.read_sql(SQLQuery, con=engine, params=(Wsp, Seed[n]))  # executing the query in MySQL
    for key in Dict.keys():
         MainDict[key] = Dict[key].to_json(orient='split')

    return json.dumps(MainDict),[]


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
    return figure

#app.run_server()
if __name__ == '__main__':
    app.run_server(debug=True) #debug=True -> Live changes in the app as code is being changed!
