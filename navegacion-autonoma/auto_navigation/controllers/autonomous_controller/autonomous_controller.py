import os
os.environ["KERAS_BACKEND"] = "torch"
import cv2
import numpy as np
from vehicle import Car, Driver
from controller import Display
import keras
import torch
from torch.nn import Linear
from torchvision.models import resnet
from torchvision.models.resnet import ResNet
import torchvision.transforms.v2.functional as F

def load_resnet_50(num_classes) -> ResNet:
    model = resnet.resnet50()
    model.fc = Linear(model.fc.in_features, num_classes)
    return model

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
ped_detector = load_resnet_50(2)
ped_detector.load_state_dict(torch.load("pedestrian_detector.pth"))
ped_detector = ped_detector.to(device)
ped_detector.eval()

# Preprocess image for model prediction
def preprocess_image(image):
    # Resize the image to the input shape expected by the network (66x200)
    resized_image = cv2.resize(image, (200, 66))
    # Convert the image to YUV color space (as in the NVIDIA model)
    yuv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2YUV)
    return yuv_image

# Load the trained model
model_path = csv_file = os.path.join(os.getcwd(), "../data_gathering/autonomous_vehicle_model_augmented.keras")
print(model_path)
model = keras.models.load_model(model_path)

# Display image 
def display_image(display, image):
    # Image to display
    image_rgb = np.dstack((image, image, image))
    # Display image
    image_ref = display.imageNew(
        image_rgb.tobytes(),
        Display.RGB,
        width=image_rgb.shape[1],
        height=image_rgb.shape[0],
    )
    display.imagePaste(image_ref, 0, 0, False)

def main():
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # Create camera instance
    camera = robot.getDevice("camera")
    camera.enable(timestep)

    # Processing display
    display_img = Display("display_image")

    while robot.step() != -1:
        # Get image from camera
        raw_image = camera.getImage()
        image = np.frombuffer(raw_image, np.uint8).reshape(
            (camera.getHeight(), camera.getWidth(), 4)
        )
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        # Predict the steering angle
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
        steering_angle = float(model.predict(preprocessed_image, batch_size=1))

        # Display the processed image
        grey_image = cv2.cvtColor(preprocessed_image[0], cv2.COLOR_YUV2BGR)
        display_image(display_img, grey_image)

        # Pedestrian detection
        cruising_speed = 20
        img = np.transpose(image, (2, 0, 1))
        ped_input = torch.from_numpy(img).float()
        ped_input = ped_input / 255
        ped_input = F.resize(ped_input, [224, 224])
        ped_input = torch.unsqueeze(ped_input, dim=0)
        ped_input = ped_input.to(device)
        with torch.no_grad():
            prediction = ped_detector(ped_input)
            prediction = prediction.cpu()
            predicted_class = torch.max(prediction, 1).indices.item()
        print(predicted_class)
        if predicted_class == 0:
            cruising_speed = 0
            print('Pedestrian detected')

        # Update the steering angle and speed
        print(f"Steering angle: {steering_angle}")
        driver.setSteeringAngle(steering_angle)
        driver.setCruisingSpeed(cruising_speed)  # Set a constant speed for testing

if __name__ == "__main__":
    main()
