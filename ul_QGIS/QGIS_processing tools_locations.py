import json
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsVectorLayer,
                       QgsFeature,
                       QgsField,
                       QgsGeometry,
                       QgsPointXY,
                       QgsProject)

# Define the file paths and prefixes
jFile01 = "C:/Loc2Route/230603_locations/20230603_003141_locations_shopping-retail-store_300m.json"
jFile02 = "C:/Loc2Route/230603_locations/20230603_023936_locations_Gym-Climbing-Fitness-Spa-Swiming-Sport-Stadium-Arena_300m.json"

filepaths = {jFile01: 'prefix1', 
             jFile02: 'prefix2'}  # replace with your file paths and desired prefixes

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
