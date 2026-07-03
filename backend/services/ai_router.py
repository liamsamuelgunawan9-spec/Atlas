import asyncio

from services.groq_service import groq


class AIProvider:
    """
    Base provider class.
    Every provider should inherit from this.
    """

    name = "Unknown"

    async def chat(self, system_prompt, user_prompt, temperature=0.2):
        raise NotImplementedError


class GroqProvider(AIProvider):

    name = "Groq"

    async def chat(self, system_prompt, user_prompt, temperature=0.2):
        return await groq.chat(
            system_prompt,
            user_prompt,
            temperature
        )


# ===================================================
# Future Providers
# ===================================================

class GeminiProvider(AIProvider):

    name = "Gemini"

    async def chat(self, *args, **kwargs):
        raise Exception("Gemini not implemented yet.")


class CerebrasProvider(AIProvider):

    name = "Cerebras"

    async def chat(self, *args, **kwargs):
        raise Exception("Cerebras not implemented yet.")


class OpenRouterProvider(AIProvider):

    name = "OpenRouter"

    async def chat(self, *args, **kwargs):
        raise Exception("OpenRouter not implemented yet.")


# ===================================================
# Router
# ===================================================

class AIRouter:

    def __init__(self):

        self.providers = [

            GroqProvider(),

            GeminiProvider(),

            CerebrasProvider(),

            OpenRouterProvider(),

        ]

    async def chat(
        self,
        system_prompt,
        user_prompt,
        temperature=0.2
    ):

        last_error = None

        for provider in self.providers:

            print(f"Trying {provider.name}...")

            try:

                result = await provider.chat(
                    system_prompt,
                    user_prompt,
                    temperature
                )

                if result.get("success"):

                    result["provider"] = provider.name

                    print(f"Success using {provider.name}")

                    return result

            except Exception as e:

                print(f"{provider.name} failed.")

                last_error = str(e)

                continue

        return {

            "success": False,

            "provider": None,

            "model": None,

            "content": None,

            "error": last_error

        }


router = AIRouter()