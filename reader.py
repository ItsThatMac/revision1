import openai
import re

def extract_skills(resume):
    # Authenticate with OpenAI API
    openai.api_key = "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"

    # Use the OpenAI API to extract skills from the resume
    prompt = "Extract skills from the following resume:\n\n" + resume
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    skills = response.choices[0].text.strip()

    # Clean up the extracted skills and return as a list
    skills = re.sub(r'[^\w\s]', '', skills)  # remove punctuation
    skills = re.sub(r'\n', ' ', skills)  # replace newlines with spaces
    skills = re.sub(r'\s+', ' ', skills)  # replace multiple spaces with single space
    skills = [skill.strip() for skill in skills.split(',')]

    return skills

# Example usage
resume_text = "I have experience in Python, Java, and SQL."
skills = extract_skills(resume_text)
print(skills)  # Output: ['Python', 'Java', 'SQL']
