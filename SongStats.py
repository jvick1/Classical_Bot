import os
import json
#from pydub import AudioSegment  
#Use pydub for audio manipulation

# Initialize song metadata
song_directory = 'E:/Code/Python/Classical_Bot/Songs/'
song_history_file = 'song_usage_history.json'

# Load or initialize song usage history
if os.path.exists(song_history_file):
    with open(song_history_file, 'r') as f:
        song_usage_history = json.load(f)
else: 
    song_usage_history = {}

# Function to read songs from the directory and parse metadata
def load_songs():
    songs = []
    for filename in os.listdir(song_directory):
        if filename.endswith('.mp3'):
            artist, title, length, mood = parse_filename(filename)
            duration = parse_duration(length)
            usage_count = song_usage_history.get(filename, 0)
            songs.append({
                'filename': filename,
                'artist': artist,
                'title': title,
                'duration': duration,
                'mood': mood,
                'usage_count': usage_count
            })
    return songs

#extract metadata
def parse_filename(filename):
    # Assuming filename format: Artist, Song, Xmin Ysec, Mood.mp3
    parts = filename[:-4].split(',')
    artist, title = parts[0].strip(), parts[1].strip()
    time_part = parts[2].strip()
    mood = parts[3].strip()
    return artist, title, time_part, mood

#convert time to seconds
def parse_duration(length):
    minutes, seconds = map(int, length.replace("min", "").replace("sec", "").split())
    return minutes * 60 + seconds

# Function to calculate total duration by artist
def total_duration_by_artist(songs):
    artist_duration = {}
    for song in songs:
        artist = song['artist']
        duration = song['duration']
        if artist in artist_duration:
            artist_duration[artist] += duration
        else:
            artist_duration[artist] = duration
    return artist_duration

# Function to list tracks by artist
def songs_by_artist(songs, artist_name):
    artist_songs = []
    for song in songs:
        if song['artist'] == artist_name:
            artist_songs.append(f"{song['title']} ({song['duration']} seconds)")
    return artist_songs

# Function to call songs_by_artist for every artist in the dataset
def songs_by_all_artists(songs):
    # Extract unique artists
    artists = set(song['artist'] for song in songs)
    
    # Call songs_by_artist for each artist
    all_artist_songs = {}
    for artist in artists:
        all_artist_songs[artist] = songs_by_artist(songs, artist)
    
    return all_artist_songs

# Function to call songs_by_artist for one or more artists
def songs_by_artists(songs, artists):
    # If a single artist is provided, convert it into a list
    if isinstance(artists, str):
        artists = [artists]
    
    # Call songs_by_artist for each artist in the list
    selected_artist_songs = {}
    for artist in artists:
        selected_artist_songs[artist] = songs_by_artist(songs, artist)
    
    return selected_artist_songs

# Function to calculate total duration by mood
def total_duration_by_mood(songs):
    mood_duration = {}
    for song in songs:
        mood = song['mood']
        duration = song['duration']
        if mood in mood_duration:
            mood_duration[mood] += duration
        else:
            mood_duration[mood] = duration
    return mood_duration

# Main program
if __name__ == '__main__':
    songs = load_songs()
    print("\nSummary Stats:\n")
    
    # Calculate and display total duration by artist
    artist_durations = total_duration_by_artist(songs)
    print("Total Duration by Artist:")
    for artist, duration in artist_durations.items():
        print(f"{artist}: {duration // 60} min")

    # Calculate and display total duration by mood
    mood_durations = total_duration_by_mood(songs)
    print("\nTotal Duration by Mood:")
    for mood, duration in mood_durations.items():
        print(f"{mood}: {duration // 60} min")

    # Get all songs by every artist
    all_songs_by_artists = songs_by_all_artists(songs)
    for artist, songs_list in all_songs_by_artists.items():
        print(f"Songs by {artist}:")
        print(songs_list)
        print()
    
    # Get songs by multiple artists
    print("Baroque/Classical Era")
    print(songs_by_artists(songs, ['Bach', 'Mozart']))