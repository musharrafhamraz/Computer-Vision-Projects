from PIL import Image
import pytesseract

class OCRText:
    def __init__(self):
        pass

    def perform_ocr(self, image_path):
        # pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\USER\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
        """
        Perform OCR on the provided image file.

        Parameters:
            image_path (str): Path to the image file.

        Returns:
            str: Extracted text from the image.
        """
        try:
            # Open the image file
            img = Image.open(image_path)

            # set the tessrect path
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(img)
            
            return extracted_text
        except Exception as e:
            return f"Error: {str(e)}"
