import httpx
from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    MODELS,
    REQUEST_TIMEOUT,
)


class GroqService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ):
        """
        Tries every model until one succeeds.
        Returns:
        {
            "model": "...",
            "content": "...",
            "success": True
        }
        """

        last_error = None

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:

            for model in MODELS:

                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    "temperature": temperature,
                }

                try:
                    response = await client.post(
                        f"{GROQ_BASE_URL}/chat/completions",
                        headers=self.headers,
                        json=payload,
                    )

                    response.raise_for_status()

                    data = response.json()

                    content = data["choices"][0]["message"]["content"]

                    return {
                        "success": True,
                        "model": model,
                        "content": content,
                    }

                except Exception as e:
                    print(f"[Groq] {model} failed.")
                    print(e)

                    last_error = str(e)

                    continue

        return {
            "success": False,
            "model": None,
            "content": None,
            "error": last_error,
        }


groq = GroqService()