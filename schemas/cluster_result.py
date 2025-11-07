from typing import List
from pydantic import BaseModel, Field

class QuestionItem(BaseModel):
    """각 질문 항목"""
    qa_id: str = Field(..., description="질문-답변 쌍의 고유 ID")
    text: str = Field(..., description="질문 텍스트")

class GroupInfo(BaseModel):
    """유사 질문 그룹 스키마"""
    group_id: int = Field(..., description="그룹 고유 번호 (1부터 시작)")
    question_count: int = Field(..., description="그룹 내 질문 개수")
    question_ids: List[str] = Field(..., description="그룹 내 질문 QA ID 목록")
    questions: List[QuestionItem] = Field(..., description="그룹 내 실제 질문 리스트")
    representative_text: str = Field(..., description="그룹의 대표 요약 문장 또는 대표 질문 텍스트")

class ClusterResult(BaseModel):
    groups: List[GroupInfo]