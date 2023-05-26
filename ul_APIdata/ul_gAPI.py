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
        i_input_Keywords= searchInputGeneric2
        sg.popup('You Changed the Search for Cultural:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    elif event ==" Fitness ":
        print('\n> Fitness Search Selected: Gym, Climbing, Fitness, Spa, Swiming, Sport, Stadium, Arena')
        searchInputGeneric3 = ('Gym, Climbing, Fitness, Spa, Swiming, Sport, Stadium, Arena')
        i_input_Keywords= searchInputGeneric3
        sg.popup('You Changed to a Fitness Search:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    elif event ==" Lodging ":
        print('\n> Lodging Search Selected: Hotels, Hostel, Resort, Lodging, B&B')
        searchInputGeneric4 = ('Hotels, Hostel, Resort, Lodging, B&B')
        i_input_Keywords= searchInputGeneric4
        sg.popup('You Changed to a Lodging Search:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    elif event ==" Food&Beverage ":
        print('\n> Food and Beverage Search Selected: Restaurant, Bar, Food, Brewery, Dining')
        searchInputGeneric4 = ('Restaurant, Bar, Food, Brewery, Dining')
        i_input_Keywords= searchInputGeneric4
        sg.popup('You Changed to a Food & Bev Search:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    elif event ==" Entertainment ":
        print('\n> Entertainment Search Selected: Theatre, Entertainment, Show, Cinema,Concert Hall, Music Venue')
        searchInputGeneric5 = ('Theatre, Entertainment, Show, Cinema,Concert Hall, Music Venue')
        i_input_Keywords= searchInputGeneric5
        sg.popup('You Changed to a Entertainment Search:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    elif event ==" Custom Search ":
        print('\n> CustomSearch Selected: %s' % values[2])
        i_input_Keywords= values[2]
        sg.popup('You Changed the Search for Cultural:\n > Keywords:    %s'%(i_input_Keywords))
        i_input_Keywords_formated=string2List(i_input_Keywords)
        print("> Length List Keyword Values: %s"%(str(len(i_input_Keywords_formated))))

    #Getting the values directly from the interface
    i_input_location  =values[0]  # location given in Geocoordinates
    i_input_Radius    =values[1]  # radius given in meters
    i_input_Mode = values[3]      # Route mode, it would have to be one of ['walking','driving','bicycling','transit']
    i_input_FolderDirectory= values["-FOLDER-"] # the file directory where the json files will be saved
 

    #End program if user close window or presses the OK button
    if event=="CLOSE" or event ==sg.WIN_CLOSED:
        break

    # RUN THE SCRIPT #    
    if event=="RUN SCRIPT":
        if 'i_input_Keywords_formated' not in globals() :
            sg.popup('You have forgotten to input Keywords for Search!')
        else:
            print("_____________________________________________________________________")
            print ("\nHOLA AND LET'S GO!\n_____________________________________________________________________")
            print('\n██╗     ███╗   ███╗███╗   ██╗████████╗███████╗    ██████╗  ██████╗ ██████╗ ██████╗ \n██║     ████╗ ████║████╗  ██║╚══██╔══╝██╔════╝    ╚════██╗██╔═████╗╚════██╗╚════██╗\n██║     ██╔████╔██║██╔██╗ ██║   ██║   ███████╗     █████╔╝██║██╔██║ █████╔╝ █████╔╝\n██║     ██║╚██╔╝██║██║╚██╗██║   ██║   ╚════██║    ██╔═══╝ ████╔╝██║██╔═══╝  ╚═══██╗\n███████╗██║ ╚═╝ ██║██║ ╚████║   ██║   ███████║    ███████╗╚██████╔╝███████╗██████╔╝\n╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝ ╚══════╝╚═════╝ \n')

            #########################################################################################################################################################
            ## GOOGLE MAPS API REQUEST ############################################################################################################################################
            #########################################################################################################################################################

            # REQUEST TYPES ###############################################################################
            GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
            GOOGLE_MAPS_API_URL_DIR = 'https://maps.googleapis.com/maps/api/directions/json'
            GOOGLE_PLACES_DET='https://maps.googleapis.com/maps/api/place/details/json'
            GOOGLE_PLACES_API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            GOOGLE_PLACES_API2="https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            GOOGLE_ELEVATION_API = 'https://maps.googleapis.com/maps/api/elevation/json'
            
            # API KEY #####################################################################################
            # Reads the API key from an external file stored in the computer, when using the code, 'dirAPIkey' should be replaced
            with open(dirAPIkey, 'r') as file:
                GOOGLE_API_KEY = file.read().strip()
            
            
            
            # INPUT DATA ##################################################################################
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>> GATHER LOCATIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # DEFINING PARAMETERS
            GOOGLE_API_SEARCH=GOOGLE_PLACES_API

            r_loc_geolocation = i_input_location
            r_loc_radius = i_input_Radius
            r_loc_keywords=i_input_Keywords_formated
            r_loc_results_raw = []  # This is the final List adding all the pages results
            r_loc_results_r='results' # this is just a way to get faster to the results since the api responds with two main keys, one being 'results'
            print('> Coordinates: %s | Radius: %s ' % (r_loc_geolocation,r_loc_radius))

            r_loc_finalList = []

            #Lists for Eliminating Duplicate Entries
            r_loc_finalListDups =[]
            r_loc_final4dupsTestLis=[]


            # Formating the appendix for file naming
            f_appendix_keywords=''
            for i,item in enumerate(r_loc_keywords):
                if i>0:
                    f_appendix_keywords=f_appendix_keywords+'-'+item
                else:
                    f_appendix_keywords=item

            f_finalNameAppendix = '%s_%sm' % (f_appendix_keywords, r_loc_radius)
            print('> File Name: %s'%f_finalNameAppendix)

            print('\n> INITIATE LOCATION GATHER: \n')
            for k in range(len(r_loc_keywords)):
                #####################################################################
                #### SEARCH KEYWORDS ################################################
                #####################################################################
                r_loc_parameters = {
                    'key': GOOGLE_API_KEY,
                    'location': r_loc_geolocation,
                    'radius': r_loc_radius,
                    'keyword': r_loc_keywords[k]
                }

                r_loc_request = requests.get(GOOGLE_API_SEARCH, params=r_loc_parameters)
                r_loc_request_in = r_loc_request.json()
               
                r_loc_results_raw = r_loc_request_in[r_loc_results_r]
           
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
                r_loc_tokenBool = checkKey(r_loc_request_in, 'next_page_token')
                #print('>NEXT PAGE TOKEN? : %s\n' % (tokenBool))
                if r_loc_tokenBool == True:
                    #print(">>TOKEN!")
                    r_loc_tempTokenBool = r_loc_tokenBool
                    r_loc_tempToken = r_loc_request_in['next_page_token']
                    #print('>>Token Reference: %s' % (tempToken))

                    # When the results come in more than one page, the following runs a loop that would go over all of them..
                    while r_loc_tempTokenBool == True:
                        # Pausing the requests so the API doesnt freakout
                        time.sleep(2)
                        
                        # Defining the parameters again, since they change wheather they are part of a page or not
                        r_loc_params_token={}
                        r_loc_params_token.update(r_loc_parameters)#R00_parameters
                        r_loc_params_token.update({'pagetoken':r_loc_tempToken})
                        # Making a request per page
                        r_loc_request_token = requests.get(GOOGLE_API_SEARCH, params=r_loc_params_token)
                        r_loc_results_in_token = r_loc_request_token.json()
                        # Storing everything in the main results list.
                        r_loc_results_raw.extend(r_loc_request_in[r_loc_results_r])
                        
                        # Check if there is another tempToken, so if there is another page
                        r_loc_tempTokenBool = checkKey(r_loc_results_in_token, 'next_page_token')
                        if r_loc_tempTokenBool == True:
                            r_loc_tempToken = r_loc_results_in_token['next_page_token']


                ######################################################################################################
                # CREATE AN ADDITIONAL REQUEST TO GET TO KNOW MORE DETAILS ABOUT THE PLACE ###########################
                ######################################################################################################
                print("\n>>>>>> GATHER LOCATION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                r_placeDet_res_raw=[]
                r_placeDet_List_hours=[]
                r_placeDet_List_ratings=[]
                r_placeDet_List_photo=[]
                r_placeDet_List_address=[]

                for result in r_loc_results_raw:
                    #Cooking the request to Place Details by place Id input
                    tempID= result['place_id']
                    
                    r_placeDet_params = {
                        'place_id': tempID,
                        'key': GOOGLE_API_KEY
                    }
                    r_placeDet=requests.get(GOOGLE_PLACES_DET,params=r_placeDet_params)
                    r_placeDet_res = r_placeDet.json()
                    r_placeDet_res_raw.append(r_placeDet_res)
                    #print(r_placeDet_res_raw)
                    #r_placeDet_List_hours.append(r_placeDet_res['result']['opening_hours']['periods'])
                    r_placeDet_List_ratings.append(r_placeDet_res['result']['rating'])
                    r_placeDet_List_photo.append(r_placeDet_res['result']['photos'][0]['html_attributions'])
                    r_placeDet_List_address.append(r_placeDet_res['result']['formatted_address'])

                    #This If statement checks if it is 'opening_hours' or 'current_opening_hours' in order to retrieve the right result
                    if 'opening_hours' in r_placeDet_res['result']:
                        r_placeDet_List_hours.append(r_placeDet_res['result']['opening_hours']['periods'])
                    elif 'current_opening_hours' in r_placeDet_res['result']:
                        r_placeDet_List_hours.append(r_placeDet_res['result']['current_opening_hours']['periods'])
                    else:
                        print("Neither 'opening_hours' nor 'current_opening_hours' found")
                
                # RESULTING DATA PER PAGE IS FORMATED IN A DICTIONARY ENTRY ###########################################
                for i, item in enumerate(r_loc_results_raw):
                    #print('>%s>>>%s' % (i, item['name']))
                    r_loc_tempLocation = '%s,%s' % (
                        item['geometry']['location']['lng'], item['geometry']['location']['lat'])
                    # Building Data Tree
                    dataEntry = {
                        'name': item['name'],
                        'location': r_loc_tempLocation,
                        'lat':item['geometry']['location']['lat'],
                        'lng':item['geometry']['location']['lng'],
                        'types': item['types'],
                        'icon': item['icon'],
                        'search':r_loc_keywords[k],
                        'hours':r_placeDet_List_hours[i],
                        'photo':r_placeDet_List_photo[i],
                        'address':r_placeDet_List_address[i],
                        'rating':r_placeDet_List_ratings[i]
                        #'vicinity': item['vicinity']
                    }
                    r_loc_finalList.append(dataEntry)
                    r_loc_finalListDups.append(r_loc_tempLocation)

                progPercent=round(k/len(r_loc_keywords)*100,2)
                print('> %s %% COMPLETE' % progPercent, end='\r')
                    # finalDic.add(dataEntry)
            print ('> 100% DONE!!                           ')
          
            # Culling all duplicates within the final list. This shit happens when the keyword search for the same thing.    
            loc_finalList4real=[]
            for i, item in enumerate(r_loc_finalListDups):
                if item not in r_loc_final4dupsTestLis:
                    r_loc_final4dupsTestLis.append(item)
                    loc_finalList4real.append(r_loc_finalList[i])

            # Final of the final of the final.... just ready to get a nice wrap in the form of a JSON file.
            loc_finalDic = dict(enumerate(loc_finalList4real))   
            loc_finalData = loc_finalDic

            # SAVE DATA OF THE LOCATIONS ##############################################################
            basePathXport=i_input_FolderDirectory
            # 1. Save Json File for Checking

            # 2. Save Final File
            # 2.a Create Folder with Today's date
            newdir = ('/%s_locations' % (dateToday_format2))
            newpath = basePathXport + newdir
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # 2.b Create the final file
            dumps_finalData = json.dumps(loc_finalData)
            fout_finalData = open("%s/%s_locations_%s.json" %(newpath, dateToday_format, f_finalNameAppendix), "w")
            #fout_finalData= open("%s/%s_Steps_dist.json" %(newpath,dateToday_format2),"w")
            fout_finalData.write(dumps_finalData)
            print('> DATA SAVED!\n')



            #########################################################################################################################################################
            ## GOOGLE MAPS ROUTES API REQUEST ########################################################################################################################
            #########################################################################################################################################################
            print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>> GOOGLE ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            
            # INPUT DATA ############################################################
            
            # Origin Points (list) ##########################
            route_inputListOrigin=[]
            route_listOr=[]
            ## This loop gets the points retrieved from the google locations search
            for i,item in enumerate(loc_finalData):
                route_listOr.append('%s,%s' %(loc_finalData[i]['lat'],loc_finalData[i]['lng']))

            route_inputListOrigin=route_listOr

            # Destination Points (list) #####################
            route_inputDestination_SiteLocation= i_input_location
            route_inputListDestination=[]
            route_inputListDestination.append(route_inputDestination_SiteLocation)
            print ('> There are %s routes to be analyzed' %(len(route_inputListDestination)) )

            # Mode of Transportation ########################
            r_route_inputMode= ['walking','driving','bicycling','transit']

            ## Set default value for inputModeSel
            r_route_inputMode_selection = 'walking'

            ## Check if i_input_Mode exists and is in inputMode
            try:
                i_input_Mode
            except NameError:
                print("> i_input_Mode is not defined")
            else:
                if i_input_Mode in r_route_inputMode:
                    r_route_inputMode_selection = i_input_Mode
                    print(f"> Travel Mode is set to... {r_route_inputMode_selection} !")
                else:
                    print(
                        f"> The value of i_input_Mode is not in the inputMode list, inputModeSel remains as {r_route_inputMode_selection}")


            ## LOOP FOR ORIGINS ######################################################
            nameAppendixRoutes='Route_%s_%s'%(f_appendix_keywords,r_route_inputMode_selection) #This is used for naming the file that will be saved
            finalDataRoute={} # This the final Dic that will be saved as a JSON file.

            print('\n> INITIATE ROUTE ANALYSIS: \n')
            for e in range(len(route_inputListDestination)):
                time.sleep(1)
                progPercentTempList=[]
                #sleep(random.randint(1, 4)) ... this was used as a way to give time between requests and to not make the API to freakout!
                for i in range(len(route_inputListOrigin)):
                    
                    ## PARAMETERS PER REQUEST TYPE ###########################################
                    params_dir = {
                        'origin': route_inputListOrigin[i],
                        'destination': route_inputListDestination[e],
                        'mode':r_route_inputMode_selection,
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
                    basePathXport=i_input_FolderDirectory
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

                progPercent=round(i/len(route_inputListDestination)*100)
                print('>%s %% COMPLETE' % progPercent, end='\r')

            print ('>100% DONE!!                  ')
            #print('6. Final Updated Data Tree: %s'% (finalDataRoute))
            print("____________________________________________________________________________________")
            print('\n\nANALYSIS DONE!!!!!!!!!!!!\n\n')
            print("_____________________+88_\n______________________+880_\n______________________++88_\n______________________++88_\n_______________________+880_________________________++_\n_______________________+888________________________+88_\n_______________________++880______________________+88_\n_______________________++888_____+++88__________+++8_\n_______________________++8888__+++8880++88____+++88_\n_______________________+++8888+++8880++8888__++888_\n________________________++888++8888+++888888++888_\n________________________++88++8888++8888888++888_\n________________________++++++888888888888888888_\n_________________________++++++88888888888888888_\n_________________________++++++++000888888888888_\n__________________________+++++++000088888888888_\n___________________________+++++++00088888888888_\n____________________________+++++++088888888888_\n____________________________+++++++088888888888_\n_____________________________+++++++8888888888_\n_____________________________+++++++0088888888_\n_____________________________++++++0088888888_\n_____________________________+++++0008888888_\n_____________________________#############_")



window.close()
exit()

