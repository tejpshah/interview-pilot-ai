import os
from dotenv import load_dotenv
from tqdm import tqdm
import anthropic
import PyPDF2

load_dotenv()
client = anthropic.Anthropic(
    api_key = os.environ.get("ANTHROPIC_API_KEY"),
)

def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def extract_text_from_pdf(pdf_path, output_folder):
    pdf_filename = os.path.basename(pdf_path)
    text_filename = os.path.splitext(pdf_filename)[0] + ".txt"
    text_folder = os.path.join(output_folder, "text-files")
    ensure_dir_exists(text_folder)
    text_file_path = os.path.join(text_folder, text_filename)

    # Check if the text file already exists, skip if it does
    if os.path.exists(text_file_path):
        print(f"Skipping {pdf_filename}, text file already exists.")
        return

    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        with open(text_file_path, "w", encoding="utf-8") as text_file:
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_file.write(text)

    print(f"Extracted text from {pdf_filename} to {text_filename}")

def extract_text_from_job_descriptions():
    folder_path = "job-descriptions"  
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            extract_text_from_pdf(pdf_path, folder_path)

def process_job_description(text_file_path, output_folder):
    system_prompt = "# Job Description Analysis\n\n## Instructions\n1. Read the provided job description carefully.\n2. Identify the key sections or components of the job description.\n3. For each section, extract the essential details and key points.\n4. Present the extracted information in a structured format using Markdown, with each section having a heading and the key points listed as bullet points.\n5. Be concise. Only important details.\n\n## Format\n```mkdown\n# Section 1 Title\n\n- Key point 1\n- Key point 2\n- Key point 3\n\n# Section 2 Title\n\n- Key point 1\n- Key point 2\n- Key point 3\n\n# Section N Title\n\n- Key point 1\n- Key point 2\n- Key point 3"

    with open(text_file_path, "r", encoding="utf-8") as file:
        job_description = file.read()

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": job_description
                }
            ]
        }
    ]
    )

    output_filename = os.path.basename(text_file_path)
    output_file_path = os.path.join(output_folder, output_filename)

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(message.content[0].text)

    print(f"Processed {text_file_path} and saved to {output_file_path}")

def process_job_descriptions(input_folder, output_folder):
    ensure_dir_exists(output_folder)

    text_file_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith(".txt")]

    for text_file_path in tqdm(text_file_paths, desc="Processing job descriptions"):
        process_job_description(text_file_path, output_folder)

if __name__ == "__main__":
    input_folder = "job-descriptions/text-files"
    output_folder = "job-descriptions/text-files-processed"

    print("\nExtracting text from job descriptions...")
    extract_text_from_job_descriptions()

    print("\nProcessing job descriptions...")
    process_job_descriptions(input_folder, output_folder)
