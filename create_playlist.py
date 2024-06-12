import os

def collect_song_paths(root_dir, extensions):
    """遍历目录收集符合指定扩展名的音乐文件路径"""
    song_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                song_paths.append(os.path.join(dirpath, filename))
    return song_paths

def delete_existing_m3u_files(root_dir):
    """删除目录中所有现有的M3U文件"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.m3u'):
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)
                print(f"已删除: {file_path}")

def create_m3u(playlist_name, song_paths, output_dir):
    """创建M3U播放列表文件，路径从'music'开始"""
    m3u_file_path = os.path.join(output_dir, f"{playlist_name}.m3u")
    
    with open(m3u_file_path, 'w', encoding='utf-8') as m3u_file:
        m3u_file.write("#EXTM3U\n")  # 写入M3U头部
        
        for song_path in song_paths:
            # 将路径转换为统一的格式（Linux路径分隔符为正斜杠）
            song_path = song_path.replace('\\', '/')
            music_index = song_path.lower().find("/music/")
            if music_index != -1:
                relative_path = song_path[music_index:]
            else:
                relative_path = song_path  # 如果未找到'music'，使用完整路径

            song_duration = 0  # 持续时间（秒），未知则为0
            song_title = os.path.basename(song_path)
            m3u_file.write(f"#EXTINF:{song_duration},{song_title}\n")
            m3u_file.write(f"{relative_path}\n")
    
    print(f"M3U播放列表 '{playlist_name}' 已成功创建于 {m3u_file_path}")

# 主函数
if __name__ == "__main__":
    # 获取当前工作目录
    root_dir = os.getcwd()
    # 播放列表名称为当前目录的名称
    playlist_name = os.path.basename(root_dir)
    # 指定的音乐文件扩展名
    extensions = ['.mp3', '.flac', '.wav', '.aac', '.m4a']  
    # 输出目录设为当前工作目录
    output_dir = root_dir  

    delete_existing_m3u_files(root_dir)  # 删除现有的M3U文件
    song_paths = collect_song_paths(root_dir, extensions)  # 收集歌曲路径
    create_m3u(playlist_name, song_paths, output_dir)  # 创建新的M3U文件
