import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "dev")
LLM_MODE = os.getenv("LLM_MODE", "rule")

print(">>> Planner ENV =", ENV)
print(">>> Planner LLM_MODE =", LLM_MODE)
