import json
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsVectorLayer,
                       QgsFeature,
                       QgsField,
                       QgsGeometry,
                       QgsPointXY,
                       QgsProject)

# Define the file paths and prefixes ###################################################

fRootLocation="C:/Loc2Route/230621_locations/"
jFile01 = fRootLocation + "20230621_151033_locations_CulturalCenter-Museum-ArtGallery-LectureHall_500m.json"
jFile02 = fRootLocation + "20230621_151033_locations_Theatre-Entertainment-Show-Cinema-ConcertHall-MusicVenue_500m.json"
jFile03 = fRootLocation + "20230621_151033_locations_Hotels-Hostel-Resort-Lodging-B&B_500m.json"
jFile04 = fRootLocation + "20230621_151033_locations_Restaurant-Bar-Food-Brewery-Dining_500m.json"
jFile05 = fRootLocation + ""


filepaths = {jFile01: 'cultural', 
             jFile02: 'entertainment',
             jFile03: 'Lodging',
             jFile04: 'FoodAndBeverage'}  # replace with your file paths and desired prefixes

#print(filepaths)

# RUNNING THE SCRIPT ###################################################################
for file_path, layer_name_prefix in filepaths.items():

    # 1. Open a JSON file
    with open(file_path) as f:
        data = json.load(f)

    # 2. Create a new Layer

    # Define the layer
    vl = QgsVectorLayer("Point", layer_name_prefix + "_Locations", "memory")

    # Access the data provider
    pr = vl.dataProvider()

    # Add necessary fields
    pr.addAttributes([QgsField("name", QVariant.String),
                      QgsField("lat", QVariant.Double),
                      QgsField("lng", QVariant.Double),
                      QgsField("icon", QVariant.String),
                      QgsField("types", QVariant.String)])

    vl.updateFields()

    # Add features
    for key, value in data.items():
        # Create a new feature
        feature = QgsFeature()

        # Join types into a single string
        types_str = ', '.join(value["types"])

        # Set attribute values
        feature.setAttributes([value["name"], value["lat"], value["lng"], value["icon"], types_str])

        # Create a new QgsPointXY object and set it as the feature's geometry
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(value["lng"], value["lat"])))

        # Add the feature to the data provider
        pr.addFeature(feature)

    # Update layer's extent when new features are added
    vl.updateExtents()

    # Add the layer to the Layers panel
    QgsProject.instance().addMapLayer(vl)
