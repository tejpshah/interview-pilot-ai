import os
import re
import argparse
from dotenv import load_dotenv
from tqdm import tqdm
import anthropic
import PyPDF2
import random

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def ensure_dir_exists(dir_path):
    """
    Create a directory if it doesn't exist.

    Args:
        dir_path (str): Path to the directory.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def extract_text_from_pdf(pdf_path, output_folder):
    """
    Extract text from a PDF file and save it as a text file.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to the output folder.
    """
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

def extract_text_from_job_descriptions(job_descriptions_folder):
    """
    Extract text from all PDF files in the job-descriptions folder.

    Args:
        job_descriptions_folder (str): Path to the job-descriptions folder.
    """
    for filename in os.listdir(job_descriptions_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(job_descriptions_folder, filename)
            extract_text_from_pdf(pdf_path, job_descriptions_folder)

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

def generate_personas():
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="Create distinct personality types for an automated phone screening recruiter with different interests, conversation styles, and approaches. For each personality type, provide a one-paragraph description in markdown format (e.g., # Emma, The Enthusiastic Networker, # Liam, the MethodicalAnalyst, etc.) covering their interests, whether they are introverted or extroverted, their conversation style, and what they are like overall.\n",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate 6 different personality types."
                    }
                ]
            }
        ]
    )

    # Create the "personas" folder if it doesn't exist
    personas_folder = "personas"
    ensure_dir_exists(personas_folder)

    # Save the generated personas to "base_personas.txt" in the "personas" folder
    base_personas_file = os.path.join(personas_folder, "base_personas.txt")
    with open(base_personas_file, "w", encoding="utf-8") as file:
        file.write(message.content[0].text)

    print(f"Generated personas and saved to {base_personas_file}")

def extract_personas_from_markdown(markdown_file, output_folder):
    # Create the output folder if it doesn't exist
    ensure_dir_exists(output_folder)

    # Read the markdown file
    with open(markdown_file, "r", encoding="utf-8") as file:
        content = file.read()

    # Split the content into sections based on the markdown header tags
    sections = re.split(r"(#.*)", content)

    # Process each section
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        persona_name = header[2:].strip().lower().replace(" ", "-").replace(",", "")
        persona_file = os.path.join(output_folder, f"{persona_name}.txt")

        # Write the persona content to a separate file
        with open(persona_file, "w", encoding="utf-8") as file:
            file.write(sections[i + 1].strip())

        print(f"Extracted {persona_name} and saved to {persona_file}")

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_job_folder(jobs_folder, job_name):
    job_folder = os.path.join(jobs_folder, job_name)
    ensure_dir_exists(job_folder)
    return job_folder

def create_finalized_personas(job_description, job_name, k=3, personas_folder="personas/individuals", jobs_folder="personas/jobs"):
    # create the personas folder
    ensure_dir_exists(personas_folder)
    # create the jobs folder
    ensure_dir_exists(jobs_folder)

    # Get a list of all persona files
    persona_files = [file for file in os.listdir(personas_folder) if file.endswith(".txt")]
    # Randomly select k personas
    selected_personas = random.sample(persona_files, k)

    job_folder = create_job_folder(jobs_folder, job_name)
    print(job_folder)

    # Mesh each selected persona with the job description
    for persona_file in selected_personas:
        persona_path = os.path.join(personas_folder, persona_file)
        if not os.path.exists(persona_path):
            persona_path = os.path.join(personas_folder, "individuals", persona_file)
        with open(persona_path, "r", encoding="utf-8") as file:
            persona_description = file.read()
        # Call the API to mesh the persona with the job description
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Create a persona that combines a user persona and a job description. The persona should be an interviewer who is knowledgeable about the job description and is preparing to interview a candidate for the position. Provide a two-paragraph description of the persona, incorporating the job description into their background and mindset as an interviewer.\n\nUser Persona: {persona_description}\n\nJob Description:\n{job_description}"
                        }
                    ]
                }
            ]
        )
        # Save the fused persona to a file in the job folder
        persona_name = persona_file[:-4]
        fused_persona_file = os.path.join(job_folder, f"{persona_name}-{job_name}.txt")
        with open(fused_persona_file, "w", encoding="utf-8") as file:
            file.write(message.content[0].text)
        print(f"Created fused persona: {fused_persona_file}")

if __name__ == "__main__":

    input_folder = "job-descriptions/text-files"
    output_folder = "job-descriptions/text-files-processed"

    print("\nExtracting text from job descriptions...")
    # extract_text_from_job_descriptions()

    print("\nProcessing job descriptions...")
    # process_job_descriptions(input_folder, output_folder)

    print("\nGenerating personas...")
    # generate_personas()

    markdown_file = "personas/base_personas.txt"
    output_folder = "personas/individuals"
    # extract_personas_from_markdown(markdown_file, output_folder)

    job_name = "meta-sweml"
    job_description = open("job-descriptions/text-files-processed/meta-sweml.txt", "r").read()
    create_finalized_personas(job_description, job_name)