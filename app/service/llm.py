from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class QuestionAnswer:
    """질문-답변 쌍"""
    question_id: str  # 질문 메시지 ID
    question_text: str  # 질문 내용
    answer_id: Optional[str] = None  # 답변 메시지 ID
    answer_text: Optional[str] = None  # 답변 내용
    chat_id: Optional[str] = None  # 채팅방 ID
    created_at: Optional[int] = None  # 생성 시간

class ChatDataProcessor:
    """채팅 데이터 전처리"""
    
    @staticmethod
    def extract_qa_pairs(chat_data: List[Dict]) -> List[QuestionAnswer]:
        """
        채팅 데이터에서 질문-답변 쌍 추출
        
        Args:
            chat_data: 원본 채팅 데이터 (제공된 JSON 형식)
            
        Returns:
            QuestionAnswer 객체 리스트
        """
        qa_pairs = []
        
        for chat in chat_data:
            chat_id = chat['chatId']
            messages = chat['messages']
            
            for i, msg in enumerate(messages):
                # bot 타입 메시지만 질문으로 간주
                if msg['type'] == 'bot':
                    question = QuestionAnswer(
                        question_id=msg['id'],
                        question_text=msg['text'],
                        chat_id=chat_id,
                        created_at=msg['createdAt']
                    )
                    
                    # 다음 메시지가 manager 답변인지 확인
                    if i + 1 < len(messages):
                        next_msg = messages[i + 1]
                        if next_msg['type'] == 'manager':
                            question.answer_id = next_msg['id']
                            question.answer_text = next_msg['text']
                    
                    qa_pairs.append(question)
        
        return qa_pairs
    
    @staticmethod
    def filter_meaningful_questions(qa_pairs: List[QuestionAnswer]) -> List[QuestionAnswer]:
        """
        의미있는 질문만 필터링 (인사말, 테스트 메시지 제외)
        """
        # 제외할 패턴들
        exclude_patterns = [
            '방문해주셔서 감사합니다',
            '연락처를 남겨주세요'
        ]
        
        filtered = []
        for qa in qa_pairs:
            # 너무 짧거나 제외 패턴에 해당하는 질문 제외
            if len(qa.question_text) < 5:
                continue
            
            is_excluded = any(pattern in qa.question_text for pattern in exclude_patterns)
            if not is_excluded:
                filtered.append(qa)
        
        return filtered


