# BizCardX - Extracting -Business -Card -Data<br>
*BizCardX is a Streamlit application that facilitates the extraction of information from images. It utilizes the EasyOCR library to recognize text content in the uploaded images and then extracts relevant details such as names, designations, phone numbers, email addresses, websites, addresses, and pin codes*<br>

**Developer Guide**<br>
*1. Tools Install*<br>
-Python 3.6 or higher.<br>
-MySQL<br>

*2. Requirement Libraries to Install*<br>
pip install pandas easyocr numpy python os re MySQL-python streamlit<br>

*3. Import Libraries*<br>
-import streamlit as st<br>
-from streamlit_option_menu import option_menu<br>
-import easyocr<br>
-from PIL import Image<br>
-import pandas as pd<br>
-import numpy as np<br>
-import re<br>
-import io<br>
-import pymysql<br>

*4. E T L Process*<br>
a) Extract data<br>
Extract relevant information from business cards by using the easyOCR library<br>
b) Process and Transform the data<br>
After the extraction process, process the extracted data based on Name, Designation, Mobile Number, Email, Website, Area, City, State, and Pincode is converted into a data frame.<br>
c) Load data<br>
After the transformation process, the data is stored in the MySQL database<br>

**USER GUIDE**<br>
**Home**<br>
-**Navigation:** Click on the "Home" option in the navigation menu to go to the home page.<br>
-**Overview:** In the home page, you'll find an introduction to BizCardX along with an image illustrating its functionality.<br>
**Upload & Modify**<br>
-**Upload Image:** Select the "Upload & Modify" option from the navigation menu. Upload an image of a business card by clicking the "Upload the file" button. Supported image formats include PNG, JPEG, and JPG.<br>
-**Extract Data:** After uploading the image, BizCardX will extract the data from the business card using OCR. Extracted data will be displayed in a tabular format below the uploaded image.<br>
-**Save Data:** If the extracted data is correct, click the "Save" button to save the data to a MySQL database.<br>
-**Preview Data:** Choose the "Preview" option from the "Select the method" radio button to preview the data stored in the database.<br>
-**Modify Data:** Select the "Modify" option from the "Select the method" radio button to modify existing data in the database. You can edit the data for each field and click "Modify" to save the changes.<br>
**Delete**<br>
-**Delete Data:** To delete data from the database, select the "Delete" option from the navigation menu. Choose the name and designation of the data you want to delete, then click the "Delete" button.<br>

