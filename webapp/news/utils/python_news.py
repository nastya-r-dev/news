from datetime import datetime
from webapp.db import db
from webapp.news.models import New
import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except (requests.RequestException, ValueError):
        print('error!')
        return False


def get_python_news():
    html = get_html('https://76.ru/text/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_list = soup.find_all('article')
        for news in news_list:
            title = news.find('h2').text
            url = 'https://76.ru' + news.find('a')['href']
            date = news.find("div", {"class": "tzxtk"}).find('time')['datetime']
            img = news.find("picture", {"class": "_6zHZU oZtUo"}).find("img")['src']
            try:
                date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                date = datetime.now()
            html2 = get_html(url)
            article = 'Новость удалена'
            if html2:
                article = extract_article_content(html2)
            save_news(title, url, date, article, img)
    return False


def extract_article_content(html):
    """Извлекает и очищает содержимое статьи."""
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup():
        for attribute in ["style"]:
            del tag[attribute]
    article = soup.find('article', class_='article_dzCDV pb-6')

    if not article:
        return 'Новость удалена'

    # Список селекторов для удаления
    selectors_to_remove = [
        'span.d-flex.align-items-c',                             # Значки иконок
        'span.item_VmtHQ',
        'div.d-flex.articleSubHeader_HojKc.default_HojKc.mb-6',
        'img.stub_nZVrb',
        'div.sharing_ksvEQ.notFixed_ksvEQ',
        'div.wrapper_XGdnt.p-4',
        'div.reactions_FD88v.mt-6',
        'a.link_VmtHQ',                                          # Ссылки, которые заменим текстом
        'nav',                                                   # Навигационные блоки
        'footer',                                                # Подвал
        'ins',                                                   # Рекламные блоки
        'aside',                                                 # Боковые панели
        'section.comments',                                      # Комментарии
        'div.comments',                                          # Комментарии
        'meta',                                                  # Метаинформация
        'input',                                                 # Поля ввода
        'form',                                                  # Формы
        'iframe',                                                # Встроенные элементы
        'style',                                                 # Встроенные стили
        'script',                                                # Сценарии JavaScript
        'link[rel="stylesheet"]',                                # Стили
        'div.hidden',                                            # Скрытые элементы
        'span.hidden',                                           # Скрытые элементы
        'div.d-flex.articleSubHeader_J4nOY.default_J4nOY.mb-6',
        'div.wrapper_W7lmS',
        'div.articleAuthors_423ch.mt-6',
        'div.articleTags_5nnkh.mt-6',
        'div.articleRemarkAboutMistake_ilBSy'
    ]

    for selector in selectors_to_remove:
        tags_to_remove = article.select(selector)
        for tag in tags_to_remove:
            tag.decompose()

    # Замена ссылок на текст
    links = article.find_all('a', class_='link_VmtHQ')
    for link in links:
        new_tag = soup.new_tag("p")
        new_tag.string = link.text.strip()
        link.replace_with(new_tag)

    return article.decode_contents()


def save_news(title, url, date, text, img):
    check_news = New.query.filter(New.url == url).count()
    if not check_news:
        new_news = New(
            title=title,
            url=url,
            date=date,
            text=text,
            img=img
        )
        db.session.add(new_news)
        db.session.commit()


if __name__ == '__main__':
    get_python_news()
