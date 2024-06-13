from openai import OpenAI
import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
import pytesseract
import io

def extract_text_images(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

    return text, images

def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables

def ocr_images(images):
    ocr_texts = []
    for image in images:
        ocr_text = pytesseract.image_to_string(image)
        ocr_texts.append(ocr_text)
    return ocr_texts

def clean_table_data(table):
    cleaned_table = []
    for row in table:
        cleaned_row = [str(cell) if cell is not None else '' for cell in row]
        cleaned_table.append(cleaned_row)
    return cleaned_table

def prepare_data_for_summary(text, tables, ocr_texts):
    # Combine all extracted elements into a single string for summarization
    combined_data = text
    for table in tables:
        cleaned_table = clean_table_data(table)
        combined_data += "\n" + "\n".join(["\t".join(row) for row in cleaned_table])
    combined_data += "\n" + "\n".join(ocr_texts)
    return combined_data

def extract_pdf_contents(pdf_path):
    text, images = extract_text_images(pdf_path)
    tables = extract_tables(pdf_path)
    ocr_texts = ocr_images(images)
    combined_data = prepare_data_for_summary(text, tables, ocr_texts)
    return combined_data
  
def summary_prompt(text):
  return f"Summarize the following text in detail to prepare it for a worksheet and return only the summarized text:\n\n{text}"

def generate_summary(api_key, text):
    prompt = summary_prompt(text)
    
    client = OpenAI(api_key=api_key)
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

def extract_summarized_pdf(pdf_path, api_key):
  combined_data = extract_pdf_contents(pdf_path)
  summary = generate_summary(api_key, combined_data)
  return summary