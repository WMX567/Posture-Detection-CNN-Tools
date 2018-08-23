"""
Vectors for right side body
wumengxi@umich.edu
"""
def calculate_vector_cnn_right(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        #vec_back = [(x[12]+x[13]-x[3]-x[2])/2, (y[12]+y[13]-y[3]-y[2])/2, (z[12]+z[13]-z[3]-z[2])/2]
        vec_back = [x[12]-x[3], y[12]-y[3], z[12]-z[3]]
    if bool_values[1]:
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
    if bool_values[2]:
        vec_arm = [x[11]-x[12], y[11]-y[12], z[11]-z[12]]
    if bool_values[3]:
        vec_elbow = [x[10]-x[11], y[10]-y[11], 0]
    if bool_values[4]:
        vec_leg = [x[1]-x[2], y[1]-y[2], z[1]-z[2]]
    if bool_values[5]:
        vec_knee = [x[0]-x[1], y[0]-y[1], z[0]-z[1]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee


def calculate_vector_sensor_right(x, y, z, bool_values):
    vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = ([] for i in range(6))
    if bool_values[0]:
        #vec_back = [(x[3]+x[9]-x[0]-x[12])/2, (y[3]+y[9]-y[0]-y[12])/2, (z[3]+z[9]-z[0]-z[12])/2]
        vec_back = [x[3]-x[0],y[3]-y[0],z[3]-z[0]]
    if bool_values[1]:
        vec_head = [x[8]-x[7], y[8]-y[7], z[8]-z[7]]
    if bool_values[2]:
        vec_arm = [x[10]-x[9], y[10]-y[9], z[10]-z[9]]
    if bool_values[3]:
        vec_elbow = [x[11]-x[10], y[11]-y[10], z[11]-z[10]]
    if bool_values[4]:
        vec_leg = [x[13]-x[12], y[13]-y[12], z[13]-z[12]]
    if bool_values[5]:
        vec_knee = [x[14]-x[13], y[14]-y[13], z[14]-z[13]]
    return vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee

