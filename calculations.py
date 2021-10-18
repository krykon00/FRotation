 # detuning["sin2theta"] = (detuning["3"]-detuning["4"])/(detuning["3"]+detuning["4"])
# sin2Q_min = detuning['sin2theta'].min()
# sin2Q_max = detuning['sin2theta'].max()
# detuning['sin2Q_norm'] = 2*((detuning["sin2theta"] - sin2Q_min)/(sin2Q_max - sin2Q_min))-1
# detuning['rot_angle'] = detuning['sin2Q_norm'].apply(lambda x: math.asin(x)/2 )