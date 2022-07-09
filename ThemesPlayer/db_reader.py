from importlib.metadata import requires
import sqlite3
from themes import Theme
from setting import CURR_DB

QUERY = """
SELECT videos.video_id, anime.name, videos.created_at, videos.updated_at, filename, path, basename, size, resources.link, anime_themes.slug, songs.title, GROUP_CONCAT(DISTINCT artists.name)
FROM videos
INNER JOIN anime_theme_entry_video 
on videos.video_id = anime_theme_entry_video.video_id
INNER JOIN anime_theme_entries
on anime_theme_entry_video.entry_id = anime_theme_entries.entry_id
INNER JOIN anime_themes
on anime_theme_entries.theme_id = anime_themes.theme_id
INNER JOIN anime
on anime_themes.anime_id = anime.anime_id
INNER JOIN anime_resource
on anime.anime_id = anime_resource.anime_id
INNER JOIN resources
on anime_resource.resource_id = resources.resource_id
INNER JOIN artist_song
on anime_themes.song_id = artist_song.song_id
INNER JOIN artists
on artist_song.artist_id = artists.artist_id
INNER JOIN songs
on artist_song.song_id = songs.song_id
where resources.site = 7
group by videos.video_id;

"""

class ThemeDB:
    def __init__(self):
        self.db = sqlite3.connect(CURR_DB)

    def getAllRows(self):
        cursor = self.db.cursor()
        cursor.execute (QUERY)
        rows = cursor.fetchall()
        return rows

    def close(self):
        if self.db:
            self.db.close()

    def getThemes(self):
        rows = self.getAllRows()
        themes = []
        for row in rows:
            (id, show_name, created_at, updated_at, filename, path, basename, size, mal_link, slug,song, artist) = row
            theme = Theme(id=id, show_name=show_name, created_at=created_at, 
                        updated_at= updated_at, filename=filename, path= path, 
                        basename=basename, size=size, mal_link=mal_link, slug=slug, song=song,artist=artist)
            themes.append(theme)
        return themes