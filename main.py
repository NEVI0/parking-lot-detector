import cv2
import pickle
import keyboard

from constants import WINDOW, PARKING, SPACE_COLORS, TEXT

try:
    with open('parking_lot_positions', 'rb') as file_to_read:
        parking_lot_positions = pickle.load(file_to_read)
except:
    parking_lot_positions = []


def add_text(image, text, color) -> None:
    cv2.putText(image, text, (30, 50), TEXT['FONT'], TEXT['SCALE'], color, TEXT['SIZE'], cv2.LINE_AA)


def add_parking_lot_space(events, x, y, flags, is_editable) -> None:
    if not is_editable:
        return

    if events == cv2.EVENT_LBUTTONDOWN:
        parking_lot_positions.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for index, position in enumerate(parking_lot_positions):
            x1, y1 = position

            if x1 < x < x1 + PARKING['WIDTH'] and y1 < y < y1 + PARKING['HEIGHT']:
                parking_lot_positions.pop(index)

    with open('parking_lot_positions', 'wb') as file_to_write:
        pickle.dump(parking_lot_positions, file_to_write)


def main():
    is_using_editable_mode = False

    while True:
        parking_lot_image = cv2.imread('parking-lot-image.png')

        if is_using_editable_mode:
            add_text(parking_lot_image, 'Editable mode is enabled! Press "Q" to quit', TEXT['COLORS']['RED'])
        else:
            add_text(parking_lot_image, 'Press "E" to edit parking lot spaces', TEXT['COLORS']['BLUE'])

        for position in parking_lot_positions:
            pos1, pos2 = position, (position[0] + PARKING['WIDTH'], position[1] + PARKING['HEIGHT'])
            cv2.rectangle(parking_lot_image, pos1, pos2, SPACE_COLORS['AVAILABLE'], 2)

        cv2.imshow(WINDOW['NAME'], parking_lot_image)

        if keyboard.is_pressed('e'):
            is_using_editable_mode = True
        if keyboard.is_pressed('q'):
            is_using_editable_mode = False

        cv2.setMouseCallback(WINDOW['NAME'], add_parking_lot_space, is_using_editable_mode)
        cv2.waitKey(1)

        if cv2.getWindowProperty(WINDOW['NAME'], cv2.WND_PROP_VISIBLE) < 1:
            break


if __name__ == '__main__':
    main()
