"""
Vectors (left&right) for 17 markers sensor
wumengxi@umich.edu
"""

def calculate_vector_sensor_left_17(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        vec_back = [(x[3]+x[10]-x[0]-x[14])/2, (y[3]+y[10]-y[0]-y[14])/2, (z[3]+z[10]-z[0]-z[14])/2]
    if bool_values[1]:
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
    if bool_values[2]:
        vec_arm = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
    if bool_values[3]:
        vec_elbow = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
    if bool_values[4]:
        vec_leg = [x[1]-x[0], y[1]-y[0], z[1]-z[0]]
    if bool_values[5]:
        vec_knee = [x[2]-x[1], y[2]-y[1], z[2]-z[1]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee


def calculate_vector_sensor_right_17(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        vec_back = [(x[3]+x[10]-x[0]-x[14])/2, (y[3]+y[10]-y[0]-y[14])/2, (z[3]+z[10]-z[0]-z[14])/2]
    if bool_values[1]:
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
    if bool_values[2]:
        vec_right_arm = [x[11]-x[10], y[11]-y[10], z[11]-z[10]]
    if bool_values[3]:
        vec_right_elbow = [x[12]-x[11], y[12]-y[11], z[12]-z[11]]
    if bool_values[4]:
        vec_right_leg = [x[15]-x[14], y[15]-y[14], z[15]-z[14]]
    if bool_values[5]:
        vec_right_knee = [x[16]-x[15], y[16]-y[15], z[16]-z[15]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee
    
