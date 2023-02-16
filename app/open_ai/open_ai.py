import openai
from openai.embeddings_utils import cosine_similarity
from typing import Union
from app.core.config import settings
from app.tasks.model import Task


class AI:
    def __init__(self):
        self._key = settings.OPENAI_APIKEY
        openai.api_key = self._key

    @staticmethod
    def send_request(text: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{text}",
            max_tokens=200,
            top_p=0.1
        )
        return response.get('choices')[0].get('text')

    @staticmethod
    def create_embeddings(text: Union[str, list[str]],
                          model="text-embedding-ada-002"):
        response = openai.Embedding.create(input=text, model=model)
        if type(text) == str:
            return response['data'][0]['embedding']
        return (response['data'][_]['embedding'] for _ in range(len(text)))

    @staticmethod
    def export_embeddings(task_descriptions: list[str],
                          embeddings: list[list[str]]):
        with open("app/tasks/embeddings/embeddings.txt", "w") as file:
            for index, task in enumerate(task_descriptions):
                file.write(f"{task};{embeddings[index]}\n")

    def match_request_with_function(self, user_request: str,
                                    task_list: list[Task]):
        request_embeddings = self.create_embeddings(user_request)
        maximum = 0
        matching_function = None
        for task in task_list:
            similarity = cosine_similarity(request_embeddings,
                                           task.embeddings)
            if similarity > maximum:
                maximum = similarity
                matching_function = task
        return matching_function


ai = AI()

if __name__ == "__main__":
    pass
