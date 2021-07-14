from themes import Theme

class ThemeClassification:
    def __init__(self):
        self.categories = {}

    def addTheme(self, theme: Theme):
        category = theme.getYearCategory()
        if category in self.categories:
            self.categories[category].append(theme)
        else:
            self.categories[category] = []

    def addThemes(self, themes=[]):
        for theme in themes:
            self.addTheme(theme)
