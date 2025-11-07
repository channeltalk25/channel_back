import os

CLUSTERER_PROMPT: str = ""
RECOMMENDER_PROMPT: str = ""

def load_prompts():
    global CLUSTERER_PROMPT, RECOMMENDER_PROMPT

    # loader.py가 있는 폴더 기준 절대 경로
    base_path = os.path.dirname(__file__)

    with open(os.path.join(base_path, "clusterer.txt"), "r", encoding="utf-8") as f:
        CLUSTERER_PROMPT = f.read().strip()
    
    with open(os.path.join(base_path, "recommender.txt"), "r", encoding="utf-8") as f:
        RECOMMENDER_PROMPT = f.read().strip()