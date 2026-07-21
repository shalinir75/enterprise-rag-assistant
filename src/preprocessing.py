import json
import re
from pathlib import Path
input_file = Path("data/processed/extracted_text.json")
output_file = Path("data/processed/cleaned_text.json")


# Text Cleaning Function

def clean_text(text):
    """
    Cleans extracted text from PDFs.
    """

    if not text:
        return ""

    # Replace tabs, newlines and multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted invisible characters
    text = text.replace("\u00a0", " ")

    # Remove repeated punctuation
    text = re.sub(r"\.{2,}", ".", text)

    # Remove extra spaces before punctuation
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text



# Load Extracted JSON

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)


# Clean Every Document

for pdf_name, pdf_data in data.items():

    # Clean each page
    if "pages" in pdf_data:
        for page in pdf_data["pages"]:
            if "text" in page:
                page["text"] = clean_text(page["text"])

    # Clean complete document text
    if "full_text" in pdf_data:
        pdf_data["full_text"] = clean_text(pdf_data["full_text"])



# Create Output Folder 

output_file.parent.mkdir(parents=True, exist_ok=True)



# Save Cleaned JSON

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)



# Success Message

print("=" * 50)
print("✅ Text preprocessing completed successfully!")
print(f"📂 Input File : {input_file}")
print(f"📂 Output File: {output_file}")
print("=" * 50)