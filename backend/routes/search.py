from fastapi import APIRouter

from services.ai_router import router

router_api = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router_api.get("/")
async def search():

    result = await router.chat(

        system_prompt="You are a helpful AI.",

        user_prompt="Say hello in exactly one sentence."

    )

    return result