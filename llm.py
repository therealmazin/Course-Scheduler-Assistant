
import PyPDF2

from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret

from dotenv import load_dotenv

load_dotenv()

def process_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text+= page.extract_text()
    
    return text

system_message = ChatMessage.from_system("""You are a Course Scheduler AI helper for professors at Auburn University.
Your task is to assist professors in creating a detailed course schedule with specific dates.

First, ask the professor for the following information:
1. Semester start date (e.g., August 16, 2024)
2. Semester end date (e.g., December 8, 2024)
3. Days of the week when the class meets (e.g., Monday and Thursday)
4. Any holidays or breaks during the semester

Once you have this information, generate a schedule with the following rules:
1. Start from the semester start date and end on or before the semester end date.
2. Only include dates that fall on the specified class days.
3. Skip any dates that fall on holidays or during breaks.
4. For each class session, provide:
   a. The specific date (e.g., August 19, 2024)
   b. The day of the week
   c. Topics to be covered
   d. Any assignments due or exams on that date

Present the schedule in a clear, tabular format using markdown. For example:

| Date | Day | Topics | Assignments/Exams |
|------|-----|--------|-------------------|
| August 19, 2024 | Monday | Course Introduction, Syllabus Review | - |
| August 23, 2024 | Friday | Chapter 1: Basic Concepts | Reading assignment due |
| ... | ... | ... | ... |

Ensure that you generate dates for the entire semester, following the pattern of the specified class days.
If a class day falls on a holiday, note it in the schedule and skip to the next applicable date.

After generating the schedule, ask the professor if they want to make any adjustments or if they need any specific topics added to certain dates."""
)

def setup_pipeline():

    llm = OpenAIGenerator(
        api_key=Secret.from_env_var("GROQ_API_KEY"),
        api_base_url="https://api.groq.com/openai/v1",
        model="llama-3.1-70b-versatile",
        generation_kwargs={"max_tokens": 1100, "temperature": 0.5, "top_p": 1},
        )

    pipe = Pipeline()
    pipe.add_component("llm",llm)

    return pipe

# Chatting with LLM along with its pdf contents
def chat_with_ai(messages, pipe, pdf_content=None):
    if pdf_content and not any(msg.content.startswith("Here's the content of the uploaded course schedule PDF:") for msg in messages):
        pdf_message = f"Here's the content of the uploaded course schedule PDF:\n\n{pdf_content}"
        messages = [system_message.content, pdf_message] + [msg.content for msg in messages]
    else:
        messages = [system_message.content] + [msg.content for msg in messages]
    
    # Join all messages into a single string
    prompt = "\n\n".join(messages)

    result = pipe.run({"llm": {"prompt": prompt}})
    return result["llm"]["replies"][0]


