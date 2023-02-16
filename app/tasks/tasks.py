import requests
from bs4 import BeautifulSoup
import json

from app.tasks.model import Task


class Weather(Task):
    def __init__(self):
        super().__init__()
        self.description = "Get weather data"
        self.embeddings: list[Task] = []

    def do_task(self):
        return "No data to show here"


class WeatherCity(Task):
    def __init__(self):
        super().__init__()
        self.description = "Get weather data for Gothenburg."
        self.embeddings: list[Task] = []

    def do_task(self):
        url = "https://www.yr.no/en/forecast/daily-table/2-2711537/Sweden/V" \
              "ästra%20Götaland/Gothenburg%20Municipality/Gothenburg"
        response = requests.request('GET', url)
        temperature = ""
        if response.status_code == 200:
            text = response.text
            soup = BeautifulSoup(text, "html.parser")
            temperature = soup.find_all(
                'span', class_="temperature temperature--warm")[1].get_text()
        if temperature:
            return f"It's currently {temperature}C in Göteborg"
        else:
            return "Could not find your weather data."


class BookMeeting(Task):
    def __init__(self):
        super().__init__()
        self.description = "Book a meeting."
        self.embeddings: list = []

    def do_task(self):
        return "Meeting booked!"


class CancelMeeting(Task):
    def __init__(self):
        super().__init__()
        self.description = "Delete a meeting."
        self.embeddings: list = []

    def do_task(self):
        return "Meeting canceled!"


class Onboarding(Task):
    def __init__(self):
        super().__init__()
        self.description = "Help with employee onboarding at QueensLab."
        self.embeddings: list = []

    def do_task(self):
        return "Here is all you need to know"


weather = Weather()
weather_city = WeatherCity()
book_meeting = BookMeeting()
cancel_meeting = CancelMeeting()
onboarding = Onboarding()


task_list = [weather, weather_city, book_meeting, cancel_meeting, onboarding]
descriptions = [task.description for task in task_list]
embeddings = [task.embeddings for task in task_list]


def get_task_list_with_embeddings():
    with open("app/tasks/embeddings/embeddings.txt", "r") as file:
        for line in file:
            [description, embedding] = line.strip().split(";")
            for task in task_list:
                if task.description == description:
                    task.embeddings = [float(number)
                                       for number in json.loads(embedding)]
                    break
    return task_list
