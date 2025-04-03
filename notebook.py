from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os
import xml.etree.ElementTree as ET
import datetime

class Notebook:
    def __init__(self, filename='db.xml'):
        self.filename = filename
        self.load_notes()

    def load_notes(self):
        try:
            if os.path.exists(self.filename):
                self.tree = ET.parse(self.filename)
                self.root = self.tree.getroot()
            else:
                self.root = ET.Element('data')
                self.tree = ET.ElementTree(self.root)
        except ET.ParseError as e:
            self.root = ET.Element('data')
            self.tree = ET.ElementTree(self.root)
            print(f"Error loading notes: {e}")

    def save_notes(self):
        try:
            self.indent(self.root)
            self.tree.write(self.filename, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def add_entry(self, topic, text, timestamp):
        try:
            topic_element = self.root.find(f"./topic[@name='{topic}']")
            if topic_element is None:
                topic_element = ET.SubElement(self.root, 'topic', name=topic)
            note_element = ET.SubElement(topic_element, 'note')
            text_element = ET.SubElement(note_element, 'text')
            text_element.text = text
            timestamp_element = ET.SubElement(note_element, 'timestamp')
            timestamp_element.text = timestamp
            self.save_notes()
            return f"Entry added to topic '{topic}'."
        except Exception as e:
            return f"Error adding entry: {e}"

    def get_entries(self, topic):
        try:
            topic_element = self.root.find(f"./topic[@name='{topic}']")
            if topic_element is not None:
                return [f"Text: {note.find('text').text}\nTimestamp: {note.find('timestamp').text}" for note in topic_element.findall('note')]
            return []
        except Exception as e:
            return f"Error retrieving entries: {e}"

    def append_wikipedia_data(self, topic, summary, full_article_url):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.add_entry(topic, f"Wikipedia Summary: {summary}\nFull Article: {full_article_url}", timestamp)
            return f"Wikipedia data appended to topic '{topic}'."
        except Exception as e:
            return f"Error appending Wikipedia data: {e}"

def main():
    try:
        notebook = Notebook()
        server = SimpleXMLRPCServer(('localhost', 8000))
        server.register_instance(notebook)
        print("Server is running on port 8000...")
        server.serve_forever()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()