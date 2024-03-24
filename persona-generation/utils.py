import os
import re
import argparse
from dotenv import load_dotenv
from tqdm import tqdm
import anthropic
import PyPDF2
import random
import pandas as pd

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Utility Functions

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

def extract_text_from_df_resume(resume_path, output_folder):
    """
    Extract text from a PDF file and save it as a text file.

    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to the output folder.
    """
    pdf_filename = os.path.basename(resume_path)
    text_filename = os.path.splitext(pdf_filename)[0] + ".txt"
    text_folder = os.path.join(output_folder, "text-files")
    ensure_dir_exists(text_folder)
    text_file_path = os.path.join(text_folder, text_filename)

    # Check if the text file already exists, skip if it does
    if os.path.exists(text_file_path):
        print(f"Skipping {pdf_filename}, text file already exists.")
        return

    with open(resume_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                text_file.write(text)
    print(f"Extracted text from {pdf_filename} to {text_filename})")

# Process Job Descriptions

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

# Generate Personas

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

# Generate Interview Questions

def generate_interview_questions(job_description, k=2):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system=f"Based on the provided document, please create a list of {k} well-crafted interview questions that an interviewer could ask any candidate applying for this position. The questions should be as concise as possible, around 1 sentence, while being informative. Please use markdown formatting for the questions, following this format where each headline is the specific question:\n\n## Question 1\n\n## Question 2\n\n...\n\n## Question k",
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
    return message.content[0].text

def process_interview_questions(questions_text, category='base'):
    # Split the questions text into individual questions
    questions = re.split(r'(## Question \d+)', questions_text)[1:]

    # Create a list to store the processed questions
    processed_questions = []

    # Process each question
    for i in range(0, len(questions), 2):
        question_text = questions[i + 1].strip()
        processed_questions.append({
            'Question Text': question_text,
            'Category': category
        })

    # Create a DataFrame from the processed questions
    df = pd.DataFrame(processed_questions)

    return df

def save_interview_questions(df, filename, output_dir='interview-questions'):
    # Create the output directory if it doesn't exist
    ensure_dir_exists(output_dir)

    # Save the DataFrame to a CSV file in the output directory
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False)

    print(f"Interview questions saved to: {file_path}")

# Generate interview Questions Based on Resume
    
def generate_interview_questions_resume(resume, k=2):
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0,
        system=f"Based on the provided document, please create a list of {k} well-crafted interview questions that an interviewer could ask this question based on resume. The questions should be as concise as possible, around 1 sentence, while being informative. Please use markdown formatting for the questions, following this format where each headline is the specific question:\n\n## Question 1\n\n## Question 2\n\n...\n\n## Question k",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"This is the resume:\n{resume}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

# Generate Persona and Response Guidelines

def generate_persona_response_guidelines(persona_file_location, 
                                         job_summary_file_location, 
                                         resume_questions_file_location, 
                                         base_questions_file_location):
    
    persona_file = open(persona_file_location, "r").read()
    job_summary_file = open(job_summary_file_location, "r").read()
    resume_questions_file = open(resume_questions_file_location, "r").read()
    base_questions_file = open(base_questions_file_location, "r").read()

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="Based on the provided customer persona, job description, and interview questions, please complete the following tasks:\n\nSelect two questions from the base interview questions and two questions from the resume interview questions.\n\nFor each of the selected questions, provide an evaluation criteria in the form of one-line bullet points describing what constitutes a good response, an okay response, and a poor response.\n\nPlease structure your response as follows:\n\nCustomer Persona (Copy-Paste from Existing)\n\n[Copy and paste the persona description here]\n\nQuestion 1: [Insert the first selected question here]\n\nGood Response Criteria: [One-line bullet point describing a good response]\n\nOkay Response Criteria: [One-line bullet point describing an okay response]\n\nPoor Response Criteria: [One-line bullet point describing a poor response]\n\n...\n\nQuestion k: [Insert the kth selected question here]\n\nGood Response Criteria: [One-line bullet point describing a good response]\n\nOkay Response Criteria: [One-line bullet point describing an okay response]\n\nPoor Response Criteria: [One-line bullet point describing a poor response]",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are assuming the role of the persona. This is the persona:\n{persona_file}\nThis is the job summary:\n{job_summary_file}\nThis is the resume questions:\n{resume_questions_file}\nThis is the base questions:\n{base_questions_file}"
                    }
                ]
            }
        ]
    )

    return message.content[0].text

