import random

import pygame
import math
import numpy as np
from variables import global_variables
from nn import NeuralNetwork


class Player(pygame.sprite.Sprite):
    def __init__(self, game_mode):
        super().__init__()

        # loading images
        player_walk1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()

        # rotating -90 degree and scaling by factor of 0.5
        player_walk1 = pygame.transform.rotozoom(player_walk1, -90, 0.5)
        player_walk2 = pygame.transform.rotozoom(player_walk2, -90, 0.5)

        # flipping vertically
        player_walk1 = pygame.transform.flip(player_walk1, flip_x=False, flip_y=True)
        player_walk2 = pygame.transform.flip(player_walk2, flip_x=False, flip_y=True)

        self.player_walk = [player_walk1, player_walk2]

        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midleft=(177, 656))

        self.player_gravity = 'left'
        self.gravity = 10
        self.game_mode = game_mode

        if self.game_mode == "Neuroevolution":
            self.fitness = 0  # Initial fitness
            layer_sizes = [5, 20, 2]  # TODO (Design your architecture here by changing the values)
            self.nn = NeuralNetwork(layer_sizes)

    def batch_normalize(self, x):
        """

        :param x: array which want to normilize
        :param n: length of second dimension of array
        :return: return normalized array
        """
        avg = sum(x) / len(x)
        temp_sum = 0
        for j in range(len(x)):
            temp_sum += (x[j] - avg) ** 2
        temp_sum = temp_sum / len(x)
        for j in range(len(x)):
            x[j] = ((x[j] - avg) / math.sqrt(temp_sum + 0.01)) / 4

        return x

    def make_input(self, screen_width, screen_height, obstacles, player_x, player_y):
        """
                Just creates input vector of the neural network

                :param screen_width: Game's screen width which is 604.
                :param screen_height: Game's screen height which is 800.
                :param obstacles: List of obstacles that are above the player. Each entry is a dictionary having 'x' and 'y' of
                the obstacle as the key. The list is sorted based on the obstacle's 'y' point on the screen. Hence, obstacles[0]
                is the nearest obstacle to our player. It is also worthwhile noting that 'y' range is in [-100, 656], such that
                -100 means it is off screen (Topmost point) and 656 means in parallel to our player's 'y' point.
                :param player_x: 'x' position of the player
                :param player_y: 'y' position of the player
                :return 'x' is vector of inputs of first layer of neural networks
        """
        """ multiply by  2 distance of obstacles which in pleyer way """
        x = []
        x.append(player_x)
        if (len(obstacles) == 0):
            for i in range(4):
                x.append(0)
        else:
            if (len(obstacles) < 4):
                for i in range(len(obstacles)):
                    if (obstacles[i]['x'] ==177):
                        x.append(obstacles[i]['y'])
                    elif(obstacles[i]['x'] ==410):
                        x.append(-obstacles[i]['y'])
                    else:
                        x.append(obstacles[i]['y']*0.5)
                for i in range(4 - len(obstacles)):
                    x.append(0)
            else:
                for i in range(len(obstacles)):
                    if (obstacles[i]['x'] ==177):
                        x.append(obstacles[i]['y'])
                    elif (obstacles[i]['x'] == 410):
                        x.append(-obstacles[i]['y'])
                    else:
                        x.append(obstacles[i]['y'] * 0.5)
                x = x[:5]

        x = self.batch_normalize(x)
        return x

    def think(self, screen_width, screen_height, obstacles, player_x, player_y):
        """
        Creates input vector of the neural network and determines the gravity according to neural network's output.

        :param screen_width: Game's screen width which is 604.
        :param screen_height: Game's screen height which is 800.
        :param obstacles: List of obstacles that are above the player. Each entry is a dictionary having 'x' and 'y' of
        the obstacle as the key. The list is sorted based on the obstacle's 'y' point on the screen. Hence, obstacles[0]
        is the nearest obstacle to our player. It is also worthwhile noting that 'y' range is in [-100, 656], such that
        -100 means it is off screen (Topmost point) and 656 means in parallel to our player's 'y' point.
        :param player_x: 'x' position of the player
        :param player_y: 'y' position of the player
        """
        # TODO (change player's gravity here by calling self.change_gravity)
        input_array1 = self.make_input(screen_width, screen_height, obstacles, player_x, player_y)

        input_array = np.array(input_array1)
        outputs = self.nn.forward(input_array)
        maximum = max(outputs)

        if (maximum == outputs[0]):
            # print("left")
            self.change_gravity('left')
        else:
            self.change_gravity('right')

    def change_gravity(self, new_gravity):
        """
        Changes the self.player_gravity based on the input parameter.
        :param new_gravity: Either "left" or "right"
        """
        new_gravity = new_gravity.lower()

        if new_gravity != self.player_gravity:
            self.player_gravity = new_gravity
            self.flip_player_horizontally()

    def player_input(self):
        """
        In manual mode: After pressing space from the keyboard toggles player's gravity.
        """
        if global_variables['events']:
            for pygame_event in global_variables['events']:
                if pygame_event.type == pygame.KEYDOWN:
                    if pygame_event.key == pygame.K_SPACE:
                        self.player_gravity = "left" if self.player_gravity == 'right' else 'right'
                        self.flip_player_horizontally()

    def apply_gravity(self):
        if self.player_gravity == 'left':
            self.rect.x -= self.gravity
            if self.rect.left <= 177:
                self.rect.left = 177
        else:
            self.rect.x += self.gravity
            if self.rect.right >= 430:
                self.rect.right = 430

    def animation_state(self):
        """
        Animates the player.
        After each execution, it increases player_index by 0.1. Therefore, after ten execution, it changes the
        player_index and player's frame correspondingly.
        """
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):
            self.player_index = 0

        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """
        Updates the player according to the game_mode. If it is "Manual", it listens to the keyboard. Otherwise the
        player changes its location based on `think` method.
        """
        if self.game_mode == "Manual":
            self.player_input()
        if self.game_mode == "Neuroevolution":
            obstacles = []
            for obstacle in global_variables['obstacle_groups']:
                if obstacle.rect.y <= 656:
                    obstacles.append({'x': obstacle.rect.x, 'y': obstacle.rect.y})

            self.think(global_variables['screen_width'],
                       global_variables['screen_height'],
                       obstacles, self.rect.x, self.rect.y)

        self.apply_gravity()
        self.animation_state()

    def flip_player_horizontally(self):
        """
        Flips horizontally to have a better graphic after each jump.
        """
        for i, player_surface in enumerate(self.player_walk):
            self.player_walk[i] = pygame.transform.flip(player_surface, flip_x=True, flip_y=False)
