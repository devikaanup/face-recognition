
# Face Recognition System
 
A real-time face recognition system that detects and identifies individuals through a live webcam feed. Built with Python, OpenCV, and the `face_recognition` library.
 
 
 
## -Features-
 
- Real-time face detection and recognition via webcam
- Matches detected faces against a preloaded database of known individuals
- Automatically annotates the live video stream with names and bounding boxes
- Marks unrecognized faces as **Unknown**
- Optimized frame processing for smooth real-time performance
---
 
## -Tech Stack-
 
| Tool | Purpose |
|---|---|
| Python | Core language |
| OpenCV | Webcam capture & video annotation |
| face_recognition | Face encoding & identity matching |
| NumPy | Frame processing & array operations |
 
---
 
## -Project Structure-
 
```
face-recognition/
│
├── face_recognition_system.py  # Main script
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
└── images/                     # Folder of known faces (not included)
    ├── john_doe.jpg
    ├── jane_smith.jpg
    └── ...
```

 ---

## -How It Works-
 
1. **Database loading** — On startup, all images in the `images/` folder are loaded and their facial features are encoded into numerical vectors
2. **Face detection** — Each webcam frame is scanned for faces using HOG-based detection
3. **Feature encoding** — Detected faces are converted into 128-dimensional encoding vectors
4. **Identity matching** — Encodings are compared against the known database using Euclidean distance; the closest match is selected
5. **Annotation** — Recognized faces get a green box with their name; unknown faces get a red box labeled "Unknown"
---
 
## -Use Cases-
 
- Attendance tracking systems
- Security monitoring
- Personalized access control
---
 
## -Notes-
 
- The `images/` folder is excluded from this repository. It can be added by the user for the known faces database.
