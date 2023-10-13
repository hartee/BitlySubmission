import os

class FileEventIngester:
    # class constants
    SHORT_DATA = os.path.join(os.path.dirname(__file__), "data", "short.json")
    FULL_DATA = os.path.join(os.path.dirname(__file__), "data", "challenge.json")


    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def get_events(self):
        for event in self.file:
            yield event.strip()

# Usage example:
if __name__ == "__main__":
    with FileEventIngester(FileEventIngester.SHORT_DATA) as reader:
        for event in reader.get_events():
            print(event)
