"""camera_pid controller.
"""

import math
import statistics

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


def main():
    robot = Car()
    driver = Driver()

    timestep = int(robot.getBasicTimeStep())

    camera = robot.getDevice("camera")
    assert isinstance(camera, Camera)
    camera.enable(timestep)
    display_view = Display("display_image")
    speed = 10
    while robot.step() != -1:
        image = get_image(camera)
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(grey_image, ksize=(5, 5), sigmaX=0, sigmaY=0)
        borders_mask = cv2.Canny(blurred_image, 150, 200, None, 3)
        cropped_image = _filter_region_of_interest(borders_mask)
        lines = cv2.HoughLinesP(cropped_image, rho=5, theta=math.pi/180, threshold=22, lines=None,
                                minLineLength=1, maxLineGap=7)
        if lines is not None:
            for line in lines:
                cv2.line(cropped_image, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (127,))
            angle = get_angle_from_road_line(lines)
        else:
            angle = 0
        print(f"Angle: {angle * 180}")
        _display_image(display_view, cropped_image)
        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(speed)


def get_angle_from_road_line(lines: np.ndarray) -> float:
    H_MID = 128 / 2
    x1s, x2s = [], []
    for line in lines:
        line_height = abs(line[0][1] - line[0][3])
        x1s.append(line[0][0] - H_MID)
        x2s.append((line[0][2] - H_MID) / line_height)
    x1 = statistics.mean(x1s)
    x2 = statistics.mean(x2s)
    try:
        coeff = 0.005
        angle = x1 * coeff
        return angle
    except ZeroDivisionError:
        return 0


def _filter_region_of_interest(img: np.ndarray):
    img_height, img_width = img.shape
    centre_rectangle = np.array([[
        [0 * img_width, img_height],
        [img_width * 0.5, img_height * 0.6],
        [1 * img_width, img_height]
    ]], dtype=np.int32)
    region_filter = np.zeros_like(img)
    PIXEL_VALUE = 255,
    cv2.fillPoly(region_filter, centre_rectangle, PIXEL_VALUE) # type: ignore
    filtered_image = cv2.bitwise_and(img, region_filter)
    return filtered_image

def _display_image(display_view: Display, image: np.ndarray):
    img_width = image.shape[1]
    img_height = image.shape[0]
    rgb_image = np.dstack((image, image, image))
    image_ref = display_view.imageNew(
        rgb_image.tobytes(),
        Display.RGB,
        width=img_width,
        height=img_height)
    display_view.imagePaste(image_ref, 0, 0, False)
    display_view.imageDelete(image_ref)


if __name__ == "__main__":
    main()