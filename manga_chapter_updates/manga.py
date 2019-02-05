#! python3
# manga.py - checks subreddits for new chapter uploads
# mangaShelf stores latest chapter information
# shelf stores information in the format:
    # 'POST TITLE' : str, 'DATESTRING' : str, [YYYY, MM, DD] : int list, CHAPTERNUMBER : int

import requests, re, bs4, shelve, sys


# resets state of shelf, removing all previously released chapters from the list
def resetShelf(shelfName, mangaList):
    s = shelve.open(shelfName, flag='n')
    
    print('Resetting saved data...')
    for manga in mangaList:
        s[manga] = ['NONE', 'NONE', [0, 0, 0], 0]
    s.close()

    print('Tracking:')
    for i in mangaList:
        print('   ', mangaSubredditToString(i))

# checks if the new chapter post string has already been checked
def checkChapter(shelfName, mangaName, postTitle, postDate, postUTC, chapter):
    s = shelve.open(shelfName, flag='w')

    # checks if the post is newer than the latest chapter post
    for i in range(len(postUTC)):
        if postUTC[i] > s[mangaName][2][i]:
            break
        elif postUTC[i] == s[mangaName][2][i]:
            continue
        else:
            s.close()
            return False
        
    
    # checks if the title is the same as last chapter
    if postTitle == s[mangaName][0]:
        s.close()
        return False
    # checks if its a new chapter
    if chapter <= s[mangaName][3]:
        s.close()
        return False
    else:
        # if its a new chapter, update latest chapter
        s[mangaName] = [postTitle, postDate, postUTC, chapter]
        s.close()
        return True

# takes subreddit and converts it to a more readable string
def mangaSubredditToString(subreddit):
    re_outer = re.compile(r'([^A-Z ])([A-Z])')
    re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
    return re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', subreddit))

# prints the latest chapters from the shelf
def newestChapters(shelfName):
    s = shelve.open(shelfName, 'r')
    mangaList = list(s.keys())

    print('Last Chapter Release:')

    # find longest proper string and chapter names so printing is pretty
    mangaStrings = []
    mangaChapters = []
    max = 0
    max1 = 0
    for manga in mangaList:
        temp = mangaSubredditToString(manga)
        mangaStrings.append(temp)

        temp1 = str(s[manga][3])
        mangaChapters.append(temp1)

        if len(temp) > max:
            max = len(temp)
        if len(temp1) > max1:
            max1 = len(temp1)

    # prints all of the latest chapters
    i = 0
    for string in mangaStrings:
        diff = max - len(string)
        diff1 = max1 - len(mangaChapters[i])
        print(string + diff * ' ' + ' (' + 'Chapter ' + mangaChapters[i] + ')' + (diff1 + 1) * ' ' + 'Released on: ' + s[mangaList[i]][1])
        i += 1
        
    s.close()

def scrapeSubreddits(subreddits):
    url = "https://old.reddit.com/r/" 
    headers = {'User-Agent': 'Mozilla/5.0'}

    # scrapes each subreddit for its posts
    postsList = []
    for subreddit in subreddits:
        urlTemp = url + str(subreddit) + "/"
        page = requests.get(urlTemp, headers=headers)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        attrs = {'class': 'thing'}
        # grabs front page of a subreddit and keeps track of all of its posts
        posts = []
        for post in soup.find_all('div', attrs=attrs):
            l = []
            l.append(post.find('p', class_= 'title').text.lower())
            l.append(str(post.find('p', class_= 'tagline').find('time')))

            posts.append(l) 
            
        postsList.append(posts)
    
    return postsList
            
# gets date in string form 'DAYOFTHEWEEK MONTH DATE' from html
def getDateString(dateString):

    # grabs nicely formated date post
    reg = re.compile(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s...\s\d*\s')
    found = 'Unknown'

    try:
        found = re.search(reg, dateString).group()
        return found
    except:
        return found
        
# gets the date in a list in form [YYYY, MM, DD] from html        
def getDateUTC(dateString):
    # sifts through a bs4 string and finds formatted infomration
    reg = re.compile(r'\d\d\d\d-\d\d-\d\d')
    try:
        found = re.search(reg, dateString).group(0)
        arr = found.split('-')
        temp = []
        for i in arr:
            temp.append(int(i))
        return temp
    except:
        return [0, 0, 0]

# gets the chapter number from the post title
def getChapter(postTitle):
    reg = re.compile(r'\d\d*')

    try:
        found = re.search(reg, postTitle).group(0)
        return(int(found))
    except:
        return(-1)

# checks all manga to see if there is a new chapter release    
def newMangaChapter(mangaDict, mangaList):
    newChapter = False
    posts = scrapeSubreddits(mangaList)

    index = 0


    for post in posts:
        manga = mangaList[index]
        reg = re.compile(mangaDict[manga][0], re.IGNORECASE)

        index += 1
        for data in post:
            # checks post titles for keywords that would indicate a new chapter release
            title = data[0]

            matches = re.findall(reg, title)
            matches = list(set(matches))


            if len(matches) >= mangaDict[manga][1]:
                time = getDateString(str(data[1]))
                date = getDateUTC(str(data[1]))
                chapter = getChapter(title)

                if checkChapter('mangaShelf', manga, title, time, date, chapter):
                    # Converts subreddit name to normal form
                    mangaStr = mangaSubredditToString(manga)
                    print('New ' + mangaStr + ' Chapter')
                    newChapter = True
                    

    # no new chapters
    if not newChapter:
        print('No new Chapters.')



if __name__ == "__main__":
    # Dictionary of subreddit names and new chapter release keywords
    mangaDict = {
        'BokuNoHeroAcademia' : [r'Chapter|Discussion|Links?', 3],
        'ShingekiNoKyojin' : [r'New|Chapter|RELEASE', 3],
        'ShokugekiNoSoma' : [r'Chapter|Links?|Discussion\s', 2],
        'GoblinSlayer' : [r'Chapter|Disc\.|CH\.', 3],
        'ThePromisedNeverland' : [r'Manga|Chapter|Links?|Discussion', 4],
        'OnePunchMan' : [r'One|Punch|Man|Chapter|English', 5]
    }
    # TODO
    # switch from hardcoded subreddits and regex to text file storage
    # additionally add method to add/remove manga trackings to the text file

    mangaList = list(mangaDict.keys())

    if len(sys.argv) == 2:
        if sys.argv[1] == 'reset':
            resetShelf('mangaShelf', mangaList)
        if sys.argv[1] == 'check':
            try:
                newMangaChapter(mangaDict, mangaList)   
            except:
                print('Error Occurred - Resetting Shelf')
                resetShelf('mangaShelf', mangaList)
                try: 
                    newMangaChapter(mangaDict, mangaList)
                except:
                    print('Error Occured')
        if sys.argv[1] == 'latest':
            newestChapters('mangaShelf')
    else:
        print(
            "Reddit Manga Chapter Scraper Usage:\n"
            "manga.py reset: resets saved data\n"
            "manga.py check: checks for new chapter uploads\n"
            "manga.py latest: prints latest chapter releases"
            )


        
   
