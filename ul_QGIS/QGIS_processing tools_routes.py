import json
import math
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsFeature, QgsField, QgsFields, QgsGeometry, 
                       QgsPointXY, QgsVectorLayer, QgsProject)

# Define haversine function to calculate distance between two coordinates on Earth
def haversine(coord1, coord2):
    R = 6371.0  # radius of Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlon = math.radians(lon2 - lon1)  # convert difference in longitude coordinates to radians
    dlat = math.radians(lat2 - lat1)  # convert difference in latitude coordinates to radians

    # calculate haversine
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance * 3280.84  # convert kilometers to feet

# Define file paths
jFile01="C:/Loc2Route/230515_routes/230515_finalDataRoute_Route_Restaurant-Bar-Food-Brewery-Dining_toNFAB_walking.json"
jFile02="C:/Loc2Route/230515_routes/230515_finalDataRoute_Route_CulturalCenter-Museum-ArtGallery-LectureHall_toNFAB_walking.json"

# Create dictionary with file paths and their corresponding prefixes
filepaths = {jFile01: 'prefix1', 
             jFile02: 'prefix2'}

# Loop over each file path in the dictionary
for filepath, prefix in filepaths.items():
    # Load JSON file
    with open(filepath) as f:
        data = json.load(f)

    # Create new memory layers for polylines and points and define their schema
    vl_lines = QgsVectorLayer("LineString", f"{prefix}_Polylines", "memory")
    pr_lines = vl_lines.dataProvider()
    pr_lines.addAttributes([QgsField("id", QVariant.String),
                            QgsField("totalDistance", QVariant.Int),
                            QgsField("totalDuration", QVariant.Int),
                            QgsField("travelMode", QVariant.String)])
    vl_lines.updateFields()

    vl_points = QgsVectorLayer("Point", f"{prefix}_Points", "memory")
    pr_points = vl_points.dataProvider()
    pr_points.addAttributes([QgsField("id", QVariant.String),
                             QgsField("stepType", QVariant.String)])
    vl_points.updateFields()

    # Loop over JSON entries and add them to the layers
    for key, value in data.items():
        steps = value['data_steps']
        
        # Create an empty QgsFeature for polyline and set its attributes
        feature_line = QgsFeature()
        feature_line.setAttributes([key, 
                                    value['data_gral']['totalDistance'], 
                                    value['data_gral']['totalDuration'], 
                                    value['data_gral']['travelMode']])
        
        # Define polyline points
        points = [QgsPointXY(float(x.split(',')[0]), float(x.split(',')[1])) for x in steps['stepStartPt']]
        points.append(QgsPointXY(float(steps['stepEndPt'][-1].split(',')[0]), float(steps['stepEndPt'][-1].split(',')[1])))

        # Create a polyline from the points and set it as the feature's geometry
        feature_line.setGeometry(QgsGeometry.fromPolylineXY(points))

        # Add feature to the polyline layer
        pr_lines.addFeature(feature_line)

        # Add points to point layer
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]

            # Calculate the distance between the two points in feet
            distance = haversine((start.x(), start.y()), (end.x(), end.y()))
            
            # Calculate the number of points to be created
            num_points = int(distance / 50)  # 50ft interval

            # Create interpolated points
            for j in range(num_points + 1):
                fraction = j / num_points if num_points != 0 else 1

                # Calculate interpolated point
                interp_x = start.x() + fraction * (end.x() - start.x())
                interp_y = start.y() + fraction * (end.y() - start.y())
                interp_point = QgsPointXY(interp_x, interp_y)

                # Create an empty QgsFeature for point and set its attributes
                feature_point = QgsFeature()
                feature_point.setAttributes([key, 
                                             "start" if interp_point == start else "end" if interp_point == end else "interpolated"])

                # Set the point as the feature's geometry
                feature_point.setGeometry(QgsGeometry.fromPointXY(interp_point))

                # Add feature to the point layer
                pr_points.addFeature(feature_point)

    # Update the layers' extents
    vl_lines.updateExtents()
    vl_points.updateExtents()

    # Add layers to the map
    QgsProject.instance().addMapLayer(vl_lines)
    QgsProject.instance().addMapLayer(vl_points)
