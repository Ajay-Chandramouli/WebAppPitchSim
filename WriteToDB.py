import mat4py #to read .mat files in Python
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

Servers= {'Local' :dict(host = 'localhost',user = 'root', pwd = 'usausb12',database = 'PitchMisalignment'),
               'Azure': dict(host = 'windturbinefaultsaz.mysql.database.azure.com',user = 'chandramouli@windturbinefaultsaz',
                             pwd = 'Parsyd123',database = 'PitchMisalignment')}
#Haha using both syntaxes to create a dictionary

ServerType = 'Local'
SQLServer = Servers[ServerType]

engine = create_engine('mysql+mysqlconnector://{user}:{pwd}@{host}/{database}'
                       .format(user=SQLServer['user'], pwd=SQLServer['pwd'], host=SQLServer['host'], database=SQLServer['database']))

#Some Simulation Info:
#PitchLevel, PitchAngle, Wsp, Seed are some parameters related to the simulations of the data.
#PitchAngle refers to the pitch angle misalignment of the wind turbine blade. For a particular pitch angle misalignment,
#simulations were performed for many wind speeds and seeds. Each simulation results in a .mat file.

#Data belonging to each pitch angle misalignment will be stored in a seperate table in SQL

path = r'C:\Host Online' #path to where the .mat files are located
for PitchLevel in [0,1,2]: #Pitch Misalignement levels used in simulations. Directly related to pitch angles itself
    PitchAngle = 3 if PitchLevel == 2 else PitchLevel # Relation between misalignment level and misalignment angle
    dbtable = 'deg' + str(PitchAngle) # Name of the table to which data will be written in SQL.
    for Wsp in [10,12,14,16,20]:
        for seed in ['s0','s1']:
            temp = mat4py.loadmat(path + '\\'+'M000P{}00_T1_S1_Wsp{}_{}.mat'.format(PitchLevel,Wsp,seed)) #read .mat files
            DfHeaders = open(path + '//' + 'Headers.txt', 'r').read().splitlines()  # Names of the .mat columns stored in a .txt file
            df = pd.DataFrame.from_dict(temp['sig']) #Store data in a DataFrame
            df.columns = DfHeaders #Naming the columns of the DataFrame
            df['Wsp']  = Wsp #Adding mean windspeed info to the data
            df['Seed'] = int(seed[1]) #Adding Seed info to the data
            # Writing Df to a SQL table. The precision of varaiable time is enough to 3 decimals, this can help in saving memory
            df.to_sql(dbtable,con=engine,if_exists='append',chunksize=1000, index = False,dtype={"Time":sqlalchemy.types.Float(precision=3, asdecimal=True)})

