import anthropic
import os
import json
from dotenv import load_dotenv



load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def summarize_interview(transcript, criteria):

    conversation = ""

    for convo in transcript:
        if convo['role'] == 'user':
            conversation += 'Interviewee: '
        else:
            conversation += 'Interviewer: '
            
        conversation += convo['content'] + '\n'
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Given this transcript, {conversation}, please generate a manuscript, focusing on key points of the interview, including the answers to the questions provided by the interviewer.\n After generating a manuscript, I need you to rate each answer by the interviewee in the transcript {conversation} on a basis of Okay, Good, Poor using this criteria: {criteria}"
                    }
                ]
            }
        ]
    )

    return message.content[0].text

if __name__ == "__main__":
    with open("history.json", "r") as f:
        convo = json.load(f)
    
    with open("meta-sweml-response-guidelines.txt", "r") as f:
        criteria = f.read()

    response = summarize_interview(convo, criteria)
    with open("response.txt", "w") as f:
        f.write(response)