class QuestionClusteringSystem:
    """질문 클러스터링 시스템"""
    
    def __init__(self, n_groups=5, min_questions_per_group=2):
        """
        Args:
            n_groups: 만들 그룹의 개수
            min_questions_per_group: 그룹당 최소 질문 수 (이보다 적으면 자동 조정)
        """
        self.n_groups = n_groups
        self.min_questions_per_group = min_questions_per_group
        self.model = None
    
    def cluster_questions(self, qa_pairs: List[QuestionAnswer]) -> Dict[str, Any]:
        """
        질문들을 클러스터링
        
        Args:
            qa_pairs: QuestionAnswer 객체 리스트
            
        Returns:
            클러스터링 결과 (그룹별 질문 및 답변 정보)
        """
        if len(qa_pairs) == 0:
            return {
                'groups': [],
                'total_questions': 0,
                'total_groups': 0,
                'message': '클러스터링할 질문이 없습니다.'
            }
        
        # 질문 수에 따라 그룹 수 자동 조정
        max_groups = max(1, len(qa_pairs) // self.min_questions_per_group)
        actual_groups = min(self.n_groups, max_groups, len(qa_pairs))
        
        # 1. 텍스트만 추출
        texts = [qa.question_text for qa in qa_pairs]
        
        # 2. Sentence Embedding으로 벡터화
        vectors = self._vectorize_embedding(texts)
        
        # 3. K-Means 클러스터링
        if actual_groups == 1:
            # 질문이 너무 적으면 모두 하나의 그룹으로
            group_labels = np.zeros(len(qa_pairs), dtype=int)
        else:
            kmeans = KMeans(n_clusters=actual_groups, random_state=42, n_init=10)
            group_labels = kmeans.fit_predict(vectors)
        
        # 4. 그룹별로 질문-답변 쌍 정리
        groups_dict = {}
        for i, label in enumerate(group_labels):
            label = int(label)
            if label not in groups_dict:
                groups_dict[label] = []
            groups_dict[label].append(qa_pairs[i])
        
        # 5. 결과 포맷팅
        groups_list = []
        for group_id, group_qa_pairs in groups_dict.items():
            # 답변이 있는 질문들만 추출
            answered_questions = [qa for qa in group_qa_pairs if qa.answer_text]
            
            group_data = {
                'group_id': group_id,
                'question_count': len(group_qa_pairs),
                'answered_count': len(answered_questions),
                'question_ids': [qa.question_id for qa in group_qa_pairs],
                'questions': [
                    {
                        'id': qa.question_id,
                        'text': qa.question_text,
                        'chat_id': qa.chat_id,
                        'created_at': qa.created_at,
                        'has_answer': qa.answer_text is not None
                    }
                    for qa in group_qa_pairs
                ],
                'answers': [
                    {
                        'id': qa.answer_id,
                        'question_id': qa.question_id,
                        'text': qa.answer_text,
                        'chat_id': qa.chat_id
                    }
                    for qa in answered_questions
                ],
                'representative_text': group_qa_pairs[0].question_text
            }
            groups_list.append(group_data)
        
        # 질문 개수 많은 순으로 정렬
        groups_list.sort(key=lambda x: x['question_count'], reverse=True)
        
        return {
            'groups': groups_list,
            'total_questions': len(qa_pairs),
            'total_groups': actual_groups,
            'timestamp': datetime.now().isoformat()
        }
    
    def _vectorize_embedding(self, texts: List[str]) -> np.ndarray:
        """Sentence-BERT로 벡터화"""
        if self.model is None:
            print("🔄 모델 로딩 중... (처음 한 번만 실행됩니다)")
            self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        return self.model.encode(texts)


# ===== 메인 실행 함수 =====

def process_chat_data(chat_json: str) -> Dict[str, Any]:
    """
    채팅 데이터를 받아서 클러스터링 결과 반환
    
    Args:
        chat_json: 채팅 데이터 JSON 문자열
        
    Returns:
        클러스터링 결과
    """
    # 1. JSON 파싱
    chat_data = json.loads(chat_json)
    
    # 2. 질문-답변 쌍 추출
    processor = ChatDataProcessor()
    qa_pairs = processor.extract_qa_pairs(chat_data)
    
    print(f"📊 총 {len(qa_pairs)}개의 bot 메시지 추출")
    
    # 3. 의미있는 질문만 필터링
    meaningful_qa_pairs = processor.filter_meaningful_questions(qa_pairs)
    
    print(f"✅ {len(meaningful_qa_pairs)}개의 의미있는 질문 필터링 완료")
    
    if len(meaningful_qa_pairs) == 0:
        print("⚠️ 클러스터링할 의미있는 질문이 없습니다.")
        return {
            'groups': [],
            'total_questions': 0,
            'total_groups': 0,
            'message': '의미있는 질문이 없습니다.'
        }
    
    # 4. 클러스터링
    clustering_system = QuestionClusteringSystem(n_groups=3)
    result = clustering_system.cluster_questions(meaningful_qa_pairs)
    
    return result


# ===== 실행 예제 =====

if __name__ == "__main__":
    # 제공된 샘플 데이터
    sample_json = '''[
    {
        "chatId": "69099f88bcc45fb43435",
        "messages": [
            {
                "id": "69099f88bebc8dbb2ec0",
                "type": "bot",
                "text": "방문해주셔서 감사합니다 :) 어떻게 도와드릴까요?",
                "createdAt": 1762238344781
            },
            {
                "id": "69099f8f0e6cdde77c7e",
                "type": "user",
                "text": "ㅎㅇ",
                "createdAt": 1762238351059
            },
            {
                "id": "69099f902702e626483a",
                "type": "bot",
                "text": "연락처를 남겨주세요. 오프라인 상태가 되면 이메일로 답변 알림을 보내드려요.\\n\\n(수집된 개인정보는 상담 답변 알림 목적으로만 이용되고, 삭제 요청을 주시기 전까지 보유됩니다. 제출하지 않으시면 상담 답변 알림을 받을 수 없어요.)",
                "createdAt": 1762238352159
            },
            {
                "id": "690dfa5106d4395680d7",
                "type": "bot",
                "text": "올해 블랙프라이데이는 언제 시작인가여",
                "createdAt": 1762523729027
            },
            {
                "id": "690dfacb7d2ae3cb2a25",
                "type": "manager",
                "text": "i dont know",
                "createdAt": 1762523851512
            }
        ]
    },
    {
        "chatId": "690a2ac7653b01179458",
        "messages": [
            {
                "id": "690a2ac766f343edc900",
                "type": "bot",
                "text": "방문해주셔서 감사합니다 :) 어떻게 도와드릴까요?",
                "createdAt": 1762273991421
            },
            {
                "id": "690a2ada9ab1342de3a3",
                "type": "user",
                "text": "ㅎㅇ",
                "createdAt": 1762274010633
            },
            {
                "id": "690a2adbb5a797811e64",
                "type": "bot",
                "text": "연락처를 남겨주세요. 오프라인 상태가 되면 이메일로 답변 알림을 보내드려요.\\n\\n(수집된 개인정보는 상담 답변 알림 목적으로만 이용되고, 삭제 요청을 주시기 전까지 보유됩니다. 제출하지 않으시면 상담 답변 알림을 받을 수 없어요.)",
                "createdAt": 1762274011744
            },
            {
                "id": "690dde3f523b3e6474bd",
                "type": "manager",
                "text": "하이요 ㅋㅋ",
                "createdAt": 1762516543336
            },
            {
                "id": "690df519b03a2bf44ced",
                "type": "bot",
                "text": "히히히히히히힣히히히히히히히히히히히히히히히ㅣ",
                "createdAt": 1762522393721
            },
            {
                "id": "690df5336ac0ec78675e",
                "type": "bot",
                "text": "이다혜 최건우 김준호 홧팅",
                "createdAt": 1762522419437
            },
            {
                "id": "690df53f1de6feb9a130",
                "type": "bot",
                "text": "이다혜 최건우 김준호 홧팅",
                "createdAt": 1762522431122
            }
        ]
    },
    {
        "chatId": "690a37d9b0954ff47241",
        "messages": [
            {
                "id": "690a37d9b3274b2ff2d5",
                "type": "bot",
                "text": "방문해주셔서 감사합니다 :) 어떻게 도와드릴까요?",
                "createdAt": 1762277337733
            },
            {
                "id": "690a37e4be981bb65b60",
                "type": "user",
                "text": "hello",
                "createdAt": 1762277348780
            },
            {
                "id": "690a37e5d7ae98d4c090",
                "type": "bot",
                "text": "연락처를 남겨주세요. 오프라인 상태가 되면 이메일로 답변 알림을 보내드려요.\\n\\n(수집된 개인정보는 상담 답변 알림 목적으로만 이용되고, 삭제 요청을 주시기 전까지 보유됩니다. 제출하지 않으시면 상담 답변 알림을 받을 수 없어요.)",
                "createdAt": 1762277349883
            },
            {
                "id": "690a3c1b847a794fe2f3",
                "type": "bot",
                "text": "hello hello hello",
                "createdAt": 1762278427542
            },
            {
                "id": "690a41c62acb231eaa43",
                "type": "bot",
                "text": "send doge to the moon",
                "createdAt": 1762279878175
            }
        ]
    }
]'''
    
    print("=" * 80)
    print("🚀 채팅 데이터 클러스터링 시작")
    print("=" * 80)
    
    # 클러스터링 실행
    result = process_chat_data(sample_json)
    
    # 결과 출력
    print(f"\n📊 클러스터링 결과")
    print(f"총 질문: {result['total_questions']}개")
    print(f"총 그룹: {result['total_groups']}개\n")
    
    for i, group in enumerate(result['groups'], 1):
        print(f"🔥 그룹 #{i} (ID: {group['group_id']})")
        print(f"   질문 개수: {group['question_count']}개")
        print(f"   답변 있는 질문: {group['answered_count']}개")
        print(f"   대표 질문: {group['representative_text']}")
        print(f"   질문 IDs: {group['question_ids'][:3]}{'...' if len(group['question_ids']) > 3 else ''}")
        
        print(f"\n   📝 질문 목록:")
        for q in group['questions']:
            answer_status = "✅ 답변있음" if q['has_answer'] else "❌ 답변없음"
            print(f"      - [ID: {q['id']}] {q['text'][:50]}... {answer_status}")
        
        print(f"\n   💬 답변 목록:")
        if group['answers']:
            for ans in group['answers']:
                print(f"      - [ID: {ans['id']}] {ans['text'][:50]}...")
        else:
            print(f"      - 답변 없음")
        
        print()
    
    # JSON 출력
    print("\n" + "=" * 80)
    print("📤 API 응답 형태 (JSON)")
    print("=" * 80)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Flask API 예제
    print("\n" + "=" * 80)
    print("🔧 Flask API 통합 예제")
    print("=" * 80)
    
    flask_example = '''
from flask import Flask, request, jsonify
from your_module import process_chat_data

app = Flask(__name__)

@app.route('/api/cluster-questions', methods=['POST'])
def cluster_questions():
    """채팅 데이터를 받아서 질문 클러스터링"""
    try:
        # 1. 요청에서 채팅 데이터 받기
        chat_data = request.json  # 배열 형태의 채팅 데이터
        
        # 2. 클러스터링 실행
        import json
        chat_json = json.dumps(chat_data)
        result = process_chat_data(chat_json)
        
        # 3. 결과 반환
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-recommended-answer', methods=['POST'])
def generate_recommended_answer():
    """특정 그룹의 이전 답변들을 기반으로 LLM 답변 생성"""
    try:
        data = request.json
        group_id = data['group_id']
        previous_answers = data['previous_answers']  # 그룹의 answers 배열
        
        # LLM에게 전달할 프롬프트
        answer_texts = [ans['text'] for ans in previous_answers]
        prompt = f"""
다음은 상담원들이 이전에 작성한 답변들입니다:
{chr(10).join(f'- {text}' for text in answer_texts)}

위 답변들을 참고하여, 동일한 유형의 질문에 대한 
친절하고 명확한 추천 답변을 작성해주세요.
"""
        
        # LLM API 호출 (예: OpenAI)
        # llm_response = call_llm_api(prompt)
        
        return jsonify({
            'success': True,
            'recommended_answer': "LLM이 생성한 답변",
            'based_on_answers': len(previous_answers)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
'''
    print(flask_example)