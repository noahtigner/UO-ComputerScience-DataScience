import parcel   # Import the module containing our Parcel class

myparcel = parcel.Parcel("SFR", 125000) # Instantiate an object of class Parcel
print(f"Land use: {myparcel.landuse}")  # print some of our object's member variables
print(f"Value: ${myparcel.value:,.2f}") 
mytax = myparcel.assessment()           # Call our object's assessment method
print(f"Tax assessment: ${mytax:,.2f}") # print return val of previous call
