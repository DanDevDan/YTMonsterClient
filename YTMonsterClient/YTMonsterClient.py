import requests
import json

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
        x=True
        while x == True:
            response = self.session.get('https://www.ytmonster.net/api/exchangeView.php?type=likes').text
            responsejson = json.loads(response)
            if responsejson['error'] == True:
                pass
            else:
                videoID = responsejson['url']
                x = False
        return videoID
