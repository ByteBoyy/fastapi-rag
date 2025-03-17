from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

GPT_VERSION = 'gpt-4o-mini'
TEMPRATURE=0.5
MAX_TOKENS=3000


def get_gpt_response_query(
    query: str,
    prompt:str,
    model: str = GPT_VERSION,
    temprature: float = TEMPRATURE,
    max_tokens: int = MAX_TOKENS,
):
    messages = [{"role": "user", "content": query}, {"role":"system","content":prompt}]
    try:
        response= client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temprature,
                max_tokens=max_tokens,
            )
        output = response.choices[0].message.content.strip()
        return output
    except Exception as e:
        return str(e)