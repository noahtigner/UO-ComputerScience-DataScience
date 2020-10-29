landuse = "SFR"
value = 125000
if landuse == "SFR":
    rate = 0.05
elif landuse == "MFR":
    rate = 0.04
else:
    rate = 0.02

assessment = value * rate
print(f"${assessment:.2f}")
