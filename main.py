# imports so that we can make a child of the parent class App
from textual.widgets import Header, Footer, Static
from textual.app import App

class Focal(App):
    CSS = """
    Static {
        color: violet;
        text-style: bold;
        content-align: center middle;
        height: 1fr;
    }
    """
    BINDINGS = [("q", "quit", "Quit")]

    def quit(self):
        self.quit()

    def compose(self):
        yield Header()
        yield Static("-- Focal --")
        yield Footer()

if __name__ == "__main__":
    Focal().run()

