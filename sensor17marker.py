"""
17 markers sensor
Cal angles tracked by sensor
return elbow, shoulder, back, knee, neck angles
wumengxi@umich.edu
"""

def calculate_vector_sensor_17(x, y, z, bool_values):
    vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee = ([] for i in range(6))
    if bool_values[0]:
        vec_back = [(x[3]+x[10]-x[0]-x[14])/2, (y[3]+y[10]-y[0]-y[14])/2, (z[3]+z[10]-z[0]-z[14])/2]
    if bool_values[1]:
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
    if bool_values[2]:
        vec_left_arm = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
    if bool_values[3]:
        vec_left_elbow = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
    if bool_values[4]:
        vec_left_leg = [x[1]-x[0], y[1]-y[0], z[1]-z[0]]
    if bool_values[5]:
        vec_left_knee = [x[2]-x[1], y[2]-y[1], z[2]-z[1]]
    return vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee
    
    
