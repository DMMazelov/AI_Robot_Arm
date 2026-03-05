# AI_Robot_Arm

N11 ավագ դպրոց  

## Теам contributions
**Milena Petrosyan**
- Model training (CNN/ KNN)
- Data Preprocesing
- Arduino programming
- Engineered the robotic hand assembly
- System integration
- designed the presentation

**David Jaghatspanyan**
- Testing and evalution
- Managed English translation
- Prepared the project documentation
  
**Erik Mkrtchyan**
- Coordinated project organization
- handled non-technical tasks

An AI-powered robotic arm that recognizes hand gestures in real time and replicates the movement using servo motors. The system combines computer vision, machine learning, and hardware engineering to create a low-latency human-robot interaction interface

Problem Statement
Human-robot interaction often requires complex controllers or manual input.
This project explores a more intuitive solution — controlling a robotic hand using natural hand gestures detected through a camera.
The goal is to build a real-time, low-latency AI system that translates human gestures into robotic movement.

Features
Real-time hand detection using MediaPipe
Gesture classification (KNN / CNN)
Landmark-based feature extraction
Low-latency processing
Servo motor control
Arduino integration
Hardware-software communication via Serial

Camera 
   ↓
Hand Detection (MediaPipe)
   ↓
Feature Extraction (Landmarks)
   ↓
Gesture Classification (KNN / CNN)
   ↓
Serial Communication
   ↓
Arduino
   ↓
Servo Motors → Robotic Hand Movement


**Dataset**
- Custom collected dataset
- Multiple gesture classes
- Images captured under different lighting conditions
- Preprocessing:
- Landmark extraction
- Normalization
- Noise filtering
- Data cleaning to remove blurry and invalid samples

**Technologies Used**
- Python
- c++
- OpenCV
- MediaPipe
- Scikit-learn / TensorFlow
- NumPy
- PySerial
- Arduino IDE

**Hardware Components**
- Arduino board
- Servo motors
- 3D-printed / assembled robotic hand
- External power supply
- Jumper wires

**Model Performance**
- Accuracy: 97%
- Latency: 2 ms
- Works best in good lighting conditions
- Full hand visibility required

**Future Improvements**
- Larger and more diverse dataset
- Improved CNN architecture
- Reduced latency
- Mobile app integration
- Multi-gesture continuous tracking
- Enhanced mechanical stability
