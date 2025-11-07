from pydantic import BaseModel

class RecommendedAnswer(BaseModel):
    """답변 생성 결과"""
    ans1: str  # 첫 번째 더미 답변
    ans2: str  # 두 번째 더미 답변
    ans3: str  # 세 번째 더미 답변
    recommended_ans: str  # 세 답변을 참고하여 생성된 가장 최적의 답변