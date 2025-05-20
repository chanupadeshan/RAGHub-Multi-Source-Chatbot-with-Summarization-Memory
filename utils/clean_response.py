import re

def clean_response(response):
    if 'answer' in response:
        answer = response['answer']
        # Remove everything between <think> and </think>, including the tags
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)
        response['answer'] = answer.strip()
    return response
