#! python3
# manga.py - checks subreddits for new chapter uploads
# mangaShelf stores latest chapter information
# shelf stores information in the format:
    # 'POST TITLE' : str, 'DATESTRING' : str, [YYYY, MM, DD] : int list, CHAPTERNUMBER : int

import requests, re, bs4, shelve, sys, string


class Manga:
    '''
    Manga class for each tracked Manga title.

    __init__
        :param string name:
        :param string regex:
        :param int threshold:

    Attributes:
        name (str): name of the tracked manga
        regex (re.compile): regex pattern to be matched when scraping
        threshold (int): number of matches required to confirm new chapter
        chapter_list (list[int]): list of chapter numbers tracked
        release_date_list (list[str]): list of tracked release dates
        release_date_UTC_list (list[str]): list of tracked dates in ####-##-## format

    '''

    def __init__(self, name, regex, threshold):
        self.name = name
        self.regex = re.compile(regex, re.IGNORECASE)
        self.threshold = threshold
        self.chapter_list = []
        self.release_date_list = []
        self.release_date_UTC_list = []

    # adds new entry
    def add_entry(self, chapter_number, release_date, release_date_UTC):
        self.chapter_list.append(chapter_number)
        self.release_date_list.append(release_date)
        self.release_date_UTC_list.append(release_date_UTC)

    # removes oldest entry
    def remove_entry(self):
        self.chapter_list.pop(0)
        self.release_date_list.pop(0)
        self.release_date_UTC_list.pop(0)
    
    def __str__(self):
        ret_string = '{}\n{} {}'.format(self.name, self.regex, self.threshold)
        for ch, date, UTC in zip(self.chapter_list, self.release_date_list, self.release_date_UTC_list):
            ret_string += '\nChapter: {}, {}, {}'.format(ch, date, UTC)
        return ret_string


# checks if the new chapter post string has already been checked
def check_chapter(manga, chapter, postDate, postUTC):
    ch_list = manga.chapter_list
    if len(ch_list) == 0:
        manga.add_entry(int(chapter), postDate, postUTC)
        return True

    # print(type(chapter), type(ch_list[-1]))
    if chapter < ch_list[-1] or chapter in ch_list:
        return False
    else:
        manga.add_entry(int(chapter), postDate, postUTC)
        return True

# takes subreddit and converts it to a more readable string
def manga_subreddit_to_string(subreddit):
    re_outer = re.compile(r'([^A-Z ])([A-Z])')
    re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
    return re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', subreddit))

# prints the latest chapters from the shelf
def newest_chapters(manga_dict):
    '''
    Prints the newest chapters for each tracked Manga.

    :param dict[Manga] manga_dict: dictionary of tracked Manga objects
    :rtype: None
    '''
    manga_names = list(manga_dict.keys())

    print('Latest Chapters:')

    # find longest proper string and chapter names so printing is pretty
    manga_strings = []
    manga_chapters = []
    max1= 0
    max2 = 0
    for name in manga_names:
        manga = manga_dict[name]
        temp = manga_subreddit_to_string(name)
        manga_strings.append(temp)

        if len(manga.chapter_list) <= 0:
            temp1 = 'NONE'
            manga.add_entry(-1, 'NONE', 'NONE')
        else:
            temp1 = str(manga.chapter_list[0])
        manga_chapters.append(temp1)

        if len(temp) > max1:
            max1= len(temp)
        if len(temp1) > max2:
            max2 = len(temp1)

    # prints all of the last read chapters
    for name, chapter in zip(manga_names, manga_chapters):
        manga = manga_dict[name]
        name = manga_subreddit_to_string(name)
        diff = max1- len(name)
        diff1 = max2 - len(chapter)
        print(name + diff * ' ' + ' (' + 'Chapter ' + chapter + ')' + (diff1 + 1) * ' ' + 'Released on: ' + manga.release_date_list[0])
    

