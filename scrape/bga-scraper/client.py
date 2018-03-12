import requests

class UnexpectedHTTPStatusCode(IOError):
    pass

class HttpClient:
  baseurl = "https://en.boardgamearena.com/"
  gameId = 43 # yes, Quoridor!
  perPage = 100

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.session = requests.Session()

  def login(self):
    url = self.baseurl + "account/account/login.html"
    params = {
      'email': self.username,
      'password': self.password,
      'rememberme': 'on',
      'form_id': 'loginform',
    }

    response = self.session.post(url, params, allow_redirects=False)
    if response.status_code != 200:
      raise UnexpectedHTTPStatusCode(response.status_code)

  def getGameList(self, timestamp):
    url = self.baseurl \
      + "/message/board?type=lastresult&id=" + str(self.gameId) \
      + "&social=false&per_page=" + str(self.perPage) \
      + "&from_time=" + str(timestamp) \
      + "&from_id=1"
    response = self.session.get(url)

    if response.status_code != 200:
      raise UnexpectedHTTPStatusCode(response.status_code)

    return response.text

  def getPage(self, url):
    url = self.baseurl + url
    response = self.session.get(url)

    if response.status_code != 200:
      raise UnexpectedHTTPStatusCode(response.status_code)

    return response.text

  def getGameInfo(self, gameId):
    return self.getPage("/gamereview?table=" + str(gameId) + "&refreshtemplate=1")
