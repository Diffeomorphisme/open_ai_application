from app.open_ai.open_ai import ai
from app.tasks.tasks import descriptions, get_task_list_with_embeddings


def create_functions_embeddings():
    ai.export_embeddings(descriptions,
                         list(ai.create_embeddings(descriptions)))


def ask_question(question: str, tasks):
    response = ai.get_matching_task(question, tasks)
    if not response:
        print("Regardless how hard I try, I cannot help you with that.")
    else:
        if response.sub_tasks:
            ask_question(question=question, tasks=response.sub_tasks)
        print(response.do_task())


def app():
    task_list = get_task_list_with_embeddings()
    while True:
        user_input = input("What can I do for you? ")
        response = ai.match_request_with_function(user_input, task_list)
        print(f"{response.description} "
              f"is the function that corresponds best to your request")
        print(response.do_task())


if __name__ == "__main__":
    # create_functions_embeddings()
    app()
