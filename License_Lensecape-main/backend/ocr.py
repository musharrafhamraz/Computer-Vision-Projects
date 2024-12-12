import cv2
import datetime
import os
import easyocr

def initialize_easyocr():
    return easyocr.Reader(['en'])

def perform_ocr(reader, image_path):
    try:
        results = reader.readtext(image_path)

        recognized_text = ""
        for detection in results:
            text = detection[1]
            text = ''.join(char for char in text if char.isalnum())
            recognized_text += text

        return recognized_text
    except Exception as e:
        print("OCR operation failed with an error:", e)
        return ""

def save_cropped_image(plate_image, save_folder, timestamp):
    image_name = f"{save_folder}/plate_{timestamp}.jpg"
    cv2.imwrite(image_name, plate_image)
    return image_name



# import cv2
# import datetime
# import os
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from msrest.authentication import CognitiveServicesCredentials

# def initialize_computer_vision_client(subscription_key, endpoint):
#     return ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# def perform_ocr(computervision_client, image_path):
#     with open(image_path, 'rb') as image_stream:
#         try:
#             results = computervision_client.recognize_printed_text_in_stream(image_stream)

#             recognized_text = ""
#             for region in results.regions:
#                 for line in region.lines:
#                     for word in line.words:
#                         word_text = word.text
#                         word_text = ''.join(char for char in word_text if char.isalnum())
#                         recognized_text += word_text

#             return recognized_text
#         except Exception as e:
#             print("OCR operation failed with an error:", e)
#             return ""

# def save_cropped_image(plate_image, save_folder, timestamp):
#     image_name = f"{save_folder}/plate_{timestamp}.jpg"
#     cv2.imwrite(image_name, plate_image)
#     return image_name
