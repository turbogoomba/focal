# imports so that we can make a child of the parent class App
from pyfiglet import figlet_format
from config import EXAMS, SEMESTER_START
from logo import LOGO
from datetime import date
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.app import App
from textual.screen import Screen

class TimerScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self):
        yield Header()
        yield Static("This is a timer")
        yield Footer()


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

class TimerScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self):
        timer = Static(figlet_format("12:10", font="Terrace"), id="clock", classes="panel")
        timer.border_title = "Timer"
        yield Header()
        with Vertical():
            yield timer
        yield Footer()


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

