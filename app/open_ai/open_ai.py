import openai
import re
from app.core.config import settings
from app.tasks.tasks import task_list
from app.tasks.model import Task


class AI:
    def __init__(self):
        self._key = settings.OPENAI_APIKEY

    def send_request(self, text: str):
        openai.api_key = self._key
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{text}",
            max_tokens=200,
            top_p=0.1
        )
        return response.get('choices')[0].get('text')

    def get_matching_task(self, question: str, task_list: list[Task]):
        ai_question = f"Here is a question: '{question}'. \n" \
                      f"Which task in the following list fits best with the " \
                      f"question?\n" \
                      f"Answer only with one of the numbers provided.\n"
        for index, item in enumerate(task_list):
            ai_question += f"{index + 1}: {item.description} \n"
        ai_question += f"0: None of the above"
        print(ai_question)
        response = self.send_request(ai_question)
        print(response)
        response_code = int(re.findall(r"([0-9]+)", response)[0]) - 1
        if response_code == - 1 or response_code >= len(task_list):
            return
        return task_list[response_code]


def ask_question(question:str, tasks):
    ai = AI()
    response = ai.get_matching_task(question, tasks)
    if not response:
        print("Regardless how hard I try, I cannot help you with that.")
    else:
        if response.sub_tasks:
            ask_question(question=question, tasks=response.sub_tasks)
        print(response.do_task())


if __name__ == "__main__":
    question = "Cancel my meeting at 2pm"
    ask_question(question, task_list)
