"""
Vectors for left side body
wumengxi@umich.edu
"""
def calculate_vector_cnn_left(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_eg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        vec_back = [(x[12]+x[13]-x[3]-x[2])/2, (y[12]+y[13]-y[3]-y[2])/2, (z[12]+z[13]-z[3]-z[2])/2]
    if bool_values[1]:
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
    if bool_values[2]:
        vec_arm = [x[14]-x[13], y[14]-y[13], z[14]-z[13]]
    if bool_values[3]:
        vec_elbow = [x[15]-x[14], y[15]-y[14], 0]
    if bool_values[4]:
        vec_leg = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
    if bool_values[5]:
        vec_knee = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee


def calculate_vector_sensor_left(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        vec_back = [(x[3]+x[9]-x[0]-x[12])/2, (y[3]+y[9]-y[0]-y[12])/2, (z[3]+z[9]-z[0]-z[12])/2]
    if bool_values[1]:
        vec_head = [x[8]-x[7], y[8]-y[7], z[8]-z[7]]
    if bool_values[2]:
        vec_arm = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
    if bool_values[3]:
        vec_elbow = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
    if bool_values[4]:
        vec_leg = [x[1]-x[0], y[1]-y[0], z[1]-z[0]]
    if bool_values[5]:
        vec_knee = [x[2]-x[1], y[2]-y[1], z[2]-z[1]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee

