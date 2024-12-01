import csv
import os
import uuid
import zmq
import song_dict

# Create CSV file if it doesn't exist yet
HEADERS = ["ID", "Title", "Artist", "Album", "Genre"]
SONGS = "songs.csv"

if not os.path.exists(SONGS):
    with open(SONGS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for song in song_dict.song_dict:
            song.insert(0, str(uuid.uuid4()))
            writer.writerow(song)

def view_all_songs():
    """Read csv file and return all albums in collection"""
    print(54 * "=")
    print("<< VIEW ALL SONGS >>")
    print("Please select an option from the menu.\n")
    print("1. Generate a text file of all songs in your collection")
    print("2. Return to Main Menu\n")

    user_input = "0"
    while user_input != "1" or user_input != "2":
        user_input = input("Please choose an option (1 - 2): ")

        if user_input == "1":
            print("Generating text file of songs...")
            with open(SONGS, "r", newline="") as f:
                song_reader = csv.DictReader(f)
                songs = list(song_reader)
                songs = sorted(songs, key=lambda x: x['Title'])

            with open("view_songs.txt", "w") as f:
                for song in songs:
                    f.write("ID: " + song["ID"] + "\n")
                    f.write("Title: " + song["Title"] + "\n")
                    f.write("Artist: " + song["Artist"] + "\n")
                    f.write("Album: " + song["Album"] + "\n")
                    f.write("Genre: " + song["Genre"] + "\n")
                    f.write("\n")
            print("Song list complete! View your songs in view_songs.txt\n")

            user_input = "0"
            while user_input != "1":
                user_input = input("Enter 1 to return to Main Menu: ")
                if user_input == "1":
                    print("\n")
                    main()

        if user_input == "2":
            print("\n")
            main()

def create_song():
    print(54 * "=")
    print("<< CREATE SONG >>")
    print("Please complete the prompts to create your song.\n")

    song_id = str(uuid.uuid4())
    title = input("Enter title of song: ")
    artist = input("Enter name of artist: ")
    genre = input("Enter name of album: ")
    year = input("Enter genre of song: ")
    print("\n")

    print("1. Save song")
    print("2. Return to Main Menu\n")

    user_input = "0"
    while user_input != "1" or user_input != "2":
        user_input = input("Please choose an option (1 - 2): ")

        if user_input == "1":
            try:
                with open(SONGS, "a", newline="") as f:
                    write_data = [song_id, title, artist, genre, year]
                    writer = csv.writer(f)
                    writer.writerow(write_data)
                print("Song created successfully\n")
                print("1. Create another song")
                print("2. Return to Main Menu\n")

                user_input = "0"
                while user_input != "1" or user_input != "2":
                    user_input = input("Please choose an option (1 - 2): ")
                    if user_input == "1":
                        print("\n")
                        create_song()
                    if user_input == "2":
                        print("\n")
                        main()
            except:
                print("Error occurred. Returning to Main Menu\n")
                main()

        if user_input == "2":
            main()

def delete_menu():
    print(54 * "=")
    print("<< DELETE SONG >>")
    print("Please select an option from the menu.")
    print("Please note: All song IDs are unique, but more than one song may share the same title.\n")
    print("1. Delete by ID: deletes a single song with given ID")
    print("2. Delete by Title: deletes ALL songs with given title")
    print("3. Return to Main Menu\n")

    user_input = "0"
    while user_input != "1" or user_input != "2" or user_input != "3":
        user_input = input("Please choose an option (1 - 3): ")
        print("\n")

        if user_input == "1":
            print(54 * "=")
            print("<< DELETE SONG BY ID >>")
            print("Please enter the exact ID of the song you wish to delete.\n")
            delete_song("ID")
        if user_input == "2":
            print(54 * "=")
            print("<< DELETE SONG BY TITLE >>")
            print("Please enter the exact title of the song you wish to delete.\n")
            delete_song("Title")
        if user_input == "3":
            main()


def delete_song(delete_mode):

    key = input(f"Enter song {delete_mode.lower()}: ")

    with open(SONGS, "r", newline="") as f:
        song_reader = csv.DictReader(f)
        songs = list(song_reader)

    new_songs = [song for song in songs if song[delete_mode] != key]
    print(new_songs)

    if len(songs) == len(new_songs):
        print(f"NO SONG FOUND WITH {delete_mode.upper()}: {key.upper()}\n")
        print(f"1. Enter new song {delete_mode.lower()}")
        print("2. Return to Delete Menu")
        print("3. Return to Main Menu\n")

        user_input = "0"
        while user_input != "1" or user_input != "2" or user_input != "3":
            user_input = input("Please choose an option (1 - 3): ")

            if user_input == "1":
                print("\n")
                delete_song(delete_mode)
            if user_input == "2":
                print("\n")
                delete_menu()
            if user_input == "3":
                print("\n")
                main()

    # Ask if user wants to proceed with deletion
    print(f"SONG WITH {delete_mode.upper()}: {key.upper()} FOUND!\n")
    print(f"!!! ARE YOU SURE YOU WISH TO PROCEED WITH PERMANENTLY DELETING {key.upper()}? !!!")
    print("1. Delete song(s).")
    print("2. Cancel and return to Delete Menu")
    print("3. Cancel and return to Main Menu\n")

    user_choice = 0
    while user_choice != 1 or user_choice != 2 or user_choice != 3:
        user_choice = input("Please choose an option (1 - 3): ")

        if user_choice == "1":
            with open(SONGS, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)
                for song in new_songs:
                    writer.writerow([song["ID"], song["Title"], song["Artist"], song["Album"], song["Genre"]])
                f.flush()

                print(f"Successfully deleted song with {delete_mode.lower()}: {key}\n")
                print("1. Return to Delete Menu")
                print("2. Return to Main Menu\n")

                user_choice = "0"
                while user_choice != 1 or user_choice != 2:
                    user_choice = input("Please choose an option (1 - 2): ")

                    if user_choice == "1":
                        delete_menu()
                    if user_choice == "2":
                        main()

        if user_choice == "2":
            print("\n")
            delete_menu()

        if user_choice == "3":
            print("\n")
            main()


def recommend_menu():
    print(54 * "=")
    print("<< RECOMMEND MUSIC >>")
    print("Please select an option from the menu.\n")
    print("1. Recommend Song: get random song recommendation from songs in collection")
    print("2. Recommend Artist: get random artist recommendation from artists in collection")
    print("3. Recommend Song by Album: get random album recommendation from albums in collection")
    print("4. Return to Main Menu\n")

    user_choice = "0"
    while user_choice != "1" or user_choice != "2" or user_choice != "3" or user_choice != "4":
        user_choice = input("Please choose an option (1 - 4): ")
        if user_choice == "1":
            print("\n")
            recommend_song_menu()
        if user_choice == "2":
            print("\n")
            recommend_artist_menu()
        if user_choice == "3":
            print("\n")
            recommend_album_menu()
        if user_choice == "4":
            print("\n")
            main()

def recommend_song_menu():
    print(54 * "=")
    print("<< RECOMMEND SONG (ALL) >>")
    print("Please select an option from the menu.\n")
    print("1. Generate random song from selection of all songs in collection.")
    print("2. Return to Recommend Song Menu")
    print("3. Return to Main Menu\n")

    user_choice = "0"
    while user_choice != "1" or user_choice != "2" or user_choice != "3":
        user_choice = input("Please choose an option (1 - 3): ")
        if user_choice == "1":
            song_data = load_songs()
            print("\n")
            recommend_song(song_data)
            print("\n")

            print("1. Generate another song")
            print("2. Return to Recommend Music Menu")
            print("3. Return to Main Menu")

            user_choice = 0
            while user_choice != "1" or user_choice != "2" or user_choice != "3":
                user_choice = input("Please choose an option (1 - 3: ")
                if user_choice == "1":
                    print("\n")
                    recommend_song_menu()
                if user_choice == "2":
                    print("\n")
                    recommend_menu()
                if user_choice == "3":
                    print("\n")
                    main()

def recommend_artist_menu():
    print(54 * "=")
    print("<< RECOMMEND ARTIST >>")
    print("Please select an option from the menu.\n")
    print("1. Generate random artist from selection of artists in collection.")
    print("2. Return to Recommend Song Menu")
    print("3. Return to Main Menu\n")

    user_choice = "0"
    while user_choice != "1" or user_choice != "2" or user_choice != "3":
        user_choice = input("Please choose an option (1 - 3): ")
        if user_choice == "1":
            song_data = load_artists()
            print("\n")
            recommend_song(song_data)
            print("\n")

            print("1. Generate another song")
            print("2. Return to Recommend Music Menu")
            print("3. Return to Main Menu")

            user_choice = 0
            while user_choice != "1" or user_choice != "2" or user_choice != "3":
                user_choice = input("Please choose an option (1 - 3: ")
                if user_choice == "1":
                    print("\n")
                    recommend_song_menu()
                if user_choice == "2":
                    print("\n")
                    recommend_menu()
                if user_choice == "3":
                    print("\n")
                    main()


def recommend_album_menu():
    print(54 * "=")
    print("<< RECOMMEND ALBUM >>")
    print("Please select an option from the menu.\n")
    print("1. Generate random album from albums in collection.")
    print("2. Return to Recommend Song Menu")
    print("3. Return to Main Menu\n")

    user_choice = "0"
    while user_choice != "1" or user_choice != "2" or user_choice != "3":
        user_choice = input("Please choose an option (1 - 3): ")
        if user_choice == "1":
            song_data = load_albums()
            print("\n")
            recommend_song(song_data)
            print("\n")

            print("1. Generate another song")
            print("2. Return to Recommend Music Menu")
            print("3. Return to Main Menu")

            user_choice = 0
            while user_choice != "1" or user_choice != "2" or user_choice != "3":
                user_choice = input("Please choose an option (1 - 3: ")
                if user_choice == "1":
                    print("\n")
                    recommend_song_menu()
                if user_choice == "2":
                    print("\n")
                    recommend_menu()
                if user_choice == "3":
                    print("\n")
                    main()


def recommend_song(data):
    context = zmq.Context()
    socket = context.socket(zmq.REQ) # Request socket
    socket.connect("tcp://localhost:5555") # Establish connection

    # Send song data to recommendation microservice
    socket.send_string(data)

    # Wait for response from microservice
    rec = socket.recv_string()
    print(f"YOUR RANDOM SONG RECOMMENDATION IS:\n{rec}")

def load_songs():
    with open(SONGS, 'r') as f:
        song_reader = csv.DictReader(f)
        song_data = ["song"]
        for song in song_reader:
            song_data.append(f"{song['ID']}*{song['Title']}*{song['Artist']}*{song['Album']}*{song['Genre']}")
        return "\n".join(song_data)

def load_artists():
    with open(SONGS, 'r') as f:
        song_reader = csv.DictReader(f)
        artist_data = ["artist"]
        for song in song_reader:
            if song['Artist'] not in artist_data:
                artist_data.append(f"{song['Artist']}")
        return "\n".join(artist_data)

def load_albums():
    with open(SONGS, 'r') as f:
        song_reader = csv.DictReader(f)
        album_data = ["album"]
        for song in song_reader:
            if f"{song['Album']}*{song['Artist']}" not in album_data:
                album_data.append(f"{song['Album']}*{song['Artist']}")
        return "\n".join(album_data)

def search_music_menu():
    print(54 * "=")
    print("<< SEARCH MUSIC >>")
    print("Please select an option from the menu.")
    print("1. Search for Song by Title: search for all songs with the given title")
    print("2. Search for Song by Artist: search for all songs by the given artist")
    print("3. Return to Main Menu\n")

    user_input = "0"
    while user_input != "1" or user_input != "2" or user_input != "3":
        user_input = input("Please choose an option (1 - 3): ")
        print("\n")

        if user_input == "1":
            print(54 * "=")
            print("<< Search for Song by Title >>")
            keyword = input("Please enter the title of the song you wish to search for: ")
            print("\n")
            search_music(keyword, "song")
        if user_input == "2":
            print(54 * "=")
            print("<< Search for Song by Artist >>")
            keyword = input("Please enter the name of the artist whose songs you wish to search for: ")
            print("\n")
            search_music(keyword, "artist")
        if user_input == "3":
            main()


def search_music(keyword, data_type):
    with open(SONGS, 'r') as f:
        song_reader = csv.DictReader(f)
        song_data = [str(keyword)]
        song_data.append(data_type)
        for song in song_reader:
            song_data.append(f"{song['ID']}*{song['Title']}*{song['Artist']}*{song['Album']}*{song['Genre']}")
        song_data = "\n".join(song_data)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Request socket
    socket.connect("tcp://localhost:5555")  # Establish connection

    # Send song data to recommendation microservice
    socket.send_string(song_data)

    # Wait for response from microservice
    rec = socket.recv_string()

    if data_type == 'song':
        print(f"SONGS WITH TITLE {keyword}:\n{rec}")
    if data_type == 'artist':
        print(f"SONGS BY ARTIST {keyword}:\n{rec}")


def features_guide():
    print(54 * "=")
    print("<< FEATURES GUIDE >>")
    print("Need help understanding MyMusicManager's features?\nAll the information you need is below\n")

    with open("features.txt", "r") as f:
        for line in f:
            print(line.rstrip())

    print("\n")
    user_input = "0"
    while user_input != "1":
        user_input = input("Enter 1 to return to Main Menu: ")
        if user_input == "1":
            print("\n")
            main()

def main():
    while True:
        print(54 * "=")
        print(10 * " " + "*** Welcome to MyMusicManager! ***")
        print(54 * "=")
        print("<< MAIN MENU >>")
        print("Select the action you wish to perform.\n")
        print("1. View All Songs")
        print("2. Create Song")
        print("3. Delete Song")
        print("4. Recommend Music")
        print("5. Search Music")
        print("6. View MyMusicManager Features Guide")
        print("7. Exit\n")

        user_input = 0
        while user_input != "1" or user_input != "2" or user_input != "3" or user_input != "4" or user_input != "5" or user_input != "6":
            user_input = input("Please choose an option (1 - 6): ")
            if user_input == "1":
                view_all_songs()
            if user_input == "2":
                create_song()
            if user_input == "3":
                delete_menu()
            if user_input == "4":
                recommend_menu()
            if user_input == "5":
                search_music_menu()
            if user_input == "6":
                features_guide()
            if user_input == "7":
                print("Thank you for using MyMusicManager. Goodbye!")
                exit()

if __name__ == "__main__":
    main()

