# Quarob parameters

# Length (in meter)
body_len = 0.1185
shoulder_width = 0.0642
thigh_len = 0.0420
calf_len = 0.0417
feet_radius = 0.010

# Weight (in kilogram)
body_weight = 0.1052
hip_weight = 0.003
thigh_weight = 0.005
calf_weight = 0.003
servo_weight = 0.0134
total_weight = body_weight + \
    (hip_weight+thigh_weight+calf_weight)*4+servo_weight*12
