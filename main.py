# imports so that we can make a child of the parent class App
from config import EXAMS, SEMESTER_START
from logo import LOGO
from datetime import date
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.app import App



def exam_text(exams):
    width = 20
    lines = []
    today = date.today()
    start = date.fromisoformat(SEMESTER_START)

    for exam in exams:
        exam_day = date.fromisoformat(exam["date"])
        days_left = (exam_day - today).days

        total = (exam_day - start).days
        passed = (today - start).days
        progress = passed / total

        filled = round(progress * width)
        bar = f"[violet]{'━' * filled}[/][#3a3a3a]{'━' * (width - filled)}[/]"

        line = f"{exam['course']:<8}{bar}{days_left:>5}d"
        lines.append(line)

    return "\n".join(lines)

class Focal(App):
    CSS_PATH = "focal.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self):
        logo = Static(LOGO, id="logo", classes="panel")
        logo.border_title = "Focal"
        yield Header()
        yield logo
        with Horizontal():
            with Vertical(id="left") as column:
                column.border_title = "Contents"
                yield Static(exam_text(EXAMS))
                yield Static("Assignments")
                yield Static("Tasks")
            with Vertical(id="right") as column:
                column.border_title = "Other"
                yield Static("Today")
                yield Static("Study hours")
        yield Footer()


if __name__ == "__main__":
    Focal().run()

