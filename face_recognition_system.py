"""
Face Recognition System
School Project 
Tools Used: Python, OpenCV, face_recognition, NumPy
"""

import cv2
import face_recognition
import numpy as np
import os

#Loading the known face database beforehand
def load_known_faces(images_dir="images"):
    """
    Load all images from the images directory and encode their faces.
    """
    known_encodings = []
    known_names = []

    if not os.path.isdir(images_dir):
        print(f"Warning: '{images_dir}' database not found. Starting with empty database.")
        return known_encodings, known_names

    print("Loading known faces from database")

    for filename in os.listdir(images_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        file_path = os.path.join(images_dir, filename)
        image = face_recognition.load_image_file(file_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            print(f" No face found in '{filename}', skipping.")
            continue

        # Use filename (without extension) as the person's name
        name = os.path.splitext(filename)[0].replace("_", " ").title()
        known_encodings.append(encodings[0])
        known_names.append(name)
        print(f"  Loaded: {name}")

    print(f"Database ready: {len(known_names)} known face(s) loaded.\n")
    return known_encodings, known_names


# Processing each frame for real-time recognition

def process_frame(frame, known_encodings, known_names):
    """
    Detect and identify all faces in a single frame.
    Returns the annotated frame with bounding boxes and name labels.
    """
    # Resize frame to 1/4 size for faster processing--  uses NumPy for conversion
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR (OpenCV) to RGB (face_recognition) using NumPy
    rgb_small_frame = small_frame[:, :, ::-1]  # NumPy reverse channel order BGR to RGB

    # Detect face locations and compute encodings in the small frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):

        # Compare detected face against the known database
        name = "Unknown"
        color = (0, 0, 255)  # Red for unknown

        if len(known_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            # Pick the known face with most similarity (least distance)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]
                color = (0, 255, 0)  # Green for recognized

        top, right, bottom, left = face_location
        top    *= 4
        right  *= 4
        bottom *= 4
        left   *= 4

        # Draw bounding box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Draw filled label background
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)

        # Annotate with name
        cv2.putText(
            frame, name,
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_DUPLEX,
            0.8, (255, 255, 255), 1
        )

    h, w = frame.shape[:2]
    info = f"Faces detected: {len(face_locations)}  |  Press Q to quit"
    cv2.putText(frame, info, (10, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

    return frame


# running the recognition loop

def run_recognition(known_encodings, known_names):
    """
    Open the webcam and run real-time face recognition on the live feed.
    Press Q to quit.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting real-time face recognition")
    print("Press Q to quit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read from webcam.")
            break

        # Process and annotate the frame
        annotated_frame = process_frame(frame, known_encodings, known_names)

        cv2.imshow("Face Recognition System", annotated_frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting")
            break

    cap.release()
    cv2.destroyAllWindows()


#MAIN

if __name__ == "__main__":
    
    # Load the known face database once at startup
    known_encodings, known_names = load_known_faces(images_dir="images")

    # Start real-time recognition
    run_recognition(known_encodings, known_names)
