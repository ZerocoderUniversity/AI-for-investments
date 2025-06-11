import os
import logging
import openai
from config import OPENAI_KEY, BASE_URL


async def get_ai_prediction(prompt, model="gpt-3.5-turbo", max_tokens=500):
    try:
        client = openai.OpenAI(api_key=OPENAI_KEY, base_url=BASE_URL)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты опытный инвестиционный советник, объясняй простым языком."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logging.error(f"Ошибка запроса к openai {e}")
        return "Извините не удалось получить прогноз. Попробуйте позже."