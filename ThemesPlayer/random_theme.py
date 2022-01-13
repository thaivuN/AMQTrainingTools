from theme_grouper import ThemeClassification
import random

def randomTheme (tc: ThemeClassification):
    random_key = random.choice(list(tc.categories.keys()))
    random_theme = random.choice(tc.categories[random_key])

    return random_theme
