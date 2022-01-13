import sqlite3
from themes import Theme

QUERY = """
SELECT videos.video_id, anime.name, videos.created_at, videos.updated_at, filename, path, basename, size, resources.link  
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
where resources.site = 7;

"""

class ThemeDB:
    def __init__(self):
        self.db = sqlite3.connect("themes.db")

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
            (id, show_name, created_at, updated_at, filename, path, basename, size, mal_link) = row
            theme = Theme(id=id, show_name=show_name, created_at=created_at, 
                        updated_at= updated_at, filename=filename, path= path, 
                        basename=basename, size=size, mal_link=mal_link)
            themes.append(theme)
        return themes