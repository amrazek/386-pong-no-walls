import pygame
import collections
import math


def rect_clamp_point_ip(rect, point):
    if point[0] < rect.left:
        point[0] = rect.left
    elif point[0] > rect.right:
        point[0] = rect.right

    if point[1] < rect.top:
        point[1] = rect.top
    elif point[1] > rect.bottom:
        point[1] = rect.bottom


def line_circle_intersection(origin, radius, p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    p1mox = p1.x - origin.x
    p1moy = p1.y - origin.y

    a = dx * dx + dy * dy
    b = 2 * (dx * p1mox + dy * p1moy)
    c = p1mox * p1mox + p1moy * p1moy - radius * radius

    det = b * b - 4 * a * c

    if a <= 0.0000001 or det < 0:
        # no solutions
        return ()
    elif det == 0:
        # single solution
        t = -b / (2 * a)

        # if the single solution does not lie on the parametrized line segment,
        # ignore it
        if not (0 < t < 1):
            return ()

        # convert parametrized segment intersection back into coordinate
        # and return it
        return pygame.Vector2(p1.x + t * dx, p1.y + t * dy)
    else:
        # must be two solutions
        t1 = (-b + math.sqrt(det)) / (2.0 * a)
        t2 = ((-b - math.sqrt(det)) / (2.0 * a))

        # return only solutions that lie on segment
        return [tuple((pygame.Vector2(p1.x + t * dx, p1.y + t * dy) for t in [t1, t2] if 0 <= t <= 1))]


def line_line_intersection(line1_p1, line1_p2, line2_p1, line2_p2):
    m1 = pygame.Vector2(line1_p2.x - line1_p1.x, line1_p2.y - line1_p1.y)
    m2 = pygame.Vector2(line2_p2.x - line2_p1.x, line2_p2.y - line2_p1.y)

    if (m1.x == 0 and m1.y == 0) or (m2.x == 0 and m2.y == 0):
        return ()

    if m1.dot(m2) == 1:
        return ()  # lines are parallel

    denominator = (m1.y * m2.x - m1.x * m2.y)

    t1 = ((line1_p1.x - line2_p1.x) * m2.x + (line2_p1.y - line1_p1.y) * m2.y)

    if math.isinf(t1):
        return ()  # parallel
    else:
        t2 = ((line2_p1.x - line1_p1.x) * m1.y + (line1_p1.y - line2_p1.y) * m1.x) / -denominator

        # calculate intersection points, or None if the intersection point does not lie
        # on its respective line segment
        intersection1 = pygame.Vector2(line1_p1.x + t1 * m1.x, line2_p1.y + t1 * m1.y) if 0 <= t1 <= 1 else None
        intersection2 = pygame.Vector2(line2_p1.x + t2 * m2.x, line2_p1.y + t2 * m2.y) if 0 <= t2 <= 1 else None

        if intersection1 is None and intersection2 is None:
            return ()  # no intersections on either segment
        else:
            return intersection1, intersection2


Dimensions = collections.namedtuple('Dimensions', 'width height')
