import os
import re
import PyPDF2
import openai

# Set up OpenAI API
openai.api_key = ""

resume_text = ''
# Read PDF file
with open('resume.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    page_count = len(reader.pages)
    for i in range(page_count):
        page = reader.pages[i]
        resume_text += page.extract_text()
    print(resume_text)

# Extract skills from resume using OpenAI API
def extract_skills(resume_text):
    model_engine = "text-davinci-002"
    prompt = (f"Extract skills from the following text: {resume_text}\n"
              "Skills:")
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    skills = [skill.strip() for skill in message.split("\n")]
    return skills[1:]  # remove "Skills:" from the beginning of the list

# Define function to search for common skills related to job title using OpenAI API
def search_common_skills(job_title):
    model_engine = "text-davinci-002"
    prompt = f"Search for common skills related to {job_title}"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    skills = message.split(", ")
    return skills

# Extract company name from resume using OpenAI NER model
def extract_company_name(resume_text):
    model_engine = "text-davinci-002"
    prompt = f"Extract company name from the following text: {resume_text}"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completions.choices[0].text.strip()
    company_name = message.split("\n")[0]
    return company_name

# Get user input for job title
job_title = input("What job are you applying for? ")

# Get company name from resume using OpenAI NER model
company_name = extract_company_name(resume_text)

# Generate cover letter using skills and job title
resume_skills = extract_skills(resume_text)

# Search for common skills related to job title using OpenAI API
common_skills = search_common_skills(job_title)

# Filter resume skills for only common skills related to job title
matched_skills = list(set(resume_skills).intersection(common_skills))


# Generate cover letter using matched skills and job title
if matched_skills:
    cover_letter = f"""Dear Hiring Manager,

    I am writing to express my interest in the {job_title} position at your company. With my experience in {matched_skills[2]}, I believe I would be a valuable addition to your team.

    In my previous role at {company_name}, I developed strong skills in {matched_skills[0]} and {matched_skills[1]}. I am confident that these skills, along with my passion for {job_title}, would make me a successful {job_title} at your company.

    Thank you for considering my application. I look forward to the opportunity to further discuss how I can contribute to your team.

    Sincerely,
    [Your Name]
    """
else:
    cover_letter = f"""Dear Hiring Manager,

    I am writing to express my interest in the {job_title} position at your company. Although I may not have experience in the specific skills required for this position, I am a quick learner and am confident that I can quickly develop the necessary skills to excel in this role.

    In my previous role at {company_name}, I developed strong skills in {resume_skills[0]} and {resume_skills[2]}. I am confident that these skills, along with my passion for {job_title}, would make me a valuable addition to your team.

    Sincerely,
    [Your Name]
    """

# Write cover letter to file
with open(f"{job_title}_cover_letter.txt", "w") as file:
    file.write(cover_letter)
