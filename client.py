import xmlrpc.client

def main():
    server_url = input("Enter the server URL (e.g., http://localhost:8000): ")
    proxy = xmlrpc.client.ServerProxy(server_url)

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
            response = proxy.add_note(topic, text, timestamp)
            print("Response from server:", response)

        elif choice == '2':
            topic = input("Enter the topic to retrieve notes: ")
            notes = proxy.get_notes(topic)
            if notes:
                print("Notes for topic '{}':".format(topic))
                for note in notes:
                    print(note)
            else:
                print("There are no topics like '{}'".format(topic))

        elif choice == '3':
            topic = input("Enter the topic to search on Wikipedia: ")
            response = proxy.append_wikipedia_data(topic)
            print("Response from server:", response)

        elif choice == '4':
            print("Exiting the client.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()