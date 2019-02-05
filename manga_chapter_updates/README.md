# Manga.py

Python script to scrape manga subreddits for new chapter releases.

## Usage

```python
manga.py check # checks for new chapter releases, prints results
manga.py reset # resets saved data
manga.py latest # prints latest chapter releases
```

<img src="../manga_chapter_updates/manga_example.JPG" alt="example" width="500"/>

## About

Generates shelf files (mangaShelf.bak, mangaShelf.dir, mangaShelf.dat on windows) to store data. If the program runs into an error, will reset shelf by default. Includes install.bat to install python package dependencies (bs4, requests)

## TODO

- Currently only allows for one manga per subreddit, doesn't support multiple manga releases in a subreddit (ie Goblin Slayer prequel chapters being released simultaneously).
- Change hardcoded manga list to text file storage and add the ability to add/remove tracked manga via command line arguments