import pygame
from pygame.locals import *
import math

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, radius, ball_color, velocity_vector):
        super(Ball, self).__init__()


        self.velocity = velocity_vector
        self.radius = radius
        self.bounds = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.position = pygame.Vector2((self.bounds.centerx, self.bounds.centery))

        # this will be an image later, so might as well save some time and
        # make it a surface to begin with
        self.image = pygame.Surface((radius * 2, radius * 2), HWSURFACE)
        self.image = self.image.convert()

        mask_color = (0, 0, 0)
        self.image.set_colorkey(mask_color)
        self.image.fill(mask_color)

        pygame.draw.circle(self.image, ball_color, (radius, radius), radius)

        self.rect = pygame.Rect(200, 200, radius, radius)

    def update(self, elapsed_seconds):
        self.position += self.velocity * elapsed_seconds
        self.rect.centerx = int(self.position.x)
        self.rect.centery = int(self.position.y)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, size, speed, bounds):
        #super(Paddle, self).__init__()
        super().__init__()

        self.speed = speed
        self.bounds = bounds
        self.size = size
        self.image = pygame.Surface(size)
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        yellow = (255, 242, 0)
        self.image.fill(yellow)
        self.image = self.image.convert()

        self.position = bounds.centery
        self.target_position = self.position

    def __calculate_movement(self, elapsed):
        distance_to_target = self.target_position - self.position
        return self.speed * elapsed, distance_to_target

    def update(self, elapsed_seconds):
        movement, dist_left = self.__calculate_movement(elapsed_seconds)
        direction = 1.0 if dist_left > 0 else -1.0

        if movement > math.fabs(dist_left):
            self.position = self.target_position
        else:
            self.position += movement * direction

        self.__update_rect()

    def __update_rect(self):
        raise NotImplementedError

    def move_to(self, position):
        self.target_position = position

    def get_position(self):
        return self.position


# class HorizontalPaddle(Paddle):
#     def __init__(self, size, speed, bounds):
#         super().__init__(size, speed, bounds)
#
#         self.position = self.bounds.centerx
#
#     def __update_rect(self):
#         self.rect.centerx = self.position
#         self.rect.clamp_ip(self.bounds)
#
# class VerticalPaddle(Paddle):
#     def __init__(self, size, speed, bounds):
#         super().__init__(size, speed, bounds)
#
#     def __update_rect(self):
#         self.rect.centery = self.position
#         self.rect.clamp_ip(self.bounds)