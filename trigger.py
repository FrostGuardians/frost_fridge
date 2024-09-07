import cv2
import os
import firebase_admin
from firebase_admin import credentials, storage
import time

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate("frost-guardians-83c73-firebase-adminsdk-qfl35-9400f3f179.json")  # Replace with your service account key path
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'fridge-captures'  # Replace with your Firebase Storage bucket name
    })

# Function to upload image to Firebase Storage
def upload_to_firebase(image_path):
    # Get the storage bucket
    bucket = storage.bucket()
    
    # Define the destination blob name (this will be the file path in Firebase)
    blob = bucket.blob("fridge_demo/" + os.path.basename(image_path))
    
    # Upload the file
    blob.upload_from_filename(image_path)
    
    # Make the file publicly accessible
    blob.make_public()
    
    print(f"Image uploaded to Firebase. Public URL: {blob.public_url}")
    return blob.public_url

# Directory where you want to save the images
save_dir = 'dataset'
print("Creating dataset directory if it doesn't exist...")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
print(f"Saving images to: {save_dir}")

# Initialize Firebase
initialize_firebase()

# Initialize webcam
print("Initializing webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

img_counter = 0  # Counter to number images saved

print("Press 'c' to capture an image. Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # Instead of displaying, just capture the image on key press
    key = input("Press 'c' to capture, 'q' to quit: ").strip().lower()

    if key == 'c':
        # Save the image when 'c' is pressed
        img_name = f"{save_dir}/{time.time()}.png"
        print(f"Saving image {img_name}...")
        cv2.imwrite(img_name, frame)
        img_counter += 1  # Increment the image counter
        print(f"Image {img_name} saved successfully.")
        
        # Upload the image to Firebase
        print("Uploading image to Firebase...")
        upload_to_firebase(img_name)
    
    elif key == 'q':
        # Quit the application when 'q' is pressed
        print("Quitting...")
        break

# Release the capture
print("Releasing the webcam...")
cap.release()
