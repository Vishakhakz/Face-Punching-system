import cv2
import pickle
import numpy as np
import os

# Setup video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0

# Input user name
name = input("Enter Your Name: ")

# Check if the file 'names.pkl' exists, and if it's empty or not
names_file_path = 'data/names.pkl'
faces_data_file_path = 'data/faces_data.pkl'

# Create 'names.pkl' if it doesn't exist
if not os.path.exists(names_file_path):
    print(f"{names_file_path} not found, creating new file.")
    names = [name] * 100  # Assuming you want 100 samples for each user
    with open(names_file_path, 'wb') as f:
        pickle.dump(names, f)
else:
    # If the file exists, load it
    try:
        with open(names_file_path, 'rb') as f:
            names = pickle.load(f)
    except EOFError:
        # Handle the case when the file is empty
        print(f"{names_file_path} is empty, creating new file.")
        names = [name] * 100
        with open(names_file_path, 'wb') as f:
            pickle.dump(names, f)

# Face data collection loop
while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
    
    # Display frame
    cv2.imshow("Frame", frame)
    
    # Exit on 'q' or if 100 images are collected
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:
        break

# Save collected face data
video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Save names and faces data to pickle files
if not os.path.exists(faces_data_file_path):
    with open(faces_data_file_path, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    # If 'faces_data.pkl' exists, load it and append the new data
    try:
        with open(faces_data_file_path, 'rb') as f:
            existing_faces = pickle.load(f)
    except EOFError:
        # Handle the case when the faces_data file is empty
        print(f"{faces_data_file_path} is empty, creating new file.")
        existing_faces = faces_data

    # Append new face data
    existing_faces = np.append(existing_faces, faces_data, axis=0)

    with open(faces_data_file_path, 'wb') as f:
        pickle.dump(existing_faces, f)

# If 'names.pkl' exists, append the new name for each 100 face samples
with open(names_file_path, 'rb') as f:
    names = pickle.load(f)
names.extend([name] * 100)

# Save updated names
with open(names_file_path, 'wb') as f:
    pickle.dump(names, f)

print("Face data collection completed.")
