# imports so that we can make a child of the parent class App
from logo import LOGO
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal, Vertical
from textual.app import App

class Focal(App):
    CSS_PATH = "focal.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def quit(self):
        self.quit()

    def compose(self):
        logo = Static(LOGO, id="exams", classes="panel")
        logo.border_title = "Focal"
        yield Header()
        yield logo
        with Horizontal():
            with Vertical():
                yield Static("Exams")
                yield Static("Assignments")
                yield Static("Tasks")
            with Vertical():
                yield Static("Today")
                yield Static("Study hours")
        yield Footer()

if __name__ == "__main__":
    Focal().run()

