"""
This program reads Date Of Birth and Aadhar Number form multiple aadhar photos present in a
folder. Also This makes csv file and store extracted data in to that csv file.
"""


import pytesseract
import re
import pandas as pd
import os

# Path of tesseract.exe NOTE : Once check your tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# NOTE : Please use "\\" instead of "\"> That will excute program SMOTHLY

class AadharDetails:

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def __extracting_details(self, file_path):
        img_text = pytesseract.image_to_string(file_path)

        # Code for Date Of Birth
        birth_date = re.findall('\d\d[/|-]\d\d[/|-][0-9]{4}', img_text)
        if birth_date:
            birth_date = birth_date[0]

        else:
            birth_date = 'Not Found'

        # Code for Aadhar Number
        aadhar_num = re.findall('[0-9]{4}\s[0-9]{4}\s[0-9]{4}', img_text)
        if aadhar_num:
            aadhar_num = aadhar_num[0]
        else:
            aadhar_num = 'Not Found'

        return birth_date, aadhar_num

    def __processing_on_each(self):

        file_list = os.listdir(self.dir_path)
        result_list = []

        for file in file_list:
            file_data = [file]
            current_path = self.dir_path + '\\' + file

            temp = list(self.__extracting_details(current_path))
            file_data.extend(temp)
            result_list.append(file_data)

        return result_list

    def make_csv(self):
        lst = self.dir_path.split('\\')
        csv_file_name = lst[-1] + '.csv'

        data = self.__processing_on_each()

        df = pd.DataFrame(data, columns=['Image Name', 'Date of Birth', 'Aadhar Numbers'])
        #         print(df)

        df.to_csv(csv_file_name, index=False)


# Folder path which contains aadhar photos NOTE : Path must be separated by "\\" instead of '\'

folder_path = r"folder_path"
obj = AadharDetails(folder_path)
obj.make_csv()
