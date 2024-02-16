import base64
from collections import namedtuple
import dill
from functools import cached_property
import re
import requests
import sys
from urllib.parse import unquote


MAX_BYTES = 1e4
PATTERN = r"(\d+(\.\d+)?)\s+out of\s(\d+(\.\d+)?)"

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"  # Reset color


def get_score_with_color(score, max_score):
    pct_format = '{:.0%}'
    if score == max_score:
        color = GREEN
    elif score == 0:
        color = RED
    else:
        color = YELLOW
        pct_format = '{:.2%}'

    return color + pct_format.format(score / max_score) + ENDC


GradedProblem = namedtuple('GradedProblem', ('score', 'max_score',))


class ProfHarrisGrader:

    def __init__(self, homework: str, url: str):
        self.homework = homework
        self.url = url
        self.results = {}

    @cached_property
    def grade_url(self) -> str:
        return f'{self.url}/grade'
    
    @cached_property
    def max_score_url(self) -> str:
        return f'{self.url}/max_score'

    @cached_property
    def max_score(self) -> int:
        params = {'homework': self.homework}
        response = requests.get(self.max_score_url, params=params)

        if (max_score := response.text) is not None:
            max_score = int(response.text)

        if max_score is None:
            max_score = sum(problem.max_score for problem in self.results.values())

        return max_score  

    @staticmethod
    def serialize_answer(obj: object) -> bytes:
        serialized_in_bytes = dill.dumps(obj, recurse = True)
        return base64.b64encode(serialized_in_bytes).decode('utf-8')     

    def grade_answer(self, problem: str, answer: object) -> None:
        params = {
            'homework': self.homework,
            'problem': problem,
            'answer': self.serialize_answer(answer),
        }

        response = requests.get(self.grade_url, params=params)
        answer_in_byes = sys.getsizeof(params['answer'])

        if response.status_code == 502:
            print("API is down, please reach out to Prof. Harris")
        elif response.status_code == 413 or answer_in_byes > MAX_BYTES:
            print("Error: Trying to send object too large, check your answer!")
        elif response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            student_score, _, max_score, _ = [float(x or 0) for x in re.search(PATTERN, response.text).groups()]
            self.results[problem] = GradedProblem(student_score, max_score)
            print(response.text)

    def summary(self) -> None:
        student_score = sum(problem.score for problem in self.results.values())
        pct_formatted = get_score_with_color(student_score, self.max_score)

        print(f"Homework: {unquote(self.homework)}")
        print(f"Grade: {student_score} out of {self.max_score} ~ {pct_formatted}")
        print()
        print(f'{"Problem Name".center(50):<50} | {"Score".center(6):<6} | {"Max Score".center(9):<9} | {"Percent".center(7):<7} |')
        print("-" * 83)

        for problem_name, problem_score in self.results.items():
            score, max_score = problem_score
            centered_score = str(score).center(6)
            centered_max_score = str(max_score).center(9)
            centered_pct = get_score_with_color(score, max_score).center(7)
            print(f"{problem_name!r:<50} | {centered_score:<6} | {centered_max_score:<9} | {centered_pct:<7}")
