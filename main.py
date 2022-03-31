import cv2
import keyboard

from parking_controller import ParkingController
from constants import WINDOW


def main():
    show_threshold_image = False
    is_using_editable_mode = False
    parking_video = cv2.VideoCapture('parking-lot-video.mp4')
    parking_ctrl = ParkingController()

    while True:
        if parking_video.get(cv2.CAP_PROP_POS_FRAMES) == parking_video.get(cv2.CAP_PROP_FRAME_COUNT):
            parking_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        _, parking_image = parking_video.read()

        gray_image = cv2.cvtColor(parking_image, cv2.COLOR_BGR2GRAY)
        threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

        parking_ctrl.place_editable_mode_text(parking_image, is_using_editable_mode)
        parking_ctrl.check_parking_positions(parking_image, threshold_image)

        if keyboard.is_pressed('e'):
            is_using_editable_mode = True
        if keyboard.is_pressed('q'):
            is_using_editable_mode = False

        if keyboard.is_pressed('t'):
            show_threshold_image = True
        if keyboard.is_pressed('esc'):
            show_threshold_image = False

        cv2.imshow(WINDOW['NAME'], parking_image)

        if show_threshold_image:
            cv2.imshow('Threshold Image', threshold_image)
        else:
            if cv2.getWindowProperty('Threshold Image', cv2.WND_PROP_VISIBLE):
                cv2.destroyWindow('Threshold Image')

        cv2.setMouseCallback(WINDOW['NAME'], parking_ctrl.add_parking_lot_position, (parking_image, is_using_editable_mode))
        cv2.waitKey(5)

        if cv2.getWindowProperty(WINDOW['NAME'], cv2.WND_PROP_VISIBLE) < 1:
            break


if __name__ == '__main__':
    main()
