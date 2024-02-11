import base64
import dill
import requests

from .session import Session
from .utils import make_primary_key


def serialize_answer(obj: object) -> bytes:
    serialized_in_bytes = dill.dumps(obj, recurse = True)
    return base64.b64encode(serialized_in_bytes).decode('utf-8')


def create_grader(homework: str, url) -> None:
    session = Session()
    session_id = session.session_id

    print(f"Homework: {homework!r} - Session: {session_id!r}")

    def grade_answer(problem: str, answer: object) -> str:

        params = {
            'primary_key': make_primary_key(session_id, homework, problem),
            'session': session_id,
            'homework': homework,
            'problem': problem,
            'answer': serialize_answer(answer),
        }

        response = requests.get(url, params=params)

        if response.status_code == 502:
            print("Error: Looks like the auto-grader is down, please reach out to Prof. Harris!")
        elif response.status_code == 413:
            print("Error: Trying to send object too large, check your answer!")
        elif response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print(response.text)

    return grade_answer