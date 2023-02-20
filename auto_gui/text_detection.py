import keras_ocr
from thefuzz import process

from auto_gui import error


class TextDetection(object):
    def __init__(self, **data):
        self.img = data.get("img")
        self.generate_prediction_groups()

    def generate_prediction_groups(self):
        pipeline = keras_ocr.pipeline.Pipeline()
        self.prediction_groups = pipeline.recognize([self.img])

    def get_text_positions(self, match_text):
        if not isinstance(match_text, str):
            raise Exception(error.INVALID_TEXT_TYPE)

        if len(self.prediction_groups[0]) == 0:
            raise Exception(error.TEXT_NOT_FOUND)

        # Remove duplicate
        all_text = set()
        map_text_box = {}
        for text, box in self.prediction_groups[0]:
            value = map_text_box.get(text)
            if value == None:
                map_text_box[text] = [box]
            else:
                map_text_box[text] = value.append(box)

            all_text.add(text)

        all_text = list(all_text)

        best_match_text = process.extractBests(match_text, all_text, limit=1)[0][0]

        match_boxes = map_text_box.get(best_match_text)
        match_centers = []
        for match_box in match_boxes:
            match_centers.append(self.get_center_box(match_box))

        return match_centers

    def get_center_box(self, box):
        x_center = 0
        y_center = 0
        count = 0
        for point in box:
            count += 1
            x_center += point[0]
            y_center += point[1]

        return [x_center / count, y_center / count]
