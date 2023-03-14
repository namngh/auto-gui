import cv2
import numpy as np

THRESHOLD = 0.8

class MatchTemplate():
    def __init__(self, **kwargs):
        self.img_gray = cv2.cvtColor(kwargs.get("img"), cv2.COLOR_BGR2GRAY)
        

    def get_template_positions(self, template):
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template_width, template_height = template.shape[::-1]

        res = cv2.matchTemplate(self.img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        loc = np.where( res >= THRESHOLD)
        positions = []
        for pt in zip(*loc[::-1]):
            positions.push([pt[0] + template_width / 2, pt[1] + template_height / 2])

        return positions