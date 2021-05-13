import requests
from bs4 import BeautifulSoup as bs
import re, os


URL = 'https://all-drawings.livejournal.com/calendar'

this_year = URL.replace('calendar', '2021')

LJ_NAME = re.search('://(.*).live', URL).group(1)

home = 'G:/Desktop/py/lj/' + LJ_NAME + '/'

print(home)

lj_text = home + LJ_NAME + '.txt'
links_by_month = home + LJ_NAME + '_get_posts_by_month.txt'
all_posts = home + LJ_NAME + '_all_posts.txt'

if not os.path.exists(home):
    os.mkdir(home, mode=0o777)



class LJ:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)



    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass



    def get_years(self):
        soup = self.get_soup()

        years = [_['href'] for _ in soup.find('ul', class_='year').find_all('a')]
        # append 2021 year
        years.append(this_year)

        return years
            


    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('div', class_='asset-content'):
                post = month.find_all('a')
                for _ in post:
                    if 'View Subjects' in _.text:
                        print(_.get('href'))
                        links_by_month_.write(_.get('href') + '\n')

        links_by_month_.close()



    def get_all_posts(self):

        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            for post in soup.find_all('dd', class_='viewsubjects'):
                post = post.find_all('a')

                print(post[2]['href'])

                posts_.write(post[2]['href'] + '\n')

        posts_.close()



    def save_lj(self):

        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())

            title = soup.find('h1', class_='b-singlepost-title').text.strip()
            link = _.strip()
            text = soup.find('article', class_='b-singlepost-body').get_text()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')

            print(link.strip())
            print(title.strip())
            
        lj_.close()










class LJ2:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass


    def get_years(self):
        soup = self.get_soup()

        years = [_['href'] for _ in soup.find('ul', class_='j-years-nav').find_all('a')]
        # append 2020 year
        years.append(this_year)

        return years
            

    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('div', class_='j-calendar-month'):
                _ = month.a['href']
                links_by_month_.write(_ + '\n')

        links_by_month_.close()


    def get_all_posts(self):
        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            for post in soup.find_all('a', class_='j-day-subject-link'):
                print(post['href'])
                posts_.write(post['href'] + '\n')

        posts_.close()


    def save_lj(self):

        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())

            try:
                title = soup.find('h1', class_='b-singlepost-title').text.strip()
            except AttributeError:
                title = 'No subject'
            
            link = _.strip()
            text = soup.find('article', class_='b-singlepost-body').get_text()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            
            print(link)
            
        lj_.close()







