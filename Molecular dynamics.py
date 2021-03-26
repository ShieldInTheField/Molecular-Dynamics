import math
from random import random
import matplotlib.pyplot as plt

# creating a time list
dt = 0.01
t = t0 = 0
time_list = [t0]
for counter in range(30000):
    t = t + dt
    time_list.append(t)

# making first state of the system randomly
location_list = []
counter = 0
flag = True
N = 64
while counter < 64:
    x = 12 * random()
    y = 12 * random()
    location = [x, y]
    if len(location_list) > 0:
        for member in location_list:
            distant = math.sqrt(
                abs(
                    ((member[1] - location[1]) * (member[1] - location[1]))
                    - ((member[0] - location[0]) * (member[0] - location[0]))
                )
            )
            if distant < math.pow(2, (1 / 6)):
                flag = False
            else:
                flag = True
    if flag == True:
        location_list.append(location)
        counter = counter + 1
    # print('counter',counter)

x_list = []
y_list = []
for member in location_list:
    x_list.append(member[0])
    y_list.append(member[1])

# plt.plot(x_list,y_list,'o')
# plt.show()

# determining initial speed of particels
velocity_x_list = []
velocity_y_list = []
T = 2.2
KE = 63 * T
KEO = 0
sum_velocity_x = 0
sum_velocity_y = 0
for member in location_list:
    initial_velocity_x = random() - 0.5
    initial_velocity_y = random() - 0.5
    sum_velocity_x = sum_velocity_x + initial_velocity_x
    sum_velocity_y = sum_velocity_y + initial_velocity_y
    KEO = KEO + (
        (1 / 2) * (initial_velocity_x * initial_velocity_x)
        + (initial_velocity_y * initial_velocity_y)
    )
    velocity_x_list.append(initial_velocity_x)
    velocity_y_list.append(initial_velocity_y)

for counter in range(len(velocity_x_list)):
    velocity_x_list[counter] = (
        velocity_x_list[counter] - (sum_velocity_x / N)
    ) * math.sqrt(KE / KEO)
    velocity_y_list[counter] = (
        velocity_y_list[counter] - (sum_velocity_y / N)
    ) * math.sqrt(KE / KEO)

# defining force and potential functions
def potential(r):
    U = 4 * (math.pow((1 / r), 12) - math.pow((1 / r), 6))
    return U


def force(r):
    f = (24 / r) * ((2 * math.pow((1 / r), 12)) - math.pow((1 / r), 6))
    return f


# defining verlet algorithm
def verlet_location(dimension, speed, acceleration):
    result = dimension + (speed * dt) + ((1 / 2) * acceleration * dt * dt)
    return result


def verlet_speed(speed, acceleration, next_acceleration):
    result = speed * ((1 / 2) * (acceleration + next_acceleration) * dt)
    return result


# calculating acceleration
L = 12
acceleration_list_x = []
acceleration_list_y = []
for counter in range(N):
    acceleration_list_x.append(0)
    acceleration_list_y.append(0)

for first_counter in range(0, N - 1):
    for second_counter in range(first_counter + 1, N):
        dx = x_list[first_counter] - x_list[second_counter]
        dy = y_list[first_counter] - y_list[second_counter]
        if dx > 0.5 * L:
            dx = dx - L
        elif dx < -0.5 * L:
            dx = dx + L
        else:
            dx = dx

        if dy > 0.5 * L:
            dy = dy - L
        elif dy < -0.5 * L:
            dy = dy + L
        else:
            dx = dx

        distance = math.sqrt((dx * dx) + (dy * dy))
        f_total = force(distance)
        f_x = f_total * math.cos(math.atan(dy / dx))
        f_y = f_total * math.sin(math.atan(dy / dx))
        acceleration_list_x[first_counter] = acceleration_list_x[first_counter] + f_x
        acceleration_list_y[first_counter] = acceleration_list_y[first_counter] + f_y
        acceleration_list_x[second_counter] = acceleration_list_x[second_counter] - f_x
        acceleration_list_y[second_counter] = acceleration_list_y[second_counter] - f_y

location_output = open("location.xyz", "w")
for main_counter in range(30000):
    acc_temp_x_list = []
    acc_temp_y_list = []
    for temp_counter in range(N):
        x_temp = acceleration_list_x[temp_counter]
        y_temp = acceleration_list_y[temp_counter]
        acc_temp_x_list.append(x_temp)
        acc_temp_y_list.append(y_temp)

    for third_counter in range(N):
        x_list[third_counter] = verlet_location(
            x_list[third_counter],
            velocity_x_list[third_counter],
            acceleration_list_x[third_counter],
        )
        y_list[third_counter] = verlet_location(
            y_list[third_counter],
            velocity_y_list[third_counter],
            acceleration_list_y[third_counter],
        )

        if x_list[third_counter] > L:
            x_list[third_counter] = x_list[third_counter] - L
        elif x_list[third_counter] < 0:
            x_list[third_counter] = x_list[third_counter] + L

        if y_list[third_counter] > L:
            y_list[third_counter] = y_list[third_counter] - L
        elif y_list[third_counter] < 0:
            y_list[third_counter] = y_list[third_counter] + L

    for first_counter in range(0, N - 1):
        for second_counter in range(first_counter + 1, N):
            dx = x_list[first_counter] - x_list[second_counter]
            dy = y_list[first_counter] - y_list[second_counter]
            if dx > 0.5 * L:
                dx = dx - L
            elif dx < -0.5 * L:
                dx = dx + L
            else:
                dx = dx

            if dy > 0.5 * L:
                dy = dy - L
            elif dy < -0.5 * L:
                dy = dy + L
            else:
                dx = dx

            distance = math.sqrt((dx * dx) + (dy * dy))
            f_total = force(distance)
            f_x = f_total * math.cos(math.atan(dy / dx))
            f_y = f_total * math.sin(math.atan(dy / dx))
            acceleration_list_x[first_counter] = (
                acceleration_list_x[first_counter] + f_x
            )
            acceleration_list_y[first_counter] = (
                acceleration_list_y[first_counter] + f_y
            )
            acceleration_list_x[second_counter] = (
                acceleration_list_x[second_counter] - f_x
            )
            acceleration_list_y[second_counter] = (
                acceleration_list_y[second_counter] - f_y
            )

    for fourth_counter in range(N):
        velocity_x_list[fourth_counter] = verlet_speed(
            velocity_x_list[fourth_counter],
            acc_temp_x_list[fourth_counter],
            acceleration_list_x[fourth_counter],
        )
        velocity_y_list[fourth_counter] = verlet_speed(
            velocity_y_list[fourth_counter],
            acc_temp_y_list[fourth_counter],
            acceleration_list_y[fourth_counter],
        )

        if main_counter % 1000 == 0 and main_counter != 0:
            velocity_x_list[fourth_counter] = velocity_x_list[fourth_counter] - 0.9
            velocity_y_list[fourth_counter] = velocity_y_list[fourth_counter] - 0.9

    if main_counter % 20 == 0:
        location_output.write("64\n")
        location_output.write("MD2\n")
        for local_counter in range(64):
            string = (
                "Ar "
                + str(x_list[local_counter])
                + " "
                + str(y_list[local_counter])
                + "\n"
            )
            location_output.write(string)

    print(main_counter)
location_output.close()