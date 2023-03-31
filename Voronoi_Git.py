
import matplotlib.pyplot as plt
from scipy.spatial import SphericalVoronoi#, geometric_slerp
from mpl_toolkits.mplot3d import proj3d
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os


main_directory=r'D:...\\' #you can select a root for this project which contains all input and outputs
os.chdir(main_directory)

#Read inputs consist of LTE cells with daily KPIs for as many days as you need
excel_lists=os.listdir(main_directory)
files = [i for i in excel_lists if (i.startswith('4G_Cell_Daily') )]
temp=[]
for f in files:
    temp_=pd.read_csv(f, header=1 ,thousands = ',')
    temp.append(temp_[['Time', '4G LTE CELL','4G_PRB_Util_Rate_PDSCH_Avg_IR(#)']])
data=pd.concat([name for name in temp])
data_config=pd.read_excel(r"LTE_Cfg.xlsx")

#%%--------preprocessing of config stats
data_config.columns=['Sec', 'Azimuth', 'Latitude', 'Longitude', 'City',
       'Province', 'Region', 'Status']
data_config=data_config[(data_config.Sec.str[0]=='L')]
data_config['Sector']=data_config['Sec'].str[1:8]

data_config.describe()
data_config.isnull().sum()
del data_config['Sec']
from pygc import great_circle

#move in the direction of azimuths
data_config['Dis']=5
data_config=data_config.dropna().drop_duplicates(subset='Sector')
data_config['new_lat'],data_config['new_long'],_ =great_circle(distance=data_config['Dis'], azimuth=data_config['Azimuth'], latitude=data_config['Latitude'], longitude=data_config['Longitude']).values()
df_points=data_config[['Sector','new_long','new_lat']].dropna().drop_duplicates().reset_index(drop=True)
points = np.array(df_points[['new_long','new_lat']])

#plot new points
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
plt.show()

#%%-------------------------
from scipy.spatial import Delaunay
indptr_neigh, neighbours = Delaunay(points).vertex_neighbor_vertices

#Accessing the neighbours-------------
neighbour_dict={}
for i in range(len(points)):
    i_neigh = neighbours[indptr_neigh[i]:indptr_neigh[i+1]]
    neighbour_dict[df_points['Sector'][i]]=i_neigh
    print('i: %d, i_neigh:'  %i, i_neigh)


sector_dict={}
for i in range(len(points)):
    plt.text(points[i, 0], points[i, 1], df_points['Sector'][i], fontsize=7)
    sector_dict[i]=df_points['Sector'][i]

fig=voronoi_plot_2d(vor, dpi=300)
for i in range(len(points)):
    plt.text(points[i, 0], points[i, 1], df_points['Sector'][i], fontsize=7)


#%%Neighbour finding per sector
neigh_dict={}
for key in neighbour_dict.keys():
    neigh_dict[key+'1']=[sector_dict[ind]+'1' for ind in neighbour_dict[key]] +[sector_dict[ind]+'2' for ind in neighbour_dict[key]]+[sector_dict[ind]+'3' for ind in neighbour_dict[key]]+[sector_dict[ind]+'5' for ind in neighbour_dict[key]]
    neigh_dict[key+'1']=[*set(neigh_dict[key+'1'])]
    neigh_dict[key+'2']=neigh_dict[key+'1']
    neigh_dict[key + '3'] = neigh_dict[key + '1']
    neigh_dict[key + '5'] = neigh_dict[key + '1']
    neigh_dict[key + '7'] = neigh_dict[key + '1']
    neigh_dict[key + '8'] = neigh_dict[key + '1']


#Neighbors in DF ----------------------
neigh_out=pd.DataFrame(columns=['Cell','Neighbours'])
neigh_out['Cell']=neigh_dict.keys()
neigh_out['Neighbours']=neigh_dict.values()
neigh_out.to_excel(r"Country_neighbors.xlsx", index=False)

#%%data usage checking
#data.columns
df=data[['4G LTE CELL', '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)']].dropna()
df=df.groupby('4G LTE CELL').median().reset_index()
high_PRB_Target=70
Low_PRB_Target=30
Congest_Cells=df[df['4G_PRB_Util_Rate_PDSCH_Avg_IR(#)']>high_PRB_Target]['4G LTE CELL'].str[1:]
Candidate_Cells=df[(df['4G_PRB_Util_Rate_PDSCH_Avg_IR(#)']>5)& (df['4G_PRB_Util_Rate_PDSCH_Avg_IR(#)']<Low_PRB_Target)]['4G LTE CELL'].str[1:]

#filtering the distance
df_distance=pd.read_csv(r"SitesDistance.csv")[['Origin', 'Destination', 'Distance_Result']]
df_distance=df_distance[(df_distance['Distance_Result']<3)

congested_dict={}
KEYS=[x for x in neigh_dict.keys() if x in list(Congest_Cells)]
for k in KEYS:
    congested_dict[k]=[x for x in neigh_dict[k] if ((x in list(Candidate_Cells)) and (k[0:6]!=x[0:6]) and (x[0:6] in (df_distance[df_distance['Origin']==k[0:6]]['Destination']).values))]
    if congested_dict[k]==[]:
        del congested_dict[k]

Output=pd.DataFrame()
Output['Cell']=congested_dict.keys()
Output['Neighbour_low_PRB_candidates']=congested_dict.values()
Output=pd.merge(Output,data_config[['Sector','City', 'Province','Region']],how='left',left_on=Output['Cell'].str[:7] , right_on='Sector' )
Output.to_csv('Neighbour_LB.csv', index=False)

