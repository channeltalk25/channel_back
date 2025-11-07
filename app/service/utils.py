from langchain_core.messages import HumanMessage, SystemMessage
from schemas.question_answer import QuestionAnswerList
from typing import Union

def build_clusterer_input(question_answer_list: QuestionAnswerList, prompt: str) -> list[Union[SystemMessage, HumanMessage]]:
    input : list[Union[SystemMessage, HumanMessage]] = [SystemMessage(prompt)]
    input.append(HumanMessage(content=question_answer_list.model_dump_json(indent=2)))
    return input

def build_recommender_input(question: str, prompt: str) -> list[Union[SystemMessage, HumanMessage]]:
    input : list[Union[SystemMessage, HumanMessage]] = [SystemMessage(prompt)]
    input.append(HumanMessage(content=question))
    return input