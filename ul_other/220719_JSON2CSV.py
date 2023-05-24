
import json
import csv
import os
import numpy as np
import pandas as pd

print(">WELCOME TO THE JSON TO CSV TRANSFORMATION TOOL! \n")
#### SET THE FILE PATHS
#path= "L:\\Marketing\\Pursuits\\Proposals\\Fort Worth CCXP\\0 Marketing\\I Design Studies\\EV\\GIS\\loc2route\\data\\220412_locations2\\"
#path="C:\\Users\evallina\\Dropbox\\_eMiniProjects\\220323_Fort Worth\\_data\\220412_locations2\\"
path="L:\\Projects T-Z-0\\unr-mugp3\\5 Design\\Studies - EV\\02_Diagrams\\220718_Activities\\220719_locations\\"
newpath=path.replace(os.sep,'/')
print(">PATH= "+newpath)


print("///////////////////////////////////")



###FINDING ALL THE JSON FILES IN THE FOLDER DIRECTORY
path_to_json = newpath
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(">JSON LIST: " +str(json_files))  # for me this prints ['foo.json']



### CREATE LIST OF FUTURE CSV FILES
csvList=[]
#print ("\nSTART OF LIST ITERATION")
for item in json_files:
#    print(item)
    csvList.append(item.replace("json","csv"))

print(">CSV LIST: " + str(csvList))

print("///////////////////////////////////\n")



### TRANSFORM JSON FILES TO CSV
for i,jsonItem in enumerate(json_files):
    # Get the JSON file
    df1 = pd.read_json(("%s/%s" %(newpath,jsonItem)))

    # View data
    print(df1)

    #Transform it to CSV
    csvdir=("%s/%s" %(newpath,csvList[i]))
    df1.to_csv(csvdir)

    ### TRANSPOND CSV FILES
    tempCVS = pd.read_csv(csvdir)
    finalCVS=tempCVS.T

    ### SAVE CSV FILE IN DIRECTORY
    finalCVS.to_csv(csvdir)

    # and view the data
    print(finalCVS)




#
#
#L:\Marketing\Pursuits\Proposals\Fort Worth CCXP\0 Marketing\I Design Studies\EV\GIS\loc2route\data\220402_locations
