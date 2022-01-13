import sqlite3
from themes import Theme

class ThemeDB:
    def __init__(self):
        self.db = sqlite3.connect("themes.db")

    def getAllRows(self):
        cursor = self.db.cursor()
        cursor.execute ("SELECT video_id, created_at, updated_at, filename, path, basename, size FROM videos")
        rows = cursor.fetchall()
        return rows

    def close(self):
        if self.db:
            self.db.close()

    def getThemes(self):
        rows = self.getAllRows()
        themes = []
        for row in rows:
            (id, created_at, updated_at, filename, path, basename, size) = row
            theme = Theme(id, created_at, updated_at, filename, path, basename, size)
            themes.append(theme)
        return themes