from schemas.recommend import RecommendedAnswer
from app.service.utils import build_recommender_input
from core.llm import llm
from prompts import loader

async def get_recommended_answers(question : str) :
    input = build_recommender_input(question, loader.RECOMMENDER_PROMPT)

    recommender = llm.with_structured_output(RecommendedAnswer)

    output = await recommender.ainvoke(input)

    return output