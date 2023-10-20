import os
import re
from scipy.spatial import distance
import pandas as pd
from scipy.signal import savgol_filter
import numpy as np
import pandas as pd
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt
import glob
import os
from scipy.signal import savgol_filter
import numpy as np
from scipy.signal import find_peaks
import seaborn as sns
import pickle

list_pickle_file=[]
list_pickle_file_path=[]
list_csv_file=[]
listhydoicdep=[]

def list_files(dir):
    subdirs = [x[0] for x in os.walk(dir)]
    for root, dirs, files in os.walk(dir):
      if len(files) != 0:
        for i in range(0,len(files)):
             if re.search(".pickle",os.path.splitext(files[i])[1]) :
                  list_pickle_file.append(files[i])
                  list_pickle_file_path.append(os.path.join(root,files[i]))
             if re.search(".csv",os.path.splitext(files[i])[1]) :
                   list_csv_file.append(os.path.join(root,files[i]))
    return list_pickle_file,list_pickle_file_path,list_csv_file

dir='C:\\Users\\user\\OneDrive - HKUST Connect\\Desktop\\Strikes_hydoic'
pickle_name,list_pickle_file_path,csv_name=list_files(dir)
#print(pickle_name)
#print(csv_name)

def plot_eyeskindistance(pickle_name,list_pickle_file_path,csv_name):
   strike_frame=[]
   for j in range(0,len(csv_name)):
         print(csv_name[j])
         val1 = (csv_name[j].split("\\")[len(csv_name[j].split("\\")) - 1].split('.')[0])
         val2 = val1.split('-')[0]
         for k in range(0,len(pickle_name)):
                picklename=pickle_name[k].split('.')[0]
                #print(picklename)
                picklename = picklename.split('-')[0]

                if picklename == val2:
                   print(list_pickle_file_path[k])
                   with open(list_pickle_file_path[k], "rb") as f:
                        #u = pickle._Unpickler(f)
                        #u.encoding = 'latin1'
                        strike_frame = pickle.load(f)
                        break
         print(strike_frame)
         df = pd.read_csv(csv_name[j], header=[0,1,2])
         x1=list((df['DLC_resnet50_Skin_Eye_DetectionMar27shuffle1_10000'][ 'bodypart1']['x']))
         y1=list((df['DLC_resnet50_Skin_Eye_DetectionMar27shuffle1_10000'][ 'bodypart1']['y']))
         x2=list((df['DLC_resnet50_Skin_Eye_DetectionMar27shuffle1_10000'][ 'bodypart3']['x']))
         y2=list((df['DLC_resnet50_Skin_Eye_DetectionMar27shuffle1_10000'][ 'bodypart3']['y']))
         dis=[]
         for i in range(0,len(x1)):
               eyecord=[x1[i],y1[i]]
               skincord=[x2[i],y2[i]]
               dis.append(distance.euclidean(eyecord, skincord))
         #yy_sg = savgol_filter((dis), 5, 1)
         yy_sg1=np.gradient(dis)
         peaks, _ = find_peaks(yy_sg1, height=1.5)
         print(peaks)

         if len(peaks) != 0:
          for l in range(0,len(strike_frame)):
             min=1000
             for m in range(0,len(peaks)):
                 if abs((strike_frame[l])-(peaks[m])) <= min:

                      min=abs((strike_frame[l])-(peaks[m]))
             print(min)
             if min <= 1000:
              listhydoicdep.append(min)


plot_eyeskindistance(pickle_name,list_pickle_file_path,csv_name)

# listhydoicdep1=[0, 0, 1, 0, 1, 2, 3, 2, 1, 3, 7, 6, 5, 4, 8, 9, 9, 5, 1, 7,
# 3, 1, 2, 3, 1, 1, 3, 0, 1, 0, 4, 3, 4, 8, 2, 1, 6, 5, 4,
# 1, 1, 4, 3, 1, 2, 3, 1, 5,5, 5, 8, 10, 5,
# 0, 1, 4, 3, 2, 4, 2, 1, 1, 1, 1, 3, 1, 3, 0, 3,
# 3, 5, 5, 7, 2, 1, 1, 10,
# 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6,
# 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
# 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1,
# 2, 3, 4, 8, 1, 2, 3, 4, 5, 8, 9, 0, 1, 2, 7, 6, 5, 4, 3, 4, 5, 6, 7, 8, 9,
# 10, 2, 2, 3, 3, 4, 4, 3, 1, 2, 1, 1, 1, 4, 3, 2, 10, 8, 7, 4, 1, 1, 1, 0, 2]
plt.figure(figsize=(11, 8.5))
plt.tight_layout()
#plt.rcParams["font.family"] = "Arial"

list_data_f_=[]
plt.rcParams["patch.force_edgecolor"] = True
listhydoicdep2=[i * 5 for i in listhydoicdep]

print(listhydoicdep)
for i in range(0,len(listhydoicdep)):
    list_data_f_.append(['Strike'])
df = pd.DataFrame (np.column_stack([listhydoicdep2,list_data_f_]), columns = ['value','Type'])
#fig, ((ax1,ax2,)) = plt.subplots(nrows=2, ncols=1)
#fig.tight_layout(pad=3.5)
#print(df)
df = df.explode('value')
df['value'] = df['value'].astype('float')
# #g=sns.violinplot(data=df,x='Type', y="value",ax=ax1)
# sns.stripplot(data=df,x='Type', y="value",size=8,color='Magenta')
#
# plt.tick_params(axis='y', labelsize=33)
# plt.tick_params(axis='x', labelsize=33)
# plt.ylabel('Difference (in millisecs)',fontsize=33)
#
plt.legend(['Time gap Hydoic Depression & Strike'], loc='upper right',fontsize=12.5)
plt.yticks([0,10,20,30,40,50],fontsize=33)
plt.xlabel('',fontsize=33)

plt.axhline(y=1.5, color='r')
plt.axvline(x=0.5, color='r')
sns.distplot(listhydoicdep2, hist_kws={"color": "#1f77b4"},bins=50,
             kde=True,
             rug=False,
             rug_kws={"color": "Magenta", "alpha": 1, "linewidth": 0.5, "height": 0.05})


plt.tick_params(axis='y', labelsize=33)
plt.tick_params(axis='x', labelsize=33)
#plt.yticklabels([-0.5,0.00,0.05,0.10,0.15,0.2],fontsize=33)
#
#plt.yticklabels(fontsize=33)
#plt.xticklabels([-2,0,2, 4, 6, 8, 10,12],fontsize=33)
#
# #plt.tick_params(axis='y', labelsize=33)
#
#
# #plt.xlim(0, 12)
# # ax1.set_yticks(fontsize=33)
# # ax1.set_xticks(fontsize=33)
# plt.ylabel('Count', fontsize=33)
# plt.xlabel('Difference in millisecs', fontsize=33)
# plt.legend(['Time gap Hydoic Depression & Strike'], loc='upper right',fontsize=20)
plt.show()
plt.savefig('Test', bbox_inches='tight')

