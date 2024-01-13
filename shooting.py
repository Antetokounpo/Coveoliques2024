import numpy as np
from game_message import Vector

class Shooting:
    def rotate_coords(self, v: Vector, angle: float):
        new_x = v.x * np.cos(angle) - v.y * np.sin(angle)
        new_y = -v.x * np.sin(angle) + v.y * np.cos(angle)

        return Vector(new_x, new_y)

    def show_position_at_time(self, cannon_position, rocket_speed, shooting_angle, meteor_position, meteor_velocity, t):
        meteor_pos_x = meteor_position.x + meteor_velocity.x*t
        meteor_pos_y = meteor_position.y + meteor_velocity.y*t

        rocket_pos_x = cannon_position.x + rocket_speed*np.cos(shooting_angle)*t
        rocket_pos_y = cannon_position.y + rocket_speed*np.sin(shooting_angle)*t

        print(f"Time : {t}")
        print(f"Meteor : ({meteor_pos_x}, {meteor_pos_y})")
        print(f"Rocket : ({rocket_pos_x}, {rocket_pos_y})")

    def get_shooting_angle(self, cannon_position: Vector, rocket_speed: float, meteor_position: Vector, meteor_velocity: Vector):
        meteor_pos = Vector(meteor_position.x - cannon_position.x, meteor_position.y - cannon_position.y)

        angle_with_x_axis = np.arctan2(meteor_pos.y, meteor_pos.x)

        meteor_pos = self.rotate_coords(meteor_pos, angle_with_x_axis)
        meteor_vel = self.rotate_coords(meteor_velocity, angle_with_x_axis)

        shooting_angle = np.arcsin(meteor_vel.y/rocket_speed)

        t = (-meteor_pos.x)/(meteor_vel.x - rocket_speed*np.cos(shooting_angle))
        self.show_position_at_time(cannon_position, rocket_speed, shooting_angle, meteor_position, meteor_velocity, t)

        return shooting_angle+angle_with_x_axis

    def distance_from_cannon(self, cannon: Vector, meteor: Vector):
        return np.linalg.norm([meteor.x - cannon.x, meteor.y - cannon.y])
