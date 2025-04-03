import xmlrpc.client
import datetime

def prompt_non_empty(prompt_msg, error_msg):
    while True:
        data = input(prompt_msg)
        if data.strip() == "":
            print(error_msg)
        else:
            return data.strip()

def prompt_valid_timestamp(prompt_msg):
    while True:
        ts = input(prompt_msg)
        if ts.strip() == "":
            print("Timestamp cannot be empty.")
            continue
        try:
            datetime.datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M:%S")
            return ts.strip()
        except ValueError:
            print("Incorrect timestamp format, please use YYYY-MM-DD HH:MM:SS.")

def main():
    server_url = prompt_non_empty("Enter the server URL (e.g., http://localhost:8000): ", "Server URL cannot be empty.")
    try:
        proxy = xmlrpc.client.ServerProxy(server_url)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return

    while True:
        print("\nOptions:")
        print("1. Add a note")
        print("2. Retrieve notes")
        print("3. Search Wikipedia and append data")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        while choice not in ['1', '2', '3', '4']:
            choice = input("Choose an option: ").strip()

        if choice == '1':
            topic = prompt_non_empty("Enter the topic: ", "Input some data as a topic")
            text = prompt_non_empty("Enter the note text: ", "Do not leave this part empty")
            timestamp = prompt_valid_timestamp("Enter the timestamp (YYYY-MM-DD HH:MM:SS): ")
            try:
                response = proxy.add_note(topic, text, timestamp)
                print("Response from server:", response)
            except Exception as e:
                print(f"Error adding note: {e}")

        elif choice == '2':
            topic = prompt_non_empty("Enter the topic to retrieve notes: ", "Topic cannot be empty")
            try:
                notes = proxy.get_notes(topic)
                if notes:
                    print("Notes for topic '{}':".format(topic))
                    for note in notes:
                        print(note)
                else:
                    print("There are no topics like '{}'".format(topic))
            except Exception as e:
                print(f"Error retrieving notes: {e}")

        elif choice == '3':
            topic = prompt_non_empty("Enter the topic to search on Wikipedia: ", "Search topic cannot be empty")
            try:
                response = proxy.append_wikipedia_data(topic)
                print("Response from server:", response)
            except Exception as e:
                print(f"Error appending Wikipedia data: {e}")

        elif choice == '4':
            print("Exiting the client.")
            break

if __name__ == "__main__":
    main()