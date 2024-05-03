"""camera_pid controller.
"""

import math

import cv2
from controller import Display, Camera
import numpy as np
from vehicle import Car, Driver


def get_image(camera):
    raw_image = camera.getImage()  
    image = np.frombuffer(raw_image, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4)
    )
    return image


def display_image(display, image):
    # Image to display
    image_rgb = np.dstack((image, image,image,))
    # Display image
    image_ref = display.imageNew(
        image_rgb.tobytes(),
        Display.RGB,
        width=image_rgb.shape[1],
        height=image_rgb.shape[0],
    )
    display.imagePaste(image_ref, 0, 0, False)
    display.imageDelete(image_ref)


def main():
    robot = Car()
    driver = Driver()

    timestep = int(robot.getBasicTimeStep())

    camera = robot.getDevice("camera")
    assert isinstance(camera, Camera)
    camera.enable(timestep)
    display_view = Display("display_image")
    speed = 5
    while robot.step() != -1:
        image = get_image(camera)
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        borders_mask = cv2.Canny(grey_image, 100, 200, None, 3)
        cropped_image = _filter_region_of_interest(borders_mask)
        line = cv2.HoughLinesP(cropped_image, rho=1, theta=math.pi/180, threshold=10, lines=None,
                                minLineLength=5, maxLineGap=100)
        if line is not None:
            line = line[0]
            cv2.line(cropped_image, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (127,))
            angle = get_angle_from_road_line(line)
            print(angle)
        _display_image(display_view, cropped_image)
        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(speed)


def get_angle_from_road_line(line: np.ndarray) -> float:
    x1, y1, x2, y2 = line[0]
    angle = (y2 - y1) / (x2 - x1)
    return angle


def _filter_region_of_interest(img: np.ndarray):
    img_height, img_width = img.shape
    centre_rectangle = np.array([[
        [0.1 * img_width, img_height],
        [img_width * 0.5, img_height * 0.35],
        [0.9 * img_width, img_height]
    ]], dtype=np.int32)
    region_filter = np.zeros_like(img)
    PIXEL_VALUE = 255,
    cv2.fillPoly(region_filter, centre_rectangle, PIXEL_VALUE) # type: ignore
    filtered_image = cv2.bitwise_and(img, region_filter)
    return filtered_image

def _display_image(display_view: Display, image: np.ndarray):
    image_ref = display_view.imageNew(
        np.dstack((image, image, image)).tobytes(),
        Display.RGB,
        width=image.shape[1],
        height=image.shape[0])
    display_view.imagePaste(image_ref, 0, 0, False)
    display_view.imageDelete(image_ref)


if __name__ == "__main__":
    main()