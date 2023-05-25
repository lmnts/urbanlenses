"""
Copyright <2021> <Enol Vallina>

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
"""
# MAIN LIBRARIES ################################################################
import requests
import json

import csv
import pandas as pd

import time
import sys
import os
import random
from datetime import datetime
from datetime import timedelta
from time import sleep

# INTERFACE LIBRARIES ###########################################################
import tkinter
from subprocess import call
import PySimpleGUI as sg

# DIFINING TIME OF SEARCH #######################################################
dateToday_raw = datetime.now()
print(str(dateToday_raw) + '\n')
dateToday_format = dateToday_raw.strftime('%Y%m%d_%H%M%S')
dateToday_format2 = dateToday_raw.strftime('%y%m%d')

# USER INPUT ####################################################################
## So... first things first, please replace this file path to the location of the text file where the API key is saved.
dirAPIkey = r"C:\Users\evallina\Dropbox\_eMiniProjects\210124_eRoutes\_urbanlensesRepos\gAPI_key.txt" 
## (you are allowed to laugh about my rudimentary naming strategies, sorry!)

# OPTIMIZATIONS #################################################################

## Definition used across the script to transform the search keywords to a list of searcheable items.
def string2List(rawstrlist):
    mylistsplit=rawstrlist.split(",")
    mylistend=[]
    for item in mylistsplit:
        mylistend.append(item.replace(" ",""))
    print(mylistend)
    return mylistend

## Defs for Elevation change and Slope Calculation
def calculate_elevation_change(elevations):
    # Calculate the overall elevation change
    elevation_change = elevations[-1] - elevations[0]
    return elevation_change

def calculate_slopes(elevations, distances):
    # Calculate the slope for each segment
    slopes = []
    for i in range(len(elevations)-1):
        elevation_change = elevations[i+1] - elevations[i]
        distance = distances[i]
        slope = elevation_change / distance
        slopes.append(slope)
    return slopes

#########################################################################################################################################################
## INTERFACE ############################################################################################################################################
#########################################################################################################################################################
sg.theme('DarkTeal10')
searchInputGeneric='Schools'
searchRouteGeneric='walking'
layout=[
    [sg.Text('Loc2Route Beta v2.7\n',font=('Arial',32,'bold'))],
    [sg.Text("Save Folder"),
    sg.In("C:/Loc2Route",size=(25, 1), enable_events=True, key="-FOLDER-"),
    sg.FolderBrowse()],

    [sg.Text('\n\n'),],
    [sg.Text('Select Location Parameters:',font=('Arial',10,'bold'))],
    [sg.Text('Enter Location (lat,lng)          '), sg.InputText('47.608658, -122.340574')],
    [sg.Text('Enter Radius (m)                  '), sg.InputText('150')],
    #[sg.Text('Enter Topic - File Name        '), sg.InputText('FoodAndBeverage...')],
    #[sg.Button("Check Values",font='Arial 8')],
    [sg.Text(' \n',font=('Arial',15,'bold'))],
    [sg.Text('Select Search Type:',font=('Arial',10,'bold'))],
    [sg.Text('Enter Search Keywords List  '), sg.InputText(searchInputGeneric)],
    [sg.Text('Enter Route Mode                '), sg.InputText(searchRouteGeneric)],
    [sg.Text("(Route Mode Options: walking, driving, transit or bicycling)\n",font=('Arial',8,'italic'))],
    [sg.Button(" Custom Search ",font='Arial 8'), sg.Button(" Cultural ",font='Arial 8'),sg.Button(" Fitness ",font='Arial 8'),sg.Button(" Food&Beverage ",font='Arial 8'),sg.Button(" Lodging ",font='Arial 8'),sg.Button(" Entertainment ",font='Arial 8')],
    [sg.Button("RUN SCRIPT",font='Arial 15')],
    #[sg.Text("\n/////////////////////////////\nCheat List: \n>NFAB Site: 37.870250,-122.256860\n>Dwinelle Site: 37.870789,-122.261577\n>FortWorthCC: 32.751390, -97.329050\n>UN Reno: 39.535735, -119.815407\n")],
    [sg.Text('\n\n                                                                                                           '),sg.Button("CLOSE")]
    ]

