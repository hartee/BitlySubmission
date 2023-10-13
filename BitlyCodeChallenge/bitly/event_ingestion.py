import os

class FileEventIngester:
    """
    This ingester is just a convenience class for the demo project.  In a
    real application, the events would be provided by some kind of message
    or event service.  Here we just use python's yield method to allow the
    main program to read one event at a time to simulate getting them.
    """

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
