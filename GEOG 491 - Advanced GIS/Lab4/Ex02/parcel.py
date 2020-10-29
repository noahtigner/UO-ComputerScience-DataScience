class Parcel:
    
    # Default Constructor,
    # Instantiates an object and assigns it the given variables
    def __init__(self, landuse, value):
        # set object's member variables
        self.landuse = landuse
        self.value = value

    # Class Method, returns value * rate based on object's landuse and value
    def assessment(self):
        if self.landuse == "SFR":
            rate = 0.05
        elif self.landuse == "MFR":
            rate = 0.04
        else:
            rate = 0.02

        assessment = self.value * rate
        return assessment