#Create the Window
window = sg.Window("Loc2Route",layout, margins=(100,150))
#Text inputs Values:

#Create event Loop with the info gathered in the interface
while True:
    event, values = window.read()
    
    # This are some pre-set scenarios for making more systemized searches.
    if event ==" Cultural ":
        print('\n> Cultural Search Selected: Cultural Center, Museum, Art Gallery, Lecture Hall')
        searchInputGeneric2 = ('Cultural Center, Museum, Art Gallery, Lecture Hall')
        intin_Keywords= searchInputGeneric2
        sg.popup('You Changed the Search for Cultural:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    elif event ==" Fitness ":
        print('\n> Fitness Search Selected: Gym, Climbing, Fitness, Spa, Swiming, Sport, Stadium, Arena')
        searchInputGeneric3 = ('Gym, Climbing, Fitness, Spa, Swiming, Sport, Stadium, Arena')
        intin_Keywords= searchInputGeneric3
        sg.popup('You Changed to a Fitness Search:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    elif event ==" Lodging ":
        print('\n> Lodging Search Selected: Hotels, Hostel, Resort, Lodging, B&B')
        searchInputGeneric4 = ('Hotels, Hostel, Resort, Lodging, B&B')
        intin_Keywords= searchInputGeneric4
        sg.popup('You Changed to a Lodging Search:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    elif event ==" Food&Beverage ":
        print('\n> Food and Beverage Search Selected: Restaurant, Bar, Food, Brewery, Dining')
        searchInputGeneric4 = ('Restaurant, Bar, Food, Brewery, Dining')
        intin_Keywords= searchInputGeneric4
        sg.popup('You Changed to a Food & Bev Search:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    elif event ==" Entertainment ":
        print('\n> Entertainment Search Selected: Theatre, Entertainment, Show, Cinema,Concert Hall, Music Venue')
        searchInputGeneric5 = ('Theatre, Entertainment, Show, Cinema,Concert Hall, Music Venue')
        intin_Keywords= searchInputGeneric5
        sg.popup('You Changed to a Entertainment Search:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    elif event ==" Custom Search ":
        print('\n> CustomSearch Selected: %s' % values[2])
        intin_Keywords= values[2]
        sg.popup('You Changed the Search for Cultural:\n > Keywords:    %s'%(intin_Keywords))
        intin_Keywords_formated=string2List(intin_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(intin_Keywords_formated))))

    #Getting the values directly from the interface
    intin_location  =values[0]  # location given in Geocoordinates
    intin_Radius    =values[1]  # radius given in meters
    intin_Mode = values[3]      # Route mode, it would have to be one of ['walking','driving','bicycling','transit']
    intin_FolderDirectory= values["-FOLDER-"] # the file directory where the json files will be saved
 

    #End program if user close window or presses the OK button
    if event=="CLOSE" or event ==sg.WIN_CLOSED:
        break

    # RUN THE SCRIPT #    
    if event=="RUN SCRIPT":
        if 'intin_Keywords_formated' not in globals() :
            sg.popup('You have forgotten to input Keywords for Search!')
        else:
            print("_____________________________________________________________________")
            print ("\nHOLA AND LET'S GO!\n_____________________________________________________________________")
            print("+88_\n_+880_\n_++88_\n_++88_\n__+880_________________________++_\n__+888________________________+88_\n__++880______________________+88_\n__++888_____+++88__________+++8_\n__++8888__+++8880++88____+++88_\n__+++8888+++8880++8888__++888_\n___++888++8888+++888888++888_\n___++88++8888++8888888++888_\n___++++++888888888888888888_\n____++++++88888888888888888_\n____++++++++000888888888888_\n_____+++++++000088888888888_\n______+++++++00088888888888_\n_______+++++++088888888888_\n_______+++++++088888888888_\n________+++++++8888888888_\n________+++++++0088888888_\n________++++++0088888888_\n________+++++0008888888_\n________#############_")

            #########################################################################################################################################################
            ## GOOGLE MAPS API REQUEST ############################################################################################################################################
            #########################################################################################################################################################

            # REQUEST TYPES ###
            GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
            GOOGLE_MAPS_API_URL_DIR = 'https://maps.googleapis.com/maps/api/directions/json'
            GOOGLE_PLACES_DET='https://maps.googleapis.com/maps/api/place/details/json'
            GOOGLE_PLACES_API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            GOOGLE_PLACES_API2="https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            GOOGLE_ELEVATION_API = 'https://maps.googleapis.com/maps/api/elevation/json'
            
            # API KEY ### Reads the API key from an external file stored in the computer, when using the code, 'dirAPIkey' should be replaced
            
            with open(dirAPIkey, 'r') as file:
                GOOGLE_API_KEY = file.read().strip()
            
            
            
            # INPUT DATA ##################################################################################
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>> GATHER LOCATIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # DEFINING PARAMETERS
            GOOGLE_API_SEARCH=GOOGLE_PLACES_API
            R00_loc = intin_location
            print('> Coordinates: %s' % R00_loc)
            #break
            R00_radius = intin_Radius
            R00_keyword=intin_Keywords_formated
            R00_locbias='circle:%s@%s'%(R00_radius,R00_loc)
            R99_results = []  # This is the final List adding all the pages results
            GAPIRESULTS='results'

            finalList = []

            #Lists for Eliminating Duplicate Entries
            finalListDups =[]
            final4dupsTestLis=[]

            nAb=''
            for i,item in enumerate(R00_keyword):
                if i>0:
                    nAb=nAb+'-'+item
                else:
                    nAb=item

            nameAppendix = '%s_%sm' % (nAb, R00_radius)
            print('> File Name: %s'%(nameAppendix))

            print('\n> INITIATE LOCATION GATHER: \n')
            for k in range(len(R00_keyword)):
                #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                #print('> SEARCH KEYWORD: %s' % (R00_keyword[k]))
                #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                R00_parameters = {
                    'key': GOOGLE_API_KEY,
                    'location': R00_loc,
                    'radius': R00_radius,
                    'keyword': R00_keyword[k]
                }

                R00_request = requests.get(GOOGLE_API_SEARCH, params=R00_parameters)
                R00_result = R00_request.json()
               
                R99_results = R00_result[GAPIRESULTS]
           
                #### DEFINITION TO CHECK IF ITEM IS IN DICTIONARY####################
                def checkKey(dict, key):
                    if key in dict.keys():
                        # print(">>Yep!")
                        #print("value =", dict[key])
                        return True
                    else:
                        #print(">>Not there, sorry...")
                        return False


                #####################################################################
                tokenBool = checkKey(R00_result, 'next_page_token')
                #print('>NEXT PAGE TOKEN? : %s\n' % (tokenBool))
                if tokenBool == True:
                    #print(">>TOKEN!")
                    tempTokenBool = tokenBool
                    tempToken = R00_result['next_page_token']
                    #print('>>Token Reference: %s' % (tempToken))

                    while tempTokenBool == True:
                        #print('\nMORE RESULTS!\nGoing to sleep')
                        time.sleep(2)
                        #print('>Wake up!')
                        R0X_parameters={}
                        R0X_parameters.update(R00_parameters)#R00_parameters
                        R0X_parameters.update({'pagetoken':tempToken})


                        R0X_request = requests.get(GOOGLE_API_SEARCH, params=R0X_parameters)
                        R0X_result = R0X_request.json()
                        #print('>>RESULT X: %s' % (R0X_result))
                        #print('>>RESULT LIST LENGTH: %s' % (len(R00_result[GAPIRESULTS])))
                        R99_results.extend(R00_result[GAPIRESULTS])
                        #print('>>R99_results LENGHT: %s' % (len(R99_results)))
                        # Check if there is another tempToken
                        tempTokenBool = checkKey(R0X_result, 'next_page_token')
                        if tempTokenBool == True:
                            tempToken = R0X_result['next_page_token']

                # CREATE AN ADDITIONAL REQUEST TO GET TO KNOW MORE DETAILS ABOUT THE PLACE ###########################
                
                placeDet_List_hours=[]

                for result in R99_results:
                    #Cooking the request to Place Details by place Id input
                    tempID= result['place_id']
                    placeDet_params = {
                        'place_id': tempID,
                        'key': GOOGLE_API_KEY
                    }
                    r_placeDet=requests.get(GOOGLE_PLACES_DET,params=placeDet_params)
                    placeDet_res = r_placeDet.json()


                # RESULTING DATA PER PAGE IS FORMATED IN A DICTIONARY ENTRY ###########################################
                for i, item in enumerate(R99_results):
                    #print('>%s>>>%s' % (i, item['name']))
                    tempLocation = '%s,%s' % (
                        item['geometry']['location']['lng'], item['geometry']['location']['lat'])
                    # Building Data Tree
                    dataEntry = {
                        'name': item['name'],
                        'location': tempLocation,
                        'lat':item['geometry']['location']['lat'],
                        'lng':item['geometry']['location']['lng'],
                        'types': item['types'],
                        'icon': item['icon'],
                        'search':R00_keyword[k]
                        #'vicinity': item['vicinity']
                    }
                    finalList.append(dataEntry)
                    finalListDups.append(tempLocation)

                progPercent=round(k/len(R00_keyword)*100,2)
                print('> %s %% COMPLETE' % progPercent, end='\r')
                    # finalDic.add(dataEntry)
            print ('> 100% DONE!!                           ')
          

            finalList4real=[]
            for i, item in enumerate(finalListDups):
                if item not in final4dupsTestLis:
                    final4dupsTestLis.append(item)
                    finalList4real.append(finalList[i])

            finalDic = dict(enumerate(finalList4real))   
            finalData = finalDic

            # SAVE DATA OF THE LOCATIONS ##############################################################
            basePathXport=intin_FolderDirectory
            # 1. Save Json File for Checking

            # 2. Save Final File
            # 2.a Create Folder with Today's date
            newdir = ('/%s_locations' % (dateToday_format2))
            newpath = basePathXport + newdir
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # 2.b Create the final file
            dumps_finalData = json.dumps(finalData)
            fout_finalData = open("%s/%s_locations_%s.json" %(newpath, dateToday_format, nameAppendix), "w")
            #fout_finalData= open("%s/%s_Steps_dist.json" %(newpath,dateToday_format2),"w")
            fout_finalData.write(dumps_finalData)
            print('> DATA SAVED!\n')



            #########################################################################################################################################################
            ## GOOGLE MAPS ROUTES API REQUEST ########################################################################################################################
            #########################################################################################################################################################
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>> GOOGLE ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            
            # INPUT DATA ############################################################
            
            # Origin Points (list) ##########################
            inputListOrigin=[]
            listOr=[]
            ## This loop gets the points retrieved from the google locations search
            for i,item in enumerate(finalData):
                listOr.append('%s,%s' %(finalData[i]['lat'],finalData[i]['lng']))

            inputListOrigin=listOr

            # Destination Points (list) #####################
            inputDestination_UCBSite= intin_location
            inputListDestination=[]
            inputListDestination.append(inputDestination_UCBSite)
            print ('> There are %s routes to be analyzed' %(len(inputListDestination)) )

            # Mode of Transportation ########################
            inputMode= ['walking','driving','bicycling','transit']

            ## Set default value for inputModeSel
            inputModeSel = 'walking'

            ## Check if intin_Mode exists and is in inputMode
            try:
                intin_Mode
            except NameError:
                print("> intin_Mode is not defined")
            else:
                if intin_Mode in inputMode:
                    inputModeSel = intin_Mode
                    print(f"> Travel Mode is set to... {inputModeSel} !")
                else:
                    print(
                        f"> The value of intin_Mode is not in the inputMode list, inputModeSel remains as {inputModeSel}")


            ## LOOP FOR ORIGINS ######################################################
            nameAppendixRoutes='Route_%s_%s'%(nAb,inputModeSel) #This is used for naming the file that will be saved
            finalDataRoute={} # This the final Dic that will be saved as a JSON file.

            print('\n> INITIATE ROUTE ANALYSIS: \n')
            for e in range(len(inputListDestination)):
                progPercentTempList=[]
                #sleep(random.randint(1, 4)) ... this was used as a way to give time between requests and to not make the API to freakout!
                for i in range(len(inputListOrigin)):
                    #sleep(random.randint(1, 5))
                    #print('########################################################################################################################################################################################################')
                    #print('## %s / LOOP INPUT DESTINATION %s/%s of ORIGIN %s/%s)' % ((len(inputListDestination)*e)+i,e,len(inputListDestination)-1,i,(len(inputListOrigin)-1)))
                    #print('## ROUTE: %s > %s'%(inputListOrigin[i],inputListDestination[e]))
                    #print('########################################################################################################################################################################################################')

                    ## PARAMETERS PER REQUEST TYPE ###########################################
                    params_dir = {
                        'origin': inputListOrigin[i],
                        'destination': inputListDestination[e],
                        'mode':inputModeSel,
                        'key':GOOGLE_API_KEY
                    }

                    ## FINAL REQUEST #######################################################
                    req = requests.get(GOOGLE_MAPS_API_URL_DIR, params=params_dir)
                    res = req.json()
                    ## Getting the Total Number of Results for this Request
                    res1= json.loads(req.text)


                    ## DATA HANDLING #######################################################
                    #Getting a Dictionary with all the geo-points in route

                    ## Getting General Details of the Route
                    data_Gral_Distance= res1['routes'][0]['legs'][0]['distance']['value'] #Distance in Meters
                    #print('_\n## dataGral: distance\n%s' % (data_Gral_Distance))

                    data_Gral_Duration= res1['routes'][0]['legs'][0]['duration']['value'] #Distance in Seconds
                    #print('_\n## dataGral: duration\n%s' % (data_Gral_Distance))

                    data_Gral_Mode=res1['routes'][0]['legs'][0]['steps'][0]['travel_mode'] # Model of Transport
                    #print('2. Saving Gral Details of Route')

                    ## Getting Steps of the route
                    data_stepsRAW=res1['routes'][0]['legs'][0]['steps']
                    #print('_\n## dataGral: steps RAW\n%s' % (data_stepsRAW))

                    ## Create Lists with Data that I want to extract
                    temp_list_steps_distances=[]
                    temp_list_steps_durations=[]
                    temp_list_steps_startLoc=[]
                    temp_list_steps_endLoc=[]

                    #temp_list_steps_elevchange=[]
                    #temp_list_steps_slopes=[]

                    # These two are just for formating the data in a better way to be used for the google API elevations
                    temp_list_steps_elevInput =[]
                    temp_list_steps_elevInput2=[]

                    for x in range(len(data_stepsRAW)):
                        temp_list_steps_distances.append(data_stepsRAW[x]['distance']['value'])
                        temp_list_steps_durations.append(data_stepsRAW[x]['duration']['value'])
                        
                        # I store (long,lat) is how it works best with Mosquito plugin in Grasshopper
                        temp_list_steps_startLoc.append(('%s,%s' % (data_stepsRAW[x]['start_location']['lng'],data_stepsRAW[x]['start_location']['lat'])))
                        temp_list_steps_endLoc.append(('%s,%s' % (data_stepsRAW[x]['end_location']['lng'],data_stepsRAW[x]['end_location']['lat'])))

                        # I store this with 'lat' first so I can use them (without changing stuff) with the google elevation API or others..
                        temp_list_steps_elevInput.append(('%s,%s' % (data_stepsRAW[x]['start_location']['lat'],data_stepsRAW[x]['start_location']['lng'])))
                        temp_list_steps_elevInput2.append(('%s,%s' % (data_stepsRAW[x]['end_location']['lat'],data_stepsRAW[x]['end_location']['lng'])))
                        
                    
                    # Retrieve Elevation information from start steps
                    temp_list_steps_elevInput.append(temp_list_steps_elevInput2[-1]) #add the last point of the route
                    temp_list_steps_elevation=[]
                    
                    for loc in temp_list_steps_elevInput:
                        elev_params_dir = {
                            'locations': loc,
                            'key': GOOGLE_API_KEY
                        }
                        elev_req = requests.get(GOOGLE_ELEVATION_API, params=elev_params_dir)
                        elev_res = elev_req.json()
                        #print(elev_res)
                        temp_list_steps_elevation.append(elev_res['results'][0]['elevation'])
                    
                    # Calculate the elevation changes and calculate the slopes
                    temp_list_steps_elevchange = calculate_elevation_change(temp_list_steps_elevation)
                    temp_list_steps_slopes = calculate_slopes(temp_list_steps_elevation, temp_list_steps_distances)
                    temp_slopeAvg = sum(temp_list_steps_slopes) / len(temp_list_steps_slopes)

                    #Building Data Tree
                    data_route={
                        'data_gral' : {
                            'totalDistance' :   data_Gral_Distance,
                            'totalDuration' :   data_Gral_Duration,
                            'travelMode'    :   data_Gral_Mode,
                            'ElevationChange':  temp_list_steps_elevchange,
                            'ElevationAvgSlope': temp_slopeAvg
                        },
                        'data_steps' : {
                            'steplDistance':   temp_list_steps_distances,
                            'stepDuration' :   temp_list_steps_durations,
                            'stepStartPt'  :   temp_list_steps_startLoc,
                            'stepEndPt'    :   temp_list_steps_endLoc,
                            'stepElevation':   temp_list_steps_elevation,
                            'stepElevSlopes':  temp_list_steps_slopes
                        }
                    }

                    nameEntry=str(e+i)
                    finalDataRoute.update({nameEntry : data_route})

                    



                    ##SAVE DATA #######################################################
                    #print('########################################################################################################################################################################################################')
                    #print('## SAVE DATA')
                    #print('########################################################################################################################################################################################################')
                    basePathXport=intin_FolderDirectory
                    #basePathXport='C:/Users/enolv/Dropbox/_eMiniProjects/210124_eRoutes/xprt'
                    # 1. Save Json File for Checking

                    #   2. Save Final File
                    #   2.a Create Folder with Today's date
                    newdir=('/%s_routes' % (dateToday_format2))
                    newpath=basePathXport+newdir
                    #print('# newpath ##### '+newpath+' ################################')
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)

                    #   2.b Create the final file
                    #print("__________________________")

                    dumps_finalDataRoute=json.dumps(finalDataRoute)
                    fout_finalDataRoute= open("%s/%s_finalDataRoute_%s.json" %(newpath,dateToday_format,nameAppendixRoutes),"w")
                    #fout_finalDataRoute= open("%s/%s_Steps_dist.json" %(newpath,dateToday_format2),"w")
                    fout_finalDataRoute.write(dumps_finalDataRoute)

                progPercent=round(i/len(inputListDestination)*100)
                print('>%s %% COMPLETE' % progPercent, end='\r')

            print ('>100% DONE!!                  ')
            #print('6. Final Updated Data Tree: %s'% (finalDataRoute))
            print("_____________________________________________________________________")
            print('\n\nANALYSIS DONE!!!!!!!!!!!!\n\n')

'''
        print('\n##############################################################################################################################################')
        print('##############################################################################################################################################')
        print('##########                                         ###########################################################################################')
        print('##########   OOOOOOOOOOOO  OO     OOO       OO     ###########################################################################################')
        print('##########   OO                   OO OO     OO     ###########################################################################################')
        print('##########   OO            OO     OO  OO    OO     ###########################################################################################')
        print('##########   OOOOOOOO      OO     OO   OO   OO     ###########################################################################################')
        print('##########   OO            OO     OO    OO  OO     ###########################################################################################')
        print('##########   OO            OO     OO     OO OO     ###########################################################################################')
        print('##########   OO            OO     OO       OOO     ###########################################################################################')
        print('##########                                         ###########################################################################################')
        print('##############################################################################################################################################')
        print('##############################################################################################################################################')
'''

window.close()
exit()