def main():
    # Step 1: Convert PDFs to text
    print("\nExtracting text from job descriptions...")
    job_descriptions_folder = "job-descriptions"
    if not os.path.exists(os.path.join(job_descriptions_folder, "text-files")):
        extract_text_from_job_descriptions(job_descriptions_folder)
    else:
        print("Skipping text extraction, text files already exist.")

    # Step 2: Process the text
    print("\nProcessing job descriptions...")
    input_folder = "job-descriptions/text-files"
    output_folder = "job-descriptions/text-files-processed"
    if not os.path.exists(output_folder):
        process_job_descriptions(input_folder, output_folder)
    else:
        print("Skipping text processing, processed files already exist.")

    # Step 3: Generate personas
    print("\nGenerating personas...")
    if not os.path.exists("personas/base_personas.txt"):
        generate_personas()
    else:
        print("Skipping persona generation, base personas file already exists.")
    markdown_file = "personas/base_personas.txt"
    output_folder = "personas/individuals"
    if not os.path.exists(output_folder):
        extract_personas_from_markdown(markdown_file, output_folder)
    else:
        print("Skipping persona extraction, individual persona files already exist.")

    # Step 4: Save each persona to appropriate folders
    # This step is already done in the extract_personas_from_markdown function

    # Step 5: Fuse personas with job descriptions
    print("\nFusing personas with job descriptions...")
    job_descriptions_folder = "job-descriptions/text-files-processed"
    for filename in os.listdir(job_descriptions_folder):
        if filename.endswith(".txt"):
            job_name = os.path.splitext(filename)[0]
            job_folder = os.path.join("personas/jobs", job_name)
            if not os.path.exists(job_folder):
                job_description_path = os.path.join(job_descriptions_folder, filename)
                with open(job_description_path, "r", encoding="utf-8") as file:
                    job_description = file.read()
                create_finalized_personas(job_description, job_name)
            else:
                print(f"Skipping persona fusion for {job_name}, fused personas already exist.")

    # Intermediate - Convert all resumes to text and save
    print("\nExtracting text from resumes...")
    resume_folder = "resumes"
    if not os.path.exists(os.path.join(resume_folder, "text-files")):
        for filename in os.listdir(resume_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(resume_folder, filename)
                extract_text_from_pdf(pdf_path, resume_folder)

    # Step 6: Generate questions based on resume and job description
    print("\nGenerating interview questions...")
    resume_folder = "resumes/text-files"
    for filename in os.listdir(resume_folder):
        if filename.endswith(".txt"):
            resume_path = os.path.join(resume_folder, filename)
            interview_questions_file = f"interview-questions/{os.path.splitext(filename)[0]}_interview_questions.csv"
            if not os.path.exists(interview_questions_file):
                with open(resume_path, "r", encoding="utf-8") as file:
                    resume = file.read()
                resume_questions = generate_interview_questions_resume(resume)
                resume_questions_df = process_interview_questions(resume_questions, category='resume')
                save_interview_questions(resume_questions_df, f"{os.path.splitext(filename)[0]}_interview_questions.csv")
            else:
                print(f"Skipping interview question generation for {filename}, questions already exist.")

    # Generating questions based on job description
    print("\nGenerating interview questions based on job descriptions...")
    for filename in os.listdir("job-descriptions/text-files-processed"):
        if filename.endswith(".txt"):
            job_description_path = os.path.join("job-descriptions/text-files-processed", filename)
            with open(job_description_path, "r", encoding="utf-8") as file:
                job_description = file.read()
            interview_questions_file = f"interview-questions/{os.path.splitext(filename)[0]}_interview_questions.csv"
            if not os.path.exists(interview_questions_file):
                job_questions = generate_interview_questions(job_description)
                job_questions_df = process_interview_questions(job_questions)
                save_interview_questions(job_questions_df, f"{os.path.splitext(filename)[0]}_interview_questions.csv")
            else:
                print(f"Skipping interview question generation for {filename}, questions already exist.")

    # Step 7: Save everything into a final file for each job's interview question
    print("\nGenerating response guidelines...")
    for job_name in os.listdir("personas/jobs"):
        job_folder = os.path.join("personas/jobs", job_name)
        for persona_file in os.listdir(job_folder):
            if persona_file.endswith(".txt"):
                persona_file_location = os.path.join(job_folder, persona_file)
                response_guidelines_file = os.path.join(job_folder, f"{os.path.splitext(persona_file)[0]}-response-guidelines.txt")
                if not os.path.exists(response_guidelines_file):
                    job_summary_file_location = os.path.join("job-descriptions/text-files-processed", f"{job_name}.txt")
                    resume_questions_file_location = "interview-questions/resume_interview_questions.csv"


                    list_of_files = os.listdir("interview-questions")
                    list_of_files.remove("resume_interview_questions.csv")

                    for file in list_of_files:
                        print(file)
                        base_questions_file_location = file 
                        response_guidelines = generate_persona_response_guidelines(persona_file_location,
                                                                                job_summary_file_location,
                                                                                resume_questions_file_location,
                                                                                'interview-questions/' + base_questions_file_location)
                        with open(response_guidelines_file, "w", encoding="utf-8") as file:
                            file.write(response_guidelines)
                        print(f"Response guidelines saved to {response_guidelines_file}")
                else:
                    print(f"Skipping response guidelines generation for {persona_file}, guidelines already exist.")


if __name__ == "__main__":
    main()

    