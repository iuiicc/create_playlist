import os
import sys

def collect_song_paths(root_dir, extensions):
    song_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                song_paths.append(os.path.join(dirpath, filename))
    return song_paths

def delete_existing_m3u_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.m3u'):
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

def create_m3u(playlist_name, song_paths, output_dir):
    m3u_file_path = os.path.join(output_dir, f"{playlist_name}.m3u")
    
    with open(m3u_file_path, 'w', encoding='utf-8') as m3u_file:
        # Write the M3U header
        m3u_file.write("#EXTM3U\n")
        
        for song_path in song_paths:
            song_duration = 0  # Duration in seconds, 0 if unknown
            song_title = os.path.basename(song_path)
            
            m3u_file.write(f"#EXTINF:{song_duration},{song_title}\n")
            m3u_file.write(f"{song_path}\n")
    
    print(f"M3U playlist '{playlist_name}' created successfully at {m3u_file_path}")

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_playlist.py <root_directory>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory")
        sys.exit(1)
    
    playlist_name = os.path.basename(root_dir)
    extensions = ['.mp3', '.flac', '.wav', '.aac', '.m4a']  # Add more extensions as needed
    output_dir = root_dir  # Output M3U file in the same directory

    delete_existing_m3u_files(root_dir)
    song_paths = collect_song_paths(root_dir, extensions)
    create_m3u(playlist_name, song_paths, output_dir)
