from dataclasses import dataclass, field
from typing import Optional
import uuid
import json

@dataclass
class QuestionAnswer:
    """질문-답변 쌍"""
    qa_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    question_id: str = ""
    question_text: str = ""
    answer_id: Optional[str] = None
    answer_text: Optional[str] = None
    chat_id: Optional[str] = None
    created_at: Optional[int] = None

def extract_qa_pairs(chat_data: list[dict]) -> list[QuestionAnswer]:
    qa_pairs: list[QuestionAnswer] = []

    for chat in chat_data:
        chat_id = chat["chatId"]
        messages = chat["messages"]

        current_question_ids = []
        current_question_texts = []
        current_question_time = None

        current_answer_ids = []
        current_answer_texts = []
        current_answer_time = None

        def flush_question_answer():
            """현재 누적된 질문/답변을 QA 객체로 변환"""
            if current_question_ids:
                question_id = ",".join(current_question_ids)
                question_text = "\n".join(current_question_texts)
                created_at = current_question_time
                if current_answer_ids:
                    answer_id = ",".join(current_answer_ids)
                    answer_text = "\n".join(current_answer_texts)
                else:
                    answer_id = None
                    answer_text = None

                qa_pairs.append(
                    QuestionAnswer(
                        question_id=question_id,
                        question_text=question_text,
                        answer_id=answer_id,
                        answer_text=answer_text,
                        chat_id=chat_id,
                        created_at=created_at,
                    )
                )

        last_type = None

        for msg in messages:
            mtype = msg["type"]
            text = msg.get("text", "")
            mid = msg["id"]
            created_at = msg["createdAt"]

            # --- BOT (질문) ---
            if mtype == "bot":
                # 이전이 매니저였다면 새 QA 시작
                if last_type == "manager":
                    flush_question_answer()
                    current_question_ids.clear()
                    current_question_texts.clear()
                    current_answer_ids.clear()
                    current_answer_texts.clear()

                current_question_ids.append(mid)
                current_question_texts.append(text)
                if current_question_time is None:
                    current_question_time = created_at

            # --- MANAGER (답변) ---
            elif mtype == "manager":
                current_answer_ids.append(mid)
                current_answer_texts.append(text)
                if current_answer_time is None:
                    current_answer_time = created_at

            last_type = mtype

        # 마지막 남은 쌍 저장
        flush_question_answer()

    return qa_pairs