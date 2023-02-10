import requests
from bs4 import BeautifulSoup

from app.tasks.model import Task


class Weather(Task):
    def __init__(self):
        super().__init__()
        self.description = "Get weather data"
        self.subtasks: list[Task] = []

    def do_task(self):
        return "No data to show here"


class WeatherGbg(Task):
    def __init__(self):
        super().__init__()
        self.description = "Get weather for Gothenburg, Sweden"

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


class Meeting(Task):
    def __init__(self):
        super().__init__()
        self.description = "Interacting with calendar"
        self.subtasks: list[Task] = []


class BookMeeting(Task):
    def __init__(self):
        super().__init__()
        self.description = "Book a meeting"
        self.subtasks: list[Task] = []

    def do_task(self):
        return "Meeting booked!"


class CancelMeeting(Task):
    def __init__(self):
        super().__init__()
        self.description = "Delete a meeting"
        self.subtasks: list[Task] = []

    def do_task(self):
        return "Meeting canceled!"


class Onboarding(Task):
    def __init__(self):
        super().__init__()
        self.description = "Help with employee onboarding at QueensLab"

    def do_task(self):
        return "Here is all you need to know"


weather = Weather()
meeting = Meeting()
onboarding = Onboarding()

weather_gbg = WeatherGbg()
weather.sub_tasks.append(weather_gbg)

book_meeting = BookMeeting()
cancel_meeting = CancelMeeting()
meeting.sub_tasks.append(book_meeting)
meeting.sub_tasks.append(cancel_meeting)

task_list = [weather, meeting, onboarding]


if __name__ == "__main__":
    for task in task_list:
        print(task.description)
        # print(task.do_task())


