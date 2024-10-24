import cv2
import face_recognition
import numpy as np
import os

# Step 1: Load known faces
def load_known_faces(known_faces_dir):
    known_faces = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)[0]  # Get the face encoding
            known_faces.append(encoding)
            known_names.append(os.path.splitext(filename)[0])  # Use filename as the name

    return known_faces, known_names

# Step 2: Detect and recognize faces in an image or video
def recognize_faces(known_faces, known_names):
    # Initialize webcam or video file
    video_capture = cv2.VideoCapture(0)  # Use 0 for webcam or replace with video file path

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]  # Convert from BGR to RGB

        # Step 3: Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Step 4: Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            # Use the first match found
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    known_faces_dir = "known_faces"  # Directory with known face images
    known_faces, known_names = load_known_faces(known_faces_dir)
    recognize_faces(known_faces, known_names)
