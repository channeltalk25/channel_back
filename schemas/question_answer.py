import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

class QuestionAnswer(BaseModel):
    """질문-답변 쌍"""
    qa_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Question-Answer의 고유 ID")
    question_id: str = Field("", description="질문 ID (채널톡 메시지 ID 등)")
    question_text: str = Field("", description="질문 텍스트")
    answer_id: Optional[str] = Field(None, description="답변 ID (매니저 메시지 ID 등)")
    answer_text: Optional[str] = Field(None, description="답변 텍스트")
    chat_id: Optional[str] = Field(None, description="채팅방 ID")
    created_at: Optional[int] = Field(None, description="생성 시각 (epoch time)")

class QuestionAnswerList(BaseModel):
    """QuestionAnswer 객체 리스트 래퍼"""
    qa_list: List[QuestionAnswer] = Field(default_factory=list, description="QA 쌍 리스트")
