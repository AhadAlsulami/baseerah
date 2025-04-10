# بصيره 👁️

Welcome to the AI-Powered Sports Event Management System. This system is designed to enhance the experience of both event organizers and attendees by using cutting-edge technologies like face recognition, crowd detection, and garbage detection (coming soon). This solution aims to address common challenges in sports events, particularly with large crowds, ensuring smooth and safe entry, crowd management, and cleanliness.

## Setup Instructions
To run the application, simply execute the following command:

```bash
python Main.py
```
Once the application is running, it will load the system with all available features. Below is a breakdown of the system's components.

## Folder Structure
```bash
├── Main.py
├── pages/
│   ├── Admin.py
│   └── User.py
├── data/
│   └── visitor_data.csv
├── videos/
│   ├── crowd_video1.mp4
│   └── crowd_video2.mp4
```

### pages folder
The pages folder contains two main Python scripts:
- Admin.py: This script provides all the features for event organizers, including face recognition, crowd detection, and garbage detection (coming soon).
- User.py: This script is for visitors who wish to register and attend sporting events. They can provide their details, and the system will facilitate their entry into the event.

### data folder
The data folder stores:
- Pictures: It saves images of the visitors' faces for the face recognition feature.
- CSV File: It serves as a temporary database for storing the visitor data, including personal details, registration information, and more.

### videos folder
- The videos folder contains two sample videos used for simulating live streams during crowd detection. These videos will help mimic the behavior of a real event and test the crowd detection algorithm.

## Features
### Admin Features
- Face Recognition: Identifies visitors upon entry, ensuring a fast and secure check-in process.
- Crowd Detection: Monitors different areas of the venue for overcrowding and sends alerts to the organizers to take action.
- Garbage Detection (Coming Soon): Detects improper waste disposal and notifies the person involved to maintain cleanliness during the event.

### User Features
- Registration: Visitors can register to attend sporting events, providing necessary details for check-in.

## Credits
This project was created by Ahad Alsulami (me) and Waad Alsulami as part of the AI League competition organized by SCAI.
