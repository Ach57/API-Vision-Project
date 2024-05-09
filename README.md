# API-Vision-Project
Overview
The API Vision Application reads a set of images and determines the number of people existing in each image. It then prints the results in the same Google Spreadsheet in a predefined format.

Description
This program utilizes the Google Cloud Vision API to analyze images and extract information about the number of people present. The results, including the number of people detected, accuracy, and confidence levels, are stored in a Google Spreadsheet.

Dependencies
gspread: Python API for Google Sheets
tkinter: GUI toolkit for Python
PIL: Python Imaging Library for image processing
google.cloud.vision: Google Cloud Vision API for image analysis
logging: Module for logging messages in the application

Usage

Run the application: API_Vision_Application.py

Format of Results
The results are printed in the following format in the Google Spreadsheet:
["Number of person,", "Accuracy", "Confidence", "Accuracy"]

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
