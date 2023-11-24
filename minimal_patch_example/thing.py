
from run import fetch_thing

class Thing:
    def run(self):
        try:
            data = fetch_thing()
        except:
            pass