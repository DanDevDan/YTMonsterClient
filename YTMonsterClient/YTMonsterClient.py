import requests
import json
import lxml.html

class YTMonsterClient():
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.session = requests.Session()

        payload = {
            'usernames':self.username,
            'passwords':self.password,
        }
        self.session.post('https://www.ytmonster.net/login?login=ok', data=payload)
        self.r = self.session.get('https://www.ytmonster.net/campaigns/new')
        if 'Dashboard' in self.r.text:
            self.loggedin = True
        else:
            self.loggedin = False

    def get_like_video_from_exchanges(self):
        if self.loggedin:
            pass
        else:
            raise Exception('Client failed to connect to the specified YTMonster account.')
        x = True
        while x:
            response = self.session.get('https://www.ytmonster.net/api/exchangeView.php?type=likes').text
            responsejson = json.loads(response)
            if responsejson['error'] == True:
                pass
            else:
                videoID = responsejson['url']
                x = False
        return videoID

    def get_channel_from_exchanges(self):
        x = True
        while x:
            response = self.session.get('https://www.ytmonster.net/api/exchangeView.php?type=subscribers').text
            responsejson = json.loads(response)
            if responsejson['error'] == True:
                pass
            else:
                channelid = responsejson['url']
                x = False

        return channelid

    def get_stats(self):
        """Returns a dictionary of user-individual statistics."""
        dashboard = self.session.get('https://www.ytmonster.net/dashboard')
        doc = lxml.html.fromstring(dashboard.content)
        credits = doc.xpath('/html/body/div[2]/div/div[2]/div[3]/div/div[1]/div[1]/div[1]/div/div[2]/div/text()')
        credits = int(credits[0].replace(r'\xa', '').replace(',', ''))
        membership = doc.xpath('/html/body/div[2]/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div/text()')
        membership = membership[0].replace(u'\xa0', u' ').replace(' ', '')
        return {'membership': membership, 'credits': credits}