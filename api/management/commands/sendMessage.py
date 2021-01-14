from api.models import AccessToken, Message
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse

class Command(BaseCommand):
    help = 'send msg'

    def lineNotifyMessage(self, token, msg):
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload
            )
        return r
    
    def send_pro(self, content, tokens):
        for token in tokens:
            status = self.lineNotifyMessage(token.token, content)
            if status.status_code == 401:
                token.delete()
            elif status.status_code != 200:
                return status
        return None

    def handle(self, *args, **kwargs):
        if len(Message.objects.all()) == 0:
            nowID = Message(stopID=15753)
        else:
            nowID = Message.objects.all()[0]
        tokens = AccessToken.objects.all()
        url = "http://www.ttsh.tp.edu.tw/module.php?i=news&cat_id=2&start=0"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        className = 'list-group-item'
        newsLists = soup.find_all('a', {'class': className})
        newsLists = newsLists[3:]
        for i in range(len(newsLists)):
            x, newsdict = newsLists[i], dict()
            newsdict['link'] = "http://www.ttsh.tp.edu.tw" + x['href'][1:]
            query = urlparse.urlsplit(newsdict['link']).query
            newsdict['id'] = int(urlparse.parse_qs(query)['news_id'][0])
            className = 'title'
            title = x.find('span', {'class': className})
            newsdict['title'] = title.get_text(strip=True)
            newsLists[i] = newsdict
        second = True
        newsLists.reverse()
        for x in newsLists:
            if x['id'] <= nowID.stopID:
                continue
            nowID.message = x['title']
            nowID.stopID = x['id']
            if second:
                tokens = AccessToken.objects.all()
                second = False
            status = self.send_pro(x['title']+"\n"+x['link'], tokens)
            if status is not None:
                print(status)
        nowID.save()
