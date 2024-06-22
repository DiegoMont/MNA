from controller import Display, Keyboard, Robot, Camera
from vehicle import Car, Driver
import numpy as np
import cv2
from datetime import datetime
import os
import csv

# Getting image from camera
def get_image(camera):
    raw_image = camera.getImage()  
    image = np.frombuffer(raw_image, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4)
    )
    return image

# Image processing
def greyscale_cv2(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_img

# Display image 
def display_image(display, image):
    # Image to display
    image_rgb = np.dstack((image, image, image))
    # Display image
    """image_ref = display.imageNew(
        image_rgb.tobytes(),
        Display.RGB,
        width=image_rgb.shape[1],
        height=image_rgb.shape[0],
    )"""
    #display.imagePaste(image_ref, 0, 0, False)

# Initial angle and speed 
manual_steering = 0
steering_angle = 0
speed = 20

# Set target speed
def set_speed(kmh):
    global speed
    speed = kmh
    if speed < 0:
        speed = 0

# Update steering angle
def set_steering_angle(wheel_angle):
    global steering_angle
    # Check limits of steering
    if (wheel_angle - steering_angle) > 0.1:
        wheel_angle = steering_angle + 0.1
    if (wheel_angle - steering_angle) < -0.1:
        wheel_angle = steering_angle - 0.1
    if wheel_angle > 0.4:
        wheel_angle = 0.4
    elif wheel_angle < -0.4:
        wheel_angle = -0.4
    steering_angle = wheel_angle


# Validate increment of steering angle
def change_steer_angle(inc):
    global manual_steering
    # Apply increment
    new_manual_steering = manual_steering + inc
    # Validate interval 
    if new_manual_steering <= 25.0 and new_manual_steering >= -25.0: 
        manual_steering = new_manual_steering
        set_steering_angle(manual_steering * 0.02)
    # Debugging
    if manual_steering == 0:
        print("going straight")
    else:
        turn = "left" if steering_angle < 0 else "right"
        print("turning {} rad {}".format(str(steering_angle), turn))

# Main
def main():
    global manual_steering
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # Create camera instance
    camera = robot.getDevice("camera")
    camera.enable(timestep)  # timestep

    # Processing display
    display_img = Display("display_image")

    # Create keyboard instance
    keyboard = Keyboard()
    keyboard.enable(timestep)

    # Create images directory
    image_dir = os.path.join(os.getcwd(), "images")
    os.makedirs(image_dir, exist_ok=True)

    # Check if CSV file exists
    csv_file = os.path.join(os.getcwd(), "image_data.csv")
    file_exists = os.path.isfile(csv_file)

    # Create CSV file if it doesn't exist, otherwise append to it
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Image Name", "Steering Angle"])

    # Image saving interval
    save_interval = 100  # Save an image every 100 steps
    step_count = 0

    while robot.step() != -1:
        # Get image from camera
        image = get_image(camera)

        # Process and display image 
        grey_image = greyscale_cv2(image)
        display_image(display_img, grey_image)

        # Automatically save images and log data at intervals
        if step_count % save_interval == 0:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            file_name = current_datetime + ".png"
            image_path = os.path.join(image_dir, file_name)
            # cv2.imwrite(image_path, image)
            # with open(csv_file, mode='a', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerow([file_name, steering_angle])

            print(f"Image {file_name} taken with steering angle {steering_angle}")

        step_count += 1

        # Read keyboard
        key = keyboard.getKey()
        if key == keyboard.UP:  # up
            set_speed(speed + 1.0)
            print("up")
        elif key == keyboard.DOWN:  # down
            set_speed(speed - 2.0)
            print("down")
        if key == keyboard.RIGHT:  # right
            change_steer_angle(+0.3)
            print("right")
        elif key == keyboard.LEFT:  # left
            change_steer_angle(-0.3)
            print("left")
        else:
            set_steering_angle(0)
            manual_steering = 0
        print(f'Angle {steering_angle}')
        # Update angle and speed
        driver.setSteeringAngle(steering_angle)
        driver.setCruisingSpeed(speed)

if __name__ == "__main__":
    main()
