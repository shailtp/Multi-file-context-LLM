import os
from groq import Groq
from loguru import logger
import time


def call_llm(system_msg: str, model_name: str, get_json: bool= True, seed: int = 100):

        # url = "https://api.groq.com/openai/v1"
        key = "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"

        client = Groq(
            api_key=key,
        )
        # client = Groq(api_key=key)
        logger.debug(f"Model being used: {model_name}")
        start = time.time()
        completion = client.chat.completions.create(
            extra_headers={},
            model=model_name,
            response_format={"type": "text" if not get_json else "json_object"},
            temperature=0,
            seed= seed,
            messages=(
                [
                    {
                        "role": "system",
                        "content": system_msg,
                    }
                ]
                if get_json
                else [
                        {
                            "role": "system",
                            "content": system_msg,
                        }
                ]
            ),
        )
        end = time.time()
        time_taken = end - start
        return completion.choices[0].message.content.replace("\n", ""), time_taken