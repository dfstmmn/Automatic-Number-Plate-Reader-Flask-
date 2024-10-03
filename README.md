# Automatic-Number-Plate-Reader-Flask

This is a Flask-based web application for license plate recognition. It allows users to upload images of vehicles and automatically detects and extracts the license plate information.

## Features

- Image upload functionality
- License plate detection using OpenCV
- Optical Character Recognition (OCR) using EasyOCR
- Display of processed image with highlighted license plate
- Responsive web design

## Tech Stack

- Backend: Flask (Python)
- Image Processing: OpenCV, NumPy
- OCR: EasyOCR
- Frontend: HTML, CSS

## Local Setup

1. Clone the repository:
   ```
   git clone (https://github.com/dfstmmn/Automatic-Number-Plate-Reader-Flask-/)
   cd your-repo-name
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python script.py
   ```

5. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. On the homepage, click the "Choose File" button to select an image of a vehicle.
2. Click "Upload Image" to process the image.
3. The result page will display the original image, the processed image with the detected license plate highlighted, and the extracted license plate text.

## File Structure

```
plate-reader/
├── script.py
├── static/
│   ├── styles/
│   │   └── index.css
│   │   └── results.css
│   └── uploads/
├── templates/
│   ├── index.html
│   └── results.html
└── README.md
```
