from xmlrpc.server import SimpleXMLRPCServer
import logging
from wikipedia_api import get_wikipedia_data
from notebook import Notebook

logging.basicConfig(level=logging.INFO)

class NotebookServer:
    def __init__(self):
        self.notebook = Notebook()

    def add_note(self, topic, text, timestamp):
        try:
            response = self.notebook.add_entry(topic, text, timestamp)
            logging.info(response)
            return response
        except Exception as e:
            logging.error(f"Error adding note: {e}")
            return f"Error adding note: {e}"

    def get_notes(self, topic):
        try:
            notes = self.notebook.get_entries(topic)
            if notes:
                return notes
            else:
                return []
        except Exception as e:
            logging.error(f"Error retrieving notes: {e}")
            return f"Error retrieving notes: {e}"

    def append_wikipedia_data(self, topic):
        try:
            summary, full_article_url = get_wikipedia_data(topic)
            response = self.notebook.append_wikipedia_data(topic, summary, full_article_url)
            logging.info(response)
            return response
        except Exception as e:
            logging.error(f"Error appending Wikipedia data: {e}")
            return f"Error appending Wikipedia data: {e}"

def main():
    try:
        server = SimpleXMLRPCServer(("localhost", 8000))
        server.register_instance(NotebookServer())
        logging.info("Server started on localhost:8000")
        server.serve_forever()
    except Exception as e:
        logging.error(f"Error starting server: {e}")

if __name__ == "__main__":
    main()