# InterviewPilot.AI

- https://devpost.com/software/interviewpilot-ai?ref_content=user-portfolio&ref_feature=in_progress

- Anthropic Build with Claude Winner: [https://x.com/alexalbert__/status/1783604747494388168 ](https://twitter.com/alexalbert__/status/1783604747494388168)

## Description
Interviewing is nerve-wracking, especially with the unpredictable back-and-forth you'll encounter. Our phone screen agent helps you prepare by creating an interactive, realistic practice experience tailored to the role you're pursuing. Provide your resume and the job details, and our AI will role-play as an interviewer - asking personalized questions based on your background, listening to your responses, and replying with intelligent follow-ups, just like a real interviewer would.

But it gets even better. The agent can take on multiple distinct interviewer personas, from a fast-paced Wall Street type to a creative director, allowing you to prep for different styles and curveballs you may face. Unlike scripted practice, this dynamic interaction forces you to think critically and articulate your thoughts clearly. You can practiceas much as needed, honing your skills in a low-pressure environment before the real deal. With this tool, you'll walk into interviews calm, prepared and ready to genuinely converse and impress your potential employer.

## Instructions

To practice your interview skills using our tool, you need to follow the following steps (obviously, you need to clone the repository first. It also might be beneficial to create a separate virtual environment to avoid conflicts with other projects):

1. Install all requirements:
```
pip install -r requirements.txt
```

2. Create a .env file within conversational-dialog. This file will hold your OpenAI API key and your Anthropic API key. For example, here is what your .env file should look like:
```
OPENAI_API_KEY=<your API Key>
ANTHROPIC_API_KEY=<your API Key>
```
3. Once you have the .env file set-up, you can run interviewer.py file like so:
```
python3 interviewer.py
```

After that you can start practicing!

## How we built it
We integrated OpenAI's Whisper for speech-to-text transcription and the Text-to-Speech model for voice synthesis with Anthropic's Claude3 LLM (Opus/Sonnet/Haiku). Python code orchestrates data processing pipelines:
- Extract text from job descriptions/resumes using PyPDF2.
- Use Claude to generate distinct interviewer persona descriptions.
- Fuse personas with job details using Claude's few-shot learning.
- Generate interview questions from fused personas/resumes with Claude.
- Define good/bad answer criteria for each question using Claude.

The modules enable voice-based conversational practice interviews, with Whisper transcribing user responses and Claude controlling the interviewer persona's voiced replies from OpenAI TTS based on the fused persona/job context. This provides realistic, dynamic interview prep across diverse roles.

## Authors
This was made by Jinal Shah, Tej Shah, Akash Shah, and Hirsh Ramani for HackRU 2024!
