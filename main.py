from config import EXAMS, SEMESTER_START, DAILY_GOAL, COURSES
from logo import LOGO

import csv
from datetime import date

from pyfiglet import figlet_format
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.app import App
from textual.screen import Screen

def log_time(course, rec_date, time):
    with open("sessions.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([course, rec_date, time])

def time_per_course():
    totals = {}
    with open("sessions.csv", newline="") as file:
        for row in csv.reader(file):
            course, rec_date, time = row
            if str(date.today()) == rec_date:
                totals[course] = totals.get(course, 0) + int(time)
        return totals

def goal_text():
    totals = time_per_course()
    lines = []

    for course in COURSES:
        line = f"{course:>7} {totals.get(course, 0)} / {DAILY_GOAL} "
        lines.append(line)

    return "\n".join(lines)

def exam_text(exams):
    width = 27
    lines = []
    today = date.today()
    start = date.fromisoformat(SEMESTER_START)

    for exam in exams:
        exam_day = date.fromisoformat(exam["date"])
        date_text = exam_day.strftime("%d.%m")
        days_left = (exam_day - today).days

        total = (exam_day - start).days
        passed = (today - start).days
        progress = passed / total

        filled = round(progress * width)
        bar = f"[violet]{'━' * filled}[/][#3a3a3a]{'━' * (width - filled)}[/]"

        line = f"{exam['course']:<8}{bar}{days_left:>3}d {date_text}"
        lines.append(line)

    return "\n".join(lines)

def timer_format(time):
    hours, rest = divmod(time, 3600)
    minutes, seconds = divmod(rest, 60)
    timer = f"{hours:02}:{minutes:02}:{seconds:02}"
    screen_timer = figlet_format(timer, font="Terrace")
    return screen_timer



class TimerScreen(Screen):
    BINDINGS = [("escape", "back", "Back"),
                ("space", "pause", "Pause"),
                ("1", "subject('MEK2000')", "Math"),
                ("2", "subject('ELI2300')", "Dynamic systems"),
                ("3", "subject('MEK3100')", "Programming"),
                ("s", "stop", "Stop"),
    ]

    def on_mount(self):
        self.count = 0
        self.course = None
        self.pause = True
        self.ticker = self.set_interval(1, self.tick, pause=self.pause)

    def compose(self):
        yield Header()
        with Vertical():
            yield Static(timer_format(0), id="clock", classes="panel")
            yield Static("No course", id="course", classes="panel")
        yield Footer()

    def action_back(self):
        self.action_stop()
        self.app.pop_screen()

    def action_stop(self):
        self.pause = True
        self.ticker.pause()
        if self.count != 0:
            log_time(self.course, date.today(), self.count)
            self.count = 0
            self.query_one("#clock", Static).update(timer_format(0))

    def action_subject(self, name):
        self.course = name
        self.query_one("#course", Static).update(self.course)

    def action_pause(self):
        if self.pause:
            self.pause = False
            self.ticker.resume()
        else:
            self.pause = True
            self.ticker.pause()

    def tick(self):
        self.count += 1
        self.query_one("#clock", Static).update(timer_format(self.count))

class Focal(App):
    CSS_PATH = "focal.tcss"
    BINDINGS = [("q", "quit", "Quit"), ("t", "open_timer", "Timer")]

    def action_open_timer(self):
        self.push_screen(TimerScreen())

    def compose(self):
        logo = Static(LOGO, id="logo", classes="panel")
        logo.border_title = "Focal"
        exams = Static(exam_text(EXAMS), id="exams", classes="panel")
        exams.border_title = "Exams"
        yield Header()
        yield logo

        with Horizontal():

            with Vertical(id="left"):
                exams = Static(exam_text(EXAMS), id="exams", classes="panel")
                exams.border_title = "Exams"
                yield exams

                assignments = Static("", id="assignments", classes="panel")
                assignments.border_title = "Assignments"
                yield assignments

                tasks = Static("", id="tasks", classes="panel")
                tasks.border_title = "Tasks"
                yield tasks

            with Vertical(id="right") as column:
                column.border_title = "Other"
                yield Static("Today")
                yield Static("Study hours")

        yield Footer()


if __name__ == "__main__":
    Focal().run()

