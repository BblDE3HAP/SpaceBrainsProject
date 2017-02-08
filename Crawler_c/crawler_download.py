from bs4 import BeautifulSoup
import requests
import gzip
import datetime
import urllib.parse
import urllib.robotparser
import re
import repository


class PageDowloader:
    error = None
    page = None

    def __init__(self, url):
        self.url = url

    def get_page(self):
        try:
            response = requests.get(self.url)
            if response.status_code == requests.codes.ok:
                if response.headers['Content-Type'] == 'application/octet-stream':
                    self.page = gzip.decompress(response.content)
                else:
                    self.page = response.text
            else:
                response.raise_for_status()
        except requests.exceptions.HTTPError:
            print('HTTPError!!!')
            self.error = 'httperror'
            # updatelastscandate(page['ID'])
            print(self.url)
            # continue
        except requests.exceptions.ConnectionError as err:
            self.error = 'connectionerror'
            print('Connetion Error ->', err)
            print(self.url)


def get_page(url):
    """
    :param url: Ссылка на скачиваемый ресурс/страницу
    :return: HTML странца скаченная по ссылке
    """
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        if response.headers['Content-Type'] == 'application/octet-stream':
            return gzip.decompress(response.content)
        else:
            return response.text
    else:
        response.raise_for_status()


def findsitestorank():
    """
    :return: Результат запроса к БД -> Список сайтов для обхода.
    """
    sitesrepository = repository.DbSiteReposytory()
    siteworker = repository.SiteRepositoryWorker(sitesrepository)
    result = siteworker.getsitestorank()
    return result


def writerobotstodb(sites):
    """
    :param sites: Список сайтов для обхода краулера
    Записываем для каждого сайта в pages ссылку на robots.txt
    """
    pagesrepository = repository.DbPageRepository()
    pagewoker = repository.PagesRepositoryWorker(pagesrepository)
    for site in sites:
        url = urllib.parse.urlunparse(('https', site['Name'], 'robots.txt', '', '', ''))
        page = repository.Page(Url=url, SiteID=site['ID'], FoundDateTime=datetime.datetime.today())
        pagewoker.writepagestostore(page)


def pagestowalk():
    """
    :return: Список страниц для обхода у которых двта последнего обхода пустая
    """
    pagesrepository = repository.DbPageRepository()
    pagewoker = repository.PagesRepositoryWorker(pagesrepository)
    result = pagewoker.getpagelastscandatenull()
    return result


def pagestowalk2():
    pagesrepository = repository.DbPageRepository()
    pagewoker = repository.PagesRepositoryWorker(pagesrepository)
    result = pagewoker.getallpages()
    return result


def whatisurl(url):
    """
    :param url: Ссылка для анализа, куда ведет
    :return: 'robots' или 'sitemap' в зависимости от того на что указывает ссылка.
    """
    parse = (urllib.parse.urlsplit(url))
    if parse.path.endswith('robots.txt'):
        return 'robots'
    elif parse.path.endswith('.xml') or parse.path.endswith('.xml.gz'):
        print(url)
        return 'sitemap'


def readrobots(file):
    """
    :param file: Файл robots.txt для аналза и извечения ссылки на  sitemap
    :return: Возвращает ссылку на sitemap
    """
    r = file.split('\n')
    for x in r:
        if x.startswith('Sitemap'):
            return x.split(':', maxsplit=1)[-1].strip()


def writeurl(url, siteid):
    """
    :param url: Ссылка для записи в БД
    :param siteid: ID сайта для которого записываем ссылку в БД
    :return:
    """
    pagesrepository = repository.DbPageRepository()
    pagewoker = repository.PagesRepositoryWorker(pagesrepository)
    print('Пишем url в БД')
    page = repository.Page(Url=url, SiteID=siteid, FoundDateTime=datetime.datetime.today())
    pagewoker.writepagestostore(page)


def updatelastscandate(pageid):
    """
    :param pageid:
    :return:
    """
    pagesrepository = repository.DbPageRepository()
    pagewoker = repository.PagesRepositoryWorker(pagesrepository)
    page = repository.Page(ID=pageid, LastScanDate=datetime.datetime.today())
    pagewoker.updatepageinstore(page)


def sitemapparse(html):
    """
    :param html: HTML страница sitemap для извлечения ссылок для дальнейшего обхода.
    :return: Список ссылок для записи в БД по которым необходимо совершать обход
    """
    soup = BeautifulSoup(html, 'lxml')
    st = [url.text for url in soup.find_all('loc')]
    return st


def countstat(html, word):
    """
    :param html: Страница для подсчета статистики.
    :param word: Слово по которому подсчитываем статистику
    :return: Количество раз упоминания слован на странице
    """
    soup = BeautifulSoup(html, 'lxml')
    c = r'\b{}\b'.format(word)
    w = re.compile(c)
    i = 0
    for string in soup.stripped_strings:
        if len(w.findall(repr(string))) > 0:
            i += len(w.findall(repr(string)))
    print('Rank ->', i)
    return i


def countstatforpage(html):
    """
    :param html: HTML страницы которую анализируем на предмет сколько раз встречается ключевые слова.
    :return: Словаь по персонам с ID персоны и статистика для проанализируемой странице
    """
    personrepository = repository.DbPersonRepository()
    personworker = repository.PersonRepositoryWorker(personrepository)
    keywordrepository = repository.DbKeywordRepository()
    keywordworker = repository.KeywordRepositoryWorker(keywordrepository)
    personslist = personworker.getpersons()
    personsdict = {}
    for person in personslist:
        lst = []
        keywordslist = keywordworker.getbypersonid(person['ID'])  # GetKeywordByPersonID
        for keyword in keywordslist:
            lst.append(countstat(html, keyword['Name']))
        s = sum(lst)
        personsdict[person['ID']] = s
    return personsdict


