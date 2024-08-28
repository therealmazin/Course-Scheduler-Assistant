# Course Scheduler Assistant

## Overview

The Course Scheduler Assistant is an AI-powered tool designed to help professors at Auburn University create and optimize their course schedules. This Streamlit-based application uses advanced language models to analyze existing course schedules (via PDF upload) or assist in creating new schedules from scratch.

## Features

- **PDF Analysis**: Upload existing course schedule PDFs for AI analysis and optimization suggestions.
- **Interactive Chat Interface**: Engage with the AI assistant to create or refine your course schedule.
- **Intelligent Scheduling**: Receive suggestions for topic distribution, time allocation, and best practices in curriculum design.
- **Markdown Output**: Generate a final course schedule in a clean, markdown format.
- **Canvas Integration**: (Feature to be implemented) Ability to post the generated schedule directly to Canvas LMS.

## Requirements

- Python 3.7+
- Streamlit
- Haystack
- PyPDF2
- python-dotenv
- An API key from Groq (for accessing the LLM)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/course-scheduler-assistant.git
   cd course-scheduler-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. You can either:
   - Upload an existing course schedule PDF for analysis and optimization.
   - Start from scratch by describing your course and schedule requirements.

4. Interact with the AI assistant through the chat interface to refine and optimize your schedule.

5. Once satisfied, the assistant will generate a final course schedule in markdown format.

## Project Structure

- `app.py`: Main Streamlit application file.
- `llm.py`: Contains functions for setting up the LLM pipeline and processing chat interactions.
- `requirements.txt`: List of Python package dependencies.

## Contributing

Contributions to improve the Course Scheduler Assistant are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses the Groq API for language model interactions.
- Built with Streamlit and Haystack.
