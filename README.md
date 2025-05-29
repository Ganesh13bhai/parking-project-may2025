# parking-project-may2025
# Parking Slot Identification and Tracking System

This project was developed for the **IIT Tirupati Navavishkar I-Hub Foundation Coding Challenge – 2**. It automatically detects parking slots from a video feed and classifies each slot as occupied or available.

## 🚗 Features

- Manual parking slot mapping using mouse input  
- Real-time video frame processing  
- Occupancy classification using pixel intensity  
- Visual slot overlay with cvzone  
- CSV export of occupancy data

## 🛠 Technologies Used

- Python  
- OpenCV  
- cvzone  
- NumPy  
- Pandas

## 📁 Project Structure
parking-project/
├── parking_tracker.py # Real-time video detection
├── export_status.py # Generate CSV with status
├── slot_labeler.py # Manual slot input tool
├── CarParkPos # Pickle file storing slot coordinates
├── carPark.mp4 # Sample parking lot video
├── results/
│ └── parking_status.csv # Output file
├── report.pdf # Final human-readable report
├── LICENSE # MIT License
└── README.md # This file

## 📤 Output Sample
Total Slots,Occupied Slots,Available Slots
50,14,36


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
