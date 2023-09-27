import sys
import csv
import gpxpy

gpx = gpxpy.gpx.GPX()
reader = csv.DictReader(sys.stdin)
for row in reader:
    w = gpxpy.gpx.GPXWaypoint(
        latitude=row["Lat"],
        longitude=row["Lng"],
        name=row["Location"],
        type=row["Type"],
    )
    gpx.waypoints.append(w)

sys.stdout.write(gpx.to_xml())