def scrape_subreddits(subreddits):
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
def get_date_string(dateString):

    # grabs nicely formated date post
    reg = re.compile(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s...\s\d*\s')
    found = 'Unknown'

    try:
        found = re.search(reg, dateString).group()
        return found
    except:
        return found
        
# gets the date in a list in form [YYYY, MM, DD] from html        
def get_date_UTC(dateString):
    # sifts through a bs4 string and finds formatted infomration
    reg = re.compile(r'\d\d\d\d-\d\d-\d\d')
    try:
        found = re.search(reg, dateString).group(0)
        return found
    except:
        return '0000-00-00'

# gets the chapter number from the post title
def get_chapter(postTitle):
    reg = re.compile(r'\d\d*')

    try:
        found = re.search(reg, postTitle).group(0)
        return(int(found))
    except:
        return(-1)

# checks all manga to see if there is a new chapter release    
def check_for_new_chapter(manga_dict, manga_list):
    '''
    Scrapes every tracked Manga's subreddit for new releases.

    :param dict[Manga] manga_dict: 
        dictionary containing all tracked Manga objects
    :param list[str] manga_list: list of strings representing tracked Manga
    :rtype: None
    '''
    new_chapter = False
    posts = scrape_subreddits(manga_list)

    index = 0


    for post, manga_name in zip(posts, manga_list):
        reg = manga_dict[manga_name].regex

        index += 1
        for data in post:
            # checks post titles for keywords that would indicate a new chapter release
            title = data[0]
            # removes all punctuation from title
            title = title.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))

            matches = re.findall(reg, title)
            matches = list(set(matches))


            if len(matches) >= manga_dict[manga_name].threshold:
                date = get_date_string(str(data[1]))
                UTC = get_date_UTC(str(data[1]))
                chapter = get_chapter(title)

                if check_chapter(manga_dict[manga_name], chapter, date, UTC):
                    # Converts subreddit name to normal form
                    mangaStr = manga_subreddit_to_string(manga_name)
                    print('New ' + mangaStr + ' Chapter')
                    new_chapter = True
                    

    # no new chapters
    if not new_chapter:
        print('No new Chapters.')
    print('')

def load_text_file(filename):
    '''
    Loads manga_dict from text file. First line of text file contains how many manga are being followed, the first line for each manga contains the name of the manga, the regex used to match a chapter upload, how many matches constitutes a chapter upload, and how many chapters are currently being tracked. Each line following contains the chapter number and the upload date.

    :param string filename: text file
    :rtype dict[Manga] manga_dict: 
        dictionary of Manga objects initialized from filename
    '''

    manga_dict = {}
    with open(filename, 'r') as f:
        # first line in the file contains the number of tracked manga
        num_manga = int(f.readline())
        for _ in range(num_manga):
            # each manga has a line containing the name, the regex, threshold, and number of chapters currently tracked
            f_line = list(f.readline().strip().split(' '))
            manga_name = f_line[0]

            reg = f_line[1]
            count_threshold = int(f_line[2])

            manga = Manga(manga_name, reg, count_threshold)

            for _ in range(int(f_line[3])):
                # adds each tracked chapter
                chapter_line = list(f.readline().strip().split(', '))
                manga.add_entry(
                    int(chapter_line[0]), chapter_line[1], chapter_line[2]
                )
            
            manga_dict[manga_name] = manga 
    
    return manga_dict
        
def write_text_file(filename, manga_dict):
    '''
    Saves current Manga information to filename text file. File format:
        int : number of manga
        manga: string, string, int, int
            subreddit/manga name, regex expression, match threshold, number of chapters tracked
        chapter tracked: int, string, ####-##-##
            chapter number, date released, date released number format


    :param string filename: output text file name
    :param dict[Manga] manga_dict: dictionary containing all tracked manga
    :rtype: None
    '''

    keys = manga_dict.keys()
    with open(filename, 'w') as f:
        print(len(keys), file=f)
        
        for manga in keys:
            m = manga_dict[manga]
            print(m.name, m.regex.pattern, m.threshold, len(m.chapter_list), sep=' ', file=f)

            for ch, date, UTC in zip(m.chapter_list, m.release_date_list, m.release_date_UTC_list):
                print(ch, date, UTC, sep=', ', file=f)
            
def remove_most_recents(manga_dict):
    for manga_name in manga_dict:
        manga = manga_dict[manga_name]

        if len(manga.chapter_list) >= 2:
            manga.remove_entry()
        

def main():
    text_file = 'manga.txt'
    manga_dict = load_text_file(text_file)

    check_for_new_chapter(manga_dict, list(manga_dict.keys()))

    # TODO allow individual anime chapters to be read, currently only keeps track of single latest chapter
    max = 0
    for i in manga_dict:
        if len(manga_dict[i].chapter_list) > max:
            max = len(manga_dict[i].chapter_list)
    for i in range(max - 1):
        remove_most_recents(manga_dict)


    newest_chapters(manga_dict)


    write_text_file(text_file, manga_dict)



if __name__ == "__main__":
    main()


        
   
