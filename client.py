import xmlrpc.client

def main():
    server_url = input("Enter the server URL (e.g., http://localhost:8000): ")
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
        choice = input("Choose an option: ")

        if choice == '1':
            topic = input("Enter the topic: ")
            text = input("Enter the note text: ")
            timestamp = input("Enter the timestamp (YYYY-MM-DD HH:MM:SS): ")
            try:
                response = proxy.add_note(topic, text, timestamp)
                print("Response from server:", response)
            except Exception as e:
                print(f"Error adding note: {e}")

        elif choice == '2':
            topic = input("Enter the topic to retrieve notes: ")
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
            topic = input("Enter the topic to search on Wikipedia: ")
            try:
                response = proxy.append_wikipedia_data(topic)
                print("Response from server:", response)
            except Exception as e:
                print(f"Error appending Wikipedia data: {e}")

        elif choice == '4':
            print("Exiting the client.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()