class LJ3:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass


    def get_years(self):
        soup = self.get_soup()
        years = []

        for _ in soup.find('div', attrs={'class': 'entry-text'}).ul.find_all('a'):
            match = re.search('\d\d\d\d', str(_))
            if match:
                years.append(_['href'])

        return years
            

    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:

            match = re.search('\d\d\d\d', year).group(0)
            
            if int(match) < 2021: 
                soup = self.get_soup(year)
                posts_by_month = soup.find_all('div', class_='calendar-wrap')
                
                for _ in posts_by_month:
                    print(_.a['href'])
                    links_by_month_.write(_.a['href'] + '\n')
        
        links_by_month_.close()


    def get_all_posts(self):
        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            try:
                for post in soup.find('div', class_='entry-text').find_all('dd'):
                    post_urls = post.find_all('a')

                    for post_url in post_urls:
                        if "all-drawings" in post_url['href']:
                            print(post_url['href'])
                            posts_.write(post_url['href'] + '\n')
            except KeyError:
                pass                

        posts_.close()


    def save_lj(self):
        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())
            
            try:
                text = soup.find('dd', class_='entry-text').get_text()
            except:
                text = 'No text'
                print(text)

            try:
                title = soup.find_all('dt', class_='entry-title')[1].text
            except:
                title = 'No subject'

            try:
                date = soup.find('dl', attrs={'class': 'vcard author'}) \
                           .find('dd', class_='entry-date') \
                           .text
            except:
                date = 'No date'

            link = _.strip()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write(date + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')

            print(title)
            print(date)
            print(_)
            
        lj_.close()

    
    def download_images(self):
        from wget import download

        all_posts_ = open(all_posts, 'r').readlines()
        for _ in all_posts_:

            print('-' * 10)
            print(_.strip())
            print('-' * 10)

            soup = self.get_soup(_.strip())
            imgs = soup.find('div', class_='entry-content').find_all('img')
            
            artist_name = soup.find_all('dt', class_='entry-title')[1].text

            n = 0

            for i in imgs:
                try:
                    if n == len(imgs):
                        n = 0

                    link = i['src']
                    session = requests.Session()
                    img_r_ = session.get(link)
                    con = img_r_.content

                    file_name = home + f'{artist_name}_{n}.jpg'

                    outf = open(file_name, "wb")
                    outf.write(con)
                    outf.close()
                    print(f'Downloaded: {file_name}')

                    n += 1

                except Exception as e:
                    print(e)
                    break
                
    



lj = LJ3()
# print(lj.get_years())
# lj.get_posts_by_month()
# lj.get_all_posts()
lj.download_images()
# lj.save_lj()




















class LJ4:

    def __init__(self):
        if not os.path.exists(home):
            os.mkdir(home, mode=0o777)


    def get_soup(self, url=URL):
        try: 
            session = requests.Session()
            request = session.get(url)
            soup = bs(request.content, 'html.parser')

            return soup

        except Exception as e:
            print(e)
            pass


    def get_years(self):
        soup = self.get_soup()
        years = []

        for _ in soup.find('font', attrs={'size': '+1', 'face': 'Arial,Helvetica'}).find_all('a'):
            match = re.search('\d\d\d\d', str(_))
            if match:
                years.append(_['href'])

        return years
            

    def get_posts_by_month(self):
        years = self.get_years()

        links_by_month_ = open(links_by_month, 'w')

        for year in years:
            soup = self.get_soup(year)
            for month in soup.find_all('a'):
                if month.text == 'View Subjects':
                    print(month['href'])
                    links_by_month_.write(month['href'] + '\n')

        links_by_month_.close()


    def get_all_posts(self):
        months_ = open(links_by_month, 'r').readlines()
        posts_ = open(all_posts, 'w')
 
        for month in months_:
            soup = self.get_soup(month.strip())

            try:
                for post in soup.find('div', class_='subjectlist').find_all('a'):
                    post_url = post['href']
                    print(post_url)
                    posts_.write(post_url + '\n')
            except KeyError:
                pass                

        posts_.close()



    def save_lj(self):
        all_posts_ = open(all_posts, 'r').readlines()
        lj_ = open(lj_text, 'w', encoding='utf-8')
 
        for _ in all_posts_:
            soup = self.get_soup(_.strip())
            try:
                text = soup.find('div', class_='b-singlepost-bodywrapper').get_text()
            except AttributeError as e:
                print(e, end='\n\n\n')
                continue

            try:
                title = soup.find('h1', class_='b-singlepost-title entry-title p-name').text.strip()
            except AttributeError:
                title = 'No subject'
            
            link = _.strip()
            data = re.sub(r'<.*?>', '', text).strip()

            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write(title + '\n')
            lj_.write(link + '\n')
            lj_.write(data + '\n')
            lj_.write('=====================================================================' + '\n')
            lj_.write('=====================================================================' + '\n\n\n\n')
            
            
            print(title)
            # print(link)
            # print(data)
            print(_)
            
        lj_.close()


session = requests.Session()
request = session.get('https://all-drawings.livejournal.com/850760.html')
soup = bs(request.content, 'html.parser')

def download_img():
    img = soup.find('div', class_='entry-content').find_all('img')
    for i in img:
        print(i['src'])







