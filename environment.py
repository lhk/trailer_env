import pygame
import colors
import params
import utils

import numpy as np

class Environment():
    def __init__(self, screen_size, car_size, num_obstacles):
        pygame.init()

        # the surface on which everything is rendered
        self.view = pygame.Surface(screen_size)

        # loading assets
        self.car = pygame.image.load("assets/car.png")
        self.car = pygame.transform.smoothscale(self.car, params.car_size)

        self.black = pygame.Surface(params.obstacle_size)
        self.black.fill(colors.black)

        self.green = pygame.Surface(params.goal_size)
        self.green.fill(colors.green)

        # set up car, obstacle and goal positions
        self.car_position = np.random.rand(2) * params.screen_size
        self.goal_position = np.random.rand(2) * params.screen_size

        self.car_dim = np.linalg.norm(params.car_size)
        self.goal_dim = np.linalg.norm(params.goal_size)
        self.obs_dim = np.linalg.norm(params.obstacle_size)

        min_dist = 2 * (self.car_dim + self.obs_dim + self.goal_dim)

        self.obstacle_positions = []
        for i in range(params.num_obstacles):
            while True:
                obstacle_position = np.random.rand(2) * params.screen_size
                # obstacle must be away from car and goal
                car_dist = np.linalg.norm(obstacle_position - self.car_position)
                goal_dist = np.linalg.norm(obstacle_position - self.goal_position)

                if car_dist > min_dist and goal_dist > min_dist:
                    self.obstacle_positions.append(obstacle_position)
                    break

        # set up values for dynamics
        self.car_rotation = 0
        self.car_speed = 0

    def make_action(self, acceleration, steering_angle, dT = 0.5):
        acceleration = np.clip(acceleration, -1, 1)
        steering_angle = np.clip(steering_angle, -1, 1)

        # TODO: fill with proper single track model
        self.car_speed += acceleration * dT
        self.car_speed = np.clip(self.car_speed, -1, 10)
        x, y = self.car_position
        new_x = x - np.sin(self.car_rotation / 180 * np.pi)*self.car_speed*dT
        new_y = y - np.cos(self.car_rotation / 180 * np.pi)*self.car_speed*dT

        if new_x > params.screen_size[0]:
            self.car_speed = 0
            new_x = params.screen_size[0]
        elif new_x < 0:
            self.car_speed = 0
            new_x = 0

        if new_y > params.screen_size[1]:
            self.car_speed = 0
            new_y = params.screen_size[1]
        elif new_y < 0:
            self.car_speed = 0
            new_y = 0

        self.car_position=(new_x, new_y)



        self.car_rotation -= self.car_speed * steering_angle * dT

        for obstacle in self.obstacle_positions:
            dist_obs = np.linalg.norm(obstacle - self.car_position)
            if dist_obs < 0.5*(self.car_dim + self.obs_dim):
                # collision with obstacle
                return params.reward_collision, True

        dist_goal = np.linalg.norm(self.goal_position - self.car_position)
        if dist_goal < 0.5*(self.car_dim + self.goal_dim):
            return params.reward_goal, True

        return params.reward_timestep, False


    def render(self, return_numpy = True):
        self.view.fill(colors.white)

        # plot all the obstacles
        self.view.fill(colors.white)
        for obstacle_position in self.obstacle_positions:
            self.view.blit(self.black, obstacle_position)

        # plot the goal
        self.view.blit(self.green, self.goal_position)

        car_rect = self.car.get_rect()
        car_rect.center = self.car_position

        rotated_surface, rotated_rect = utils.rotate(self.car, car_rect, self.car_rotation)
        self.view.blit(rotated_surface, rotated_rect)

        if return_numpy:
            # get numpy surface
            np_arr = pygame.surfarray.array3d(self.view)

            return np_arr

        else:
            return self.view