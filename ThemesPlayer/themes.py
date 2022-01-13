from enum import Enum

class Theme:
    def __init__(self, id, show_name, created_at, updated_at, filename, path, basename, size, mal_link):
        self.id = id
        self.show_name = show_name
        self.created_at = created_at
        self.updated_at = updated_at
        self.filename = filename
        self.path = path
        self.basename = basename
        self.size = size
        self.mal_link = mal_link

    def __str__(self):
        line = f"({self.id}, {self.show_name}, {self.created_at}, {self.updated_at}, {self.filename}, {self.path}, {self.basename}, {self.size}, {self.mal_link}, {self.getYearCategory()})"
        return line

    def getYearCategory(self):
        if "/" in str(self.path):
            year_category = str(self.path).split("/")[0]
            return year_category
        return "Other"
    
    def getUrl(self):
        return f"https://animethemes.moe/video/{self.filename}"