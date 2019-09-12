import pygame
import collections

def rect_clamp_point_ip(rect, point):
    if point[0] < rect.left:
        point[0] = rect.left
    elif point[0] > rect.right:
        point[0] = rect.right

    if point[1] < rect.top:
        point[1] = rect.top
    elif point[1] > rect.bottom:
        point[1] = rect.bottom

Dimensions = collections.namedtuple('Dimensions', 'width height')