def writerank(personid, pageid, rank):
    """
    :param personid:
    :param pageid:
    :param rank:
    :return:
    """
    personpagerankrepository = repository.DbPersonPageRankRepository()
    personpagerankwoker = repository.PersonPageRankRepositoryWorker(personpagerankrepository)

    print('Пишем Rank в БД')
    personpagerank = repository.PersonPageRank(PersonID=personid, PageID=pageid, Rank=rank)
    personpagerankwoker.writeranktostore(personpagerank)


def geturlfrompage(url, html):
    soup = BeautifulSoup(html, 'lxml')
    alst = soup.select('a[href^="/"]')
    print('Количество ссылок -> ', len(alst))
    p = urllib.parse.urlparse(url)
    r = urllib.robotparser.RobotFileParser()
    rurl = urllib.parse.urlunparse((p.scheme, p.netloc, 'robots.txt', '', '', ''))
    robot = get_page(rurl)
    robot = robot.splitlines()
    r.parse(robot)
    print(p.netloc)
    hrefs = set()
    for link in alst:
        path = link['href'].split('?')[0]
        # print('PATH -> ', path)
        u = urllib.parse.urljoin(url, path)
        u1 = urllib.parse.urlparse(u)
        if p.netloc == u1.netloc:
            if r.can_fetch("*", u):
                # print(u)
                hrefs.add(u)
                # print(u1.netloc)
    # input('Нашли ссылки')
    print(len(hrefs))
    return hrefs


def main():
    # cn = db_connect()
    # cur = cn.cursor()

    while True:
        print('Находим сайты для обхода и записываем ссылку на robots.txt')
        sites = findsitestorank()
        writerobotstodb(sites)

        pages = pagestowalk()
        print('Страниц для обхода ->', len(pages))

        if len(pages) > 0:
            i = 0  # Cделал для отладки
            pagesnotinsitemap = set()
            for page in pages:
                p = PageDowloader(page['Url'])
                p.get_page()
                html = p.page
                if p.error is not None:
                    print(p.error)
                    if p.error == 'httperror':
                        print('HTTPError!!!')
                        updatelastscandate(page['ID'])
                        print(page)
                        continue
                    elif p.error == 'connectionerror':
                        print('Connetion Error ->')
                        print(page)
                        continue

                if (whatisurl(page['Url'])) == 'robots':
                    print('Записываем ссылку на sitemap в БД')
                    sitemapurl = readrobots(html)
                    writeurl(sitemapurl, page['SiteID'])
                    updatelastscandate(page['ID'])
                elif (whatisurl(page['Url'])) == 'sitemap':
                    print('Получаем ссылки из sitemap и записываем в БД')
                    urlstowrite = sitemapparse(html)
                    for url in urlstowrite:
                        print(url)
                        writeurl(url, page['SiteID'])
                        updatelastscandate(page['ID'])
                else:  # Страница для анализа.
                    print(page['Url'])

                    urlsfrompage = geturlfrompage(page['Url'], html)

                    print('Найденные сылки -> ', urlsfrompage)
                    print('Пересечение -> ', pagesnotinsitemap.intersection(urlsfrompage))

                    pagesnotinsitemap.update(urlsfrompage)

                    print('Новые ссылки {} -> {}'.format(len(pagesnotinsitemap), pagesnotinsitemap))

                    d = countstatforpage(html)
                    for pers, rank in d.items():
                        writerank(pers, page['ID'], rank)

                    updatelastscandate(page['ID'])
                i += 1  # Cделал для отладки
                print('Осталось обойти : {} страниц из {}'.format(len(pages) - i, len(pages)))  # Cделал для отладки
        else:
            break

    print(len(pagesnotinsitemap))
    print(pagesnotinsitemap)
    input('SECOND STAGE')

    # Наброски для версии 2.0
    pages = pagestowalk2()
    print(len(pages))
    t = datetime.timedelta(hours=24)
    for page in pages:
        if datetime.datetime.today() - page['LastScanDate'] > t:
            p = urllib.parse.urlparse(page['Url'])
            if (p.path[1:].startswith('sitemap')) and (p.path[1:].endswith('xml') or p.path[1:].endswith('xml.gz')):
                print(p.path[1:])
                print(datetime.datetime.today() - page['LastScanDate'])
                html = get_page(page['Url'])
                urlstowrite = sitemapparse(html)
                print(len(urlstowrite))
                lst = [x['Url'] for x in pages]
                for item in urlstowrite:
                    if item not in lst:
                        print(item)
                        writeurl(item, page['SiteID'])
                        updatelastscandate(page['ID'])
                        # s1 = set(urlstowrite)
                        # s2 = set([x['Url'] for x in pages])
                        # print(s2 - s1)

    # Наброски для версии 3.0
    '''
    pages = pagestowalk2()
    print(len(pages))
    newpagestowalk = set()
    for page in pages:
        html = get_page(page['Url'])
        if (whatisurl(page['Url'])) == 'robots' or (whatisurl(page['Url'])) == 'sitemap':
            continue
        else:
            print('Новые ссылки ->', newpagestowalk)
            urlsfrompage = geturlfrompage(page['Url'],  html)
            print('Найденные сылки -> ', urlsfrompage)
            print('Пересечение -> ', newpagestowalk.intersection(urlsfrompage))
            newpagestowalk.update(urlsfrompage)
            print('Новые ссылки {} -> {}'.format(len(newpagestowalk), newpagestowalk))
    '''

    repository.conn.close()


if __name__ == '__main__':
    main()
