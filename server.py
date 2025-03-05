from xmlrpc.server import SimpleXMLRPCServer
import logging
from wikipedia_api import get_wikipedia_data
from notebook import Notebook

logging.basicConfig(level=logging.INFO)

class NotebookServer:
    def __init__(self):
        self.notebook = Notebook()

    def add_note(self, topic, text, timestamp):
        response = self.notebook.add_entry(topic, text, timestamp)
        logging.info(response)
        return response

    def get_notes(self, topic):
        notes = self.notebook.get_entries(topic)
        if notes:
            return notes
        else:
            return []

    def append_wikipedia_data(self, topic):
        summary, full_article_url = get_wikipedia_data(topic)
        response = self.notebook.append_wikipedia_data(topic, summary, full_article_url)
        logging.info(response)
        return response

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(NotebookServer())
    logging.info("Server started on localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    main()