import base64
import dill
import requests


def serialize_answer(obj: object) -> bytes:
    serialized_in_bytes = dill.dumps(obj, recurse = True)
    return base64.b64encode(serialized_in_bytes).decode('utf-8')


def create_grader(homework: str, url) -> None:
    def grade_answer(problem: int, answer: object) -> str:

        params = {
            'homework': homework,
            'problem': problem,
            'answer': serialize_answer(answer),
        }

        response = requests.get(url, params=params)

        if response.status_code == 413:
            print("Error: Trying to send object too large, check your answer!")
        elif response.status_code != 200:
            print(f"Error: {response.text}")

        print(response.text)

    return grade_answer