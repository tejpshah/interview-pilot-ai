# InterviewPilot.AI

## Description
Interviewing is nerve-wracking, especially with the unpredictable back-and-forth you'll encounter. Our phone screen agent helps you prepare by creating an interactive, realistic practice experience tailored to the role you're pursuing. Provide your resume and the job details, and our AI will role-play as an interviewer - asking personalized questions based on your background, listening to your responses, and replying with intelligent follow-ups, just like a real interviewer would.

But it gets even better. The agent can take on multiple distinct interviewer personas, from a fast-paced Wall Street type to a creative director, allowing you to prep for different styles and curveballs you may face. Unlike scripted practice, this dynamic interaction forces you to think critically and articulate your thoughts clearly. You can practiceas much as needed, honing your skills in a low-pressure environment before the real deal. With this tool, you'll walk into interviews calm, prepared and ready to genuinely converse and impress your potential employer.

## How we built it
We integrated OpenAI's Whisper for speech-to-text transcription and the Text-to-Speech model for voice synthesis with Anthropic's Claude3 LLM (Opus/Sonnet/Haioku). Python code orchestrates data processing pipelines:
- Extract text from job descriptions/resumes using PyPDF2.
- Use Claude to generate distinct interviewer persona descriptions.
- Fuse personas with job details using Claude's few-shot learning.
- Generate interview questions from fused personas/resumes with Claude.
- Define good/bad answer criteria for each question using Claude.

The modules enable voice-based conversational practice interviews, with Whisper transcribing user responses and Claude controlling the interviewer persona's voiced replies from OpenAI TTS based on the fused persona/job context. This provides realistic, dynamic interview prep across diverse roles.
