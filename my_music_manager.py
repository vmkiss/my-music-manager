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
    with open(SONGS, "r", newline="") as f:
        song_reader = csv.DictReader(f)
        songs = list(song_reader)
        songs = sorted(songs, key=lambda x: x['Title'])

    with open("view_albums.txt", "w") as f:
        for song in songs:
            f.write("ID: " + song["ID"] + "\n")
            f.write("Title: " + song["Title"] + "\n")
            f.write("Artist: " + song["Artist"] + "\n")
            f.write("Album: " + song["Album"] + "\n")
            f.write("Genre: " + song["Genre"] + "\n")
            f.write("\n")
    return

def create_song():
    song_id = str(uuid.uuid4())
    title = input("Enter title of song: ")
    artist = input("Enter name of artist: ")
    genre = input("Enter name of album: ")
    year = input("Enter genre of song: ")

    with open(SONGS, "a", newline="") as f:
        write_data = [song_id, title, artist, genre, year]
        writer = csv.writer(f)
        writer.writerow(write_data)

def delete_song(delete_mode, key):
    with open(SONGS, "r", newline="") as f:
        song_reader = csv.DictReader(f)
        songs = list(song_reader)

    new_songs = [song for song in songs if song[delete_mode] != key]

    if len(songs) == len(new_songs):
        print(f"No album found with {delete_mode}: {key}")
        return

    # Ask if user wants to proceed with deletion
    print(f"Album with {delete_mode}: {key} found!\n")
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

            print(f"Successfully deleted album with {delete_mode}: {key}")
    else:
        return


if __name__ == "__main__":
    view_all_songs()


