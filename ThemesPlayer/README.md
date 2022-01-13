# AnimeThemes.moe MediaPlayer

Using VLC and PyQT5, this is a simple media player with a quick accessing to all the video links 
inside of AnimeThemes.moe's repository.

### Dependencies + How to Run

Install the dependencies:

`pip install -r requirements.txt`

- You also need VLC
- If you want to update the database file, get MySQL. If not, don't.

Executable File:

`player.exe`


### How to update the DB file?

I use the dump mysql file provided by AnimeThemes.moe and convert it into a SQLite file.
If you want to update the the database used by this program, for now it's going to be a manual process
 by following these steps. Else, you could always wait for me to update that file periodically
 (don't trust me on that).

- Go to https://github.com/AnimeThemes/animethemes-db-dump
- Find and Download the MySQL dump. They update it every week.
- Create a MySQL schema/database
- Run the dump file on that MySQL database/schema
- Delete themes.db
- Get <a href="https://pypi.org/project/mysql-to-sqlite3/">mysql-to-sqlite3</a> and convert the MySQL schema into a SQLite file
   
`pip install mysql-to-sqlite3`
   
`mysql2sqlite -f themes.db -d <NAME_OF_THE_DB_YOU_DUMPED_THE_DATA> -u <DB_USERNAME> -t videos -p`

Else, you could always wait for me to update that themes.db file on this repo (don't trust me on that).

### Notes

- Usage of the MediaPlayer's slider may kill the app.
- Scale-able resizing of app window not yet implemented.
- Have yet to test this on Linux and MAC.
- You may have to update your VLC (do Unistall it and re-install it method, or else the next point will occur) 
and make sure you have the codecs to play webm videos.
- If you used the VLC update tool within the VLC app, you may get a "Entry point not found" error message box 
before this program runs. Close it and the program will run. If it annoys you, do a complete uninstall of VLC 
and re-installing it.
- The terminal will print bunch of error messages during playback. Ignore it for now.
- If nothing happens when you click on the theme you want to play for a while, it might be best to close 
and re-open the app. There's hardly any error handling on this app for now.