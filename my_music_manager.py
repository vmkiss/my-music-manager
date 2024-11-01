import csv
import os
import uuid

# Create CSV file if it doesn't exist yet
HEADERS = ["ID", "Title", "Artist", "Album", "Genre"]
ID1 = str(uuid.uuid4())
DATA1 = [ID1, "Death on Two Legs", "Queen", "A Night at the Opera", "Rock"]
ID2 = str(uuid.uuid4())
DATA2 = [ID2, "Red Wine Supernova", "Chappell Roan", "Rise and Fall of a Midwest Princess", "Pop"]
ID3 = str(uuid.uuid4())
DATA3 = [ID3, "Lover, You Should've Come Over", "Jeff Buckley", "Grace", "Rock"]
ID4 = str(uuid.uuid4())
DATA4 = [ID4, "You Oughta Know", "Alanis Morissette", "Jagged Little Pill", "Rock"]
SONGS = "songs.csv"

if not os.path.exists(SONGS):
    with open(SONGS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        writer.writerow(DATA1)
        writer.writerow(DATA2)
        writer.writerow(DATA3)
        writer.writerow(DATA4)

def view_all_songs():
    """Read csv file and return all albums in collection"""
    print(54 * "=")
    print("<< VIEW ALL SONGS >>")
    print("Please select an option from the menu below.\n")
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
    print("Please select an option from the delete menu.")
    print("Please note: All song IDs are unique, but more than one song may share the same title.\n")
    print("1. Delete by ID: deletes a single song with given ID")
    print("2. Delete by Title: deletes ALL songs with given title")
    print("3. Return to Main Menu\n")

    user_input = "0"
    while user_input != "1" or user_input != "2" or user_input != "3":
        user_input = input("Please choose an option (1 - 3): ")
        print("\n")

        if user_input == "1":
            delete_song("ID")
        if user_input == "2":
            delete_song("Title")
        if user_input == "3":
            main()


def delete_song(delete_mode):

    key = input(f"Enter Song {delete_mode}: ")

    with open(SONGS, "r", newline="") as f:
        song_reader = csv.DictReader(f)
        songs = list(song_reader)

    new_songs = [song for song in songs if song[delete_mode] != key]

    if len(songs) == len(new_songs):
        print(f"No album found with {delete_mode}: {key}")
        return

    # Ask if user wants to proceed with deletion
    print(f"Song with {delete_mode}: {key} found!\n")
    print("Are you sure you wish to proceed with deletion?")
    print("Press 1 to proceed.")
    print("Press 2 to cancel.\n")

    user_choice = input("Enter your choice (1 - 2): ")

    if user_choice == "1":
        with open(SONGS, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
            for song in new_songs:
                writer.writerow([song["ID"], song["Title"], song["Artist"], song["Album"], song["Genre"]])

            print(f"Successfully deleted song with {delete_mode}: {key}")

def generate_recommendation():
    pass

def main():
    print(54 * "=")
    print(10 * " " + "*** Welcome to MyMusicManager! ***")
    print(54 * "=")
    print("<< MAIN MENU >>")
    print("Select the action you wish to perform.\n")
    print("1. View All Songs")
    print("2. Create Song")
    print("3. Delete Song")
    print("4. Recommend Song")
    print("5. View MyMusicManager Features Guide")
    print("6. Exit\n")

    user_input = input("Please choose an option (1 - 6): ")
    if user_input == "1":
        view_all_songs()
    if user_input == "2":
        create_song()
    if user_input == "3":
        delete_menu()
    if user_input == "4":
        generate_recommendation()
    if user_input == "4":
        print("Features Guide TBD")
    if user_input == "5":
        return





if __name__ == "__main__":
    main()


