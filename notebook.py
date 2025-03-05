from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os
import xml.etree.ElementTree as ET
import datetime
import xml.dom.minidom

class Notebook:
    def __init__(self, filename='db.xml'):
        self.filename = filename
        self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            self.tree = ET.parse(self.filename)
            self.root = self.tree.getroot()
        else:
            self.root = ET.Element('data')
            self.tree = ET.ElementTree(self.root)

    def save_notes(self):
        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml()
        with open(self.filename, 'w') as f:
            f.write(pretty_xml_as_string)

    def add_entry(self, topic, text, timestamp):
        topic_element = self.root.find(f"./topic[@name='{topic}']")
        if topic_element is None:
            topic_element = ET.SubElement(self.root, 'topic', name=topic)
        note_element = ET.SubElement(topic_element, 'note')
        text_element = ET.SubElement(note_element, 'text')
        text_element.text = f"\n{text}\n"
        timestamp_element = ET.SubElement(note_element, 'timestamp')
        timestamp_element.text = f"\n{timestamp}\n"
        self.save_notes()
        return f"Entry added to topic '{topic}'."
    

    def get_entries(self, topic):
        topic_element = self.root.find(f"./topic[@name='{topic}']")
        if topic_element is not None:
            return [f"Text: {note.find('text').text}\nTimestamp: {note.find('timestamp').text}" for note in topic_element.findall('note')]
        return []

    def append_wikipedia_data(self, topic, summary, full_article_url):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_entry(topic, f"Wikipedia Summary: {summary}\nFull Article: {full_article_url}", timestamp)
        return f"Wikipedia data appended to topic '{topic}'."

def main():
    notebook = Notebook()
    server = SimpleXMLRPCServer(('localhost', 8000))
    server.register_instance(notebook)
    print("Server is running on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    main()