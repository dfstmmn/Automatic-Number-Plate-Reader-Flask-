import os
from flask import Flask, request, render_template, redirect
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        result_image_path, recognized_text = process_image(filepath)
        
        if result_image_path is None:
            return render_template('results.html', result_image=None, text=recognized_text)
        
        return render_template('results.html', uploaded_image=filepath, result_image=result_image_path, text=recognized_text)

def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    
    # Apply edge detection
    edged = cv2.Canny(filtered, 30, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    location = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            location = approx
            break

    if location is None:
        return None, "No license plate detected."
    
    # Create mask
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Crop the license plate region
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]

    # Enhance the cropped image
    cropped_image = cv2.GaussianBlur(cropped_image, (3, 3), 0)
    cropped_image = cv2.threshold(cropped_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Perform OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)

    if result:
        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.putText(img, text=text, org=(location[0][0][0], location[1][0][1] + 60), 
                          fontFace=font, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        img = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)

        output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
        cv2.imwrite(output_image_path, img)
        return output_image_path, text
    else:
        return None, "No license plate text detected."

if __name__ == "__main__":
    app.run(debug=True)