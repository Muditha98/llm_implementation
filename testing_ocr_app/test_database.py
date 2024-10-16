import sqlite3
import easyocr
import os

# Initialize the EasyOCR reader (use 'en' for English)
reader = easyocr.Reader(['en'])

# Connect to SQLite and create a cursor
connection = sqlite3.connect("cheques.db")
cursor = connection.cursor()

# Create the CHEQUE table
table_info = """
CREATE TABLE IF NOT EXISTS CHEQUE(
    BANK_NAME VARCHAR(100),
    AMOUNT VARCHAR(25),
    ACCOUNT_NUMBER VARCHAR(50),
    DATE VARCHAR(25)
)
"""
cursor.execute(table_info)

# Directory containing the cheque images
image_directory = "test_images"  # Replace with your image directory

# Loop through each image in the directory
for image_name in os.listdir(image_directory):
    if image_name.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_directory, image_name)
        
        # Perform OCR on the image
        results = reader.readtext(image_path)
        
        # Extract relevant fields (simple parsing)
        bank_name = ""
        amount = ""
        account_number = ""
        date = ""
        
        for res in results:
            text = res[1].lower()
            if "bank" in text:
                bank_name = text
            elif "amount" in text or "$" in text:
                amount = text
            elif "account" in text:
                account_number = text
            elif "date" in text or any(char.isdigit() for char in text):
                date = text

        # Insert the data into the database
        cursor.execute(
            "INSERT INTO CHEQUE (BANK_NAME, AMOUNT, ACCOUNT_NUMBER, DATE) VALUES (?, ?, ?, ?)",
            (bank_name, amount, account_number, date)
        )
        print(f"Inserted data for {image_name}")

# Commit changes to the database
connection.commit()

# Display all the records in the CHEQUE table
print("\nThe inserted records are:")
data = cursor.execute("SELECT * FROM CHEQUE")
for row in data:
    print(row)

# Close the connection
connection.close()
