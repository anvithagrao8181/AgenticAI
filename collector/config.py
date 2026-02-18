# import os
# from dotenv import load_dotenv

# load_dotenv()

# PREPROCESSOR_URL = os.getenv("PREPROCESSOR_URL")
# STORAGE_PATH = os.getenv("STORAGE_PATH")
# ENV = os.getenv("ENV", "dev")

# JENKINS_URL = os.getenv("JENKINS_URL")
# JENKINS_USER = os.getenv("JENKINS_USER")
# JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")

# if not STORAGE_PATH:
#     raise RuntimeError("STORAGE_PATH is not set in .env")

# STORAGE_PATH = os.path.abspath(STORAGE_PATH)

# print(">>> FINAL STORAGE_PATH =", STORAGE_PATH)
# print(">>> PREPROCESSOR_URL =", PREPROCESSOR_URL)
# print(">>> JENKINS_URL =", JENKINS_URL)

import os
from dotenv import load_dotenv

load_dotenv()

STORAGE_PATH = os.getenv("STORAGE_PATH")
ENV = os.getenv("ENV", "dev")

if not STORAGE_PATH:
    raise RuntimeError("STORAGE_PATH is not set in .env")

STORAGE_PATH = os.path.abspath(STORAGE_PATH)

print(">>> FINAL STORAGE_PATH =", STORAGE_PATH)
