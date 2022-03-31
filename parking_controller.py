import cv2
import pickle

from constants import PARKING, TEXT, SPACE_COLORS


class ParkingController:
    def __init__(self) -> None:
        try:
            with open('parking_lot_positions', 'rb') as file_to_read:
                self.parking_positions = pickle.load(file_to_read)
        except:
            self.parking_positions = []

    @staticmethod
    def _add_text(image, text, position, color) -> None:
        cv2.putText(image, text, position, TEXT['FONT'], TEXT['SCALE'], color, TEXT['SIZE'], cv2.LINE_AA)

    @staticmethod
    def _get_position(image, position) -> None:
        x, y = position
        cropped_image = image[y:y + PARKING['HEIGHT'], x:x + PARKING['WIDTH']]
        cv2.imshow(f'Position: {x}x{y}', cropped_image)

    def place_editable_mode_text(self, image, editable) -> None:
        if editable:
            self._add_text(image, 'Editable mode is enabled! Press "Q" to quit', (20, 35), TEXT['COLORS']['RED'])
        else:
            self._add_text(image, 'Press "E" to edit parking lot positions', (20, 35), TEXT['COLORS']['BLUE'])

    def add_parking_lot_position(self, event, x, y, flags, params) -> None:
        image, editable = params

        if event == cv2.EVENT_LBUTTONDOWN and editable:
            self.parking_positions.append((x, y))

        if event == cv2.EVENT_RBUTTONDOWN:
            for index, position in enumerate(self.parking_positions):
                x1, y1 = position

                if x1 < x < x1 + PARKING['WIDTH'] and y1 < y < y1 + PARKING['HEIGHT']:
                    if not editable:
                        self._get_position(image, self.parking_positions[index])
                    else:
                        self.parking_positions.pop(index)

        with open('parking_lot_positions', 'wb') as file_to_write:
            pickle.dump(self.parking_positions, file_to_write)

    def check_parking_positions(self, normal_image, threshold_image) -> None:
        available_positions = 0

        for position in self.parking_positions:
            x, y = position
            pos1, pos2 = position, (position[0] + PARKING['WIDTH'], position[1] + PARKING['HEIGHT'])
            rectangle_color = SPACE_COLORS['NOT_AVAILABLE']

            cropped_image = threshold_image[y:y + PARKING['HEIGHT'], x:x + PARKING['WIDTH']]
            counted_pixels = cv2.countNonZero(cropped_image)

            if counted_pixels < 850:
                rectangle_color = SPACE_COLORS['AVAILABLE']
                available_positions += 1

            cv2.rectangle(normal_image, pos1, pos2, rectangle_color, 2)

        self._add_text(normal_image, f'Available: {available_positions}/{len(self.parking_positions)}', (20, 65), TEXT['COLORS']['ORANGE'])
