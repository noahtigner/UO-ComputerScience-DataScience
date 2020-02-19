# Test data for polyline simplifier

The test data is in comma-separated values form (.csv). The points are in UTM format, meaning they are meters east and meters north of a UTM zone origin.  Easting and northing values treat a region of the earth as if it were flat, so they are reasonably accurate only for limited distances.  Their advantage and the reason they are used here is that "meters" is a uniform metric in the x and y direction, so you can directly do distance calculations treating (easting,northing) as an (x,y) pair in the cartesian plane.  In contrast, one degree latitude and one degree longitude may be vastly different distances, and the distance represented by a degree longitude depends on the latitude (circles around the earth become shorter as you get farther from the equator). 

## Files: 

### diamond.csv
Just four points in a diamond, useful for debugging the way data is fit to the screen.  

### zigzag.csv
A short zig-zag sequence with co-linear points between extremes, for testing simplification. For example, the first three points are (0,0), (50,100), (100,200).  With any tolerance > 0, the intermediate point (50,100) should be dropped. 


### FoxHollow.csv

From [https://ridewithgps.com/routes/9582336](https://ridewithgps.com/routes/9582336), a short training route around Eugene.  A relatively small data set, with about 1500 points covering about 17 miles. 

### SmithRiverLp.csv

From [https://ridewithgps.com/routes/21564104](https://ridewithgps.com/routes/21564104), a 300km (186 mile) loop from Eugene to Florence to Reedsport to Eugene.  About 10,000 points. 

## Peculiarities

### Zone
Easting and northing values are relative to the origin of some UTM zone, but these files do not include the zone.  (I believe they are all in zone 9.) 

### Rounding

These (easting,northing) values have been rounded to the nearest meter to make the files more compact and easier to read.  In some places the rounding has resulted in duplicate points.  For example,  SmithRiverLp.csv contains the subsequence 

```
492943,4877908
492943,4877915
492943,4877915
492943,4877915
492942,4878024
```

In the original GPX file from RideWithGPS, the three middle values presumably had different values after the decimal point.  But since these values are in meters, this means they were within 1 meter of each other, so for our purposes it is fine to treat them as the same point. 
