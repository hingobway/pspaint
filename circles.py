import cv2 as cv


class Color:
    def __init__(self, color):
        self.color = color

    def draw(self, img, x, y, radius):
        cv.circle(img, (x, y), radius, self.color, -1)


# class Image:
#     def __init__(self):
#         #

#     def draw(self, img, x, y, radius):

#         #


circles = [
    Color((255, 0, 0)), Color((0, 255, 0)), Color(
        (0, 0, 255)), Color((255, 255, 255)), Color((0, 0, 0))
]
