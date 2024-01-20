import base64
import hashlib
import json
import random
import requests
import tls_client
import time
import ua_generator
import uuid

config = json.load(open('./data/config.json', 'r'))
proxies = list(proxy.strip() for proxy in open('./data/proxies.txt', 'r').readlines())

def __get_proxy__() -> str | None:
    if len(proxies):
       return random.choice(proxies)
    
def __get_client_identifier__() -> str:
    return random.choice([
       'chrome_103',
       'chrome_104',
       'chrome_105',
       'chrome_106',
       'chrome_107',
       'chrome_108',
       'chrome_109',
       'chrome_111',
       'chrome_112',
       'chrome_117'
    ])

def __get_client__(random_tls_extension_order: bool = True) -> tls_client.Session:
    return tls_client.Session(random_tls_extension_order = random_tls_extension_order, client_identifier = __get_client_identifier__())

def __get_git_hash__() -> str:
    return __get_client__().get('https://www.guilded.gg', headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'guilded.gg',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1'
    }).text.split('id="bundle" src="')[1].split('/')[1]

git_hash = __get_git_hash__()

class Client:
      def __init__(this, proxy: str | None = None) -> None:
          this.client_id = str(uuid.uuid4())
          this.agent = ua_generator.generate(device = ('desktop'), browser = ('chrome'))
          this.proxy = ({
              'http' : 'http://{}'.format(proxy),
              'https': 'http://{}'.format(proxy)} if proxy != None else None)
          this.client = __get_client__()
          if this.proxy:
             this.client.proxies.update(this.proxy)
          this.cookies = this.getCookies()

      def __construct_cookies__(this, cookies: tls_client.cookies.RequestsCookieJar) -> str:
          return ' '.join('{}={};'.format(cookie.name, cookie.value) for cookie in cookies)

      def __construct_headers__(this, headers: dict = {}) -> dict:
          return {
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.9',
             'sec-ch-ua': this.agent.ch.brands,
             'sec-ch-ua-mobile': this.agent.ch.mobile,
             'sec-ch-ua-platform': this.agent.ch.platform,
            **headers,
             'User-Agent': this.agent.text
          }
      
      def getCookies(this) -> tls_client.response.Response:
          return this.client.put('https://www.guilded.gg/api/data/event', headers = this.__construct_headers__({
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'DNT': '1',
             'guilded-client-id': this.client_id,
             'guilded-viewer-platform': this.agent.device,
             'Host': 'www.guilded.gg',
             'Origin': 'https://www.guilded.gg',
             'Referer': 'https://www.guilded.gg/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'X-Requested-With': 'XMLHttpRequest'
          }), json = {'data': [{
             'attributionSource': None,
             'browser': this.agent.browser.title(),
             'device': None,
             'eventName': 'ClientTiming',
             'eventSource': 'Client',
             'gitHash': git_hash,
             'measurment': 'Bundle evaluated',
             'time': round(time.time()) * 1000,
             'timing': random.randint(800, 900),
             'viewerAppType': 'None',
             'viewerPlatform': this.agent.device,
             'viewerSystemName': None
          }]})
      
      def signUp(this, email: str, password: str, name: str, full_name: str) -> tls_client.response.Response:
          return this.client.post('https://www.guilded.gg/api/users?type=email', headers = this.__construct_headers__({
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookies': this.__construct_cookies__(this.cookies.cookies),
             'DNT': '1',
             'guilded-client-id': this.client_id,
             'guilded-stag': str(this.cookies.cookies.get('guilded_ipah')),
             'guilded-viewer-platform': this.agent.device,
             'Host': 'www.guilded.gg',
             'Origin': 'https://www.guilded.gg',
             'Referer': 'https://www.guilded.gg/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'X-Requested-With': 'XMLHttpRequest'
          }), json = {'email': email, 'extraInfo': {'platform': this.agent.device}, 'fullName': full_name, 'name': name, 'password': password})
            
      def sendVerify(this, cookies: tls_client.cookies.RequestsCookieJar) -> tls_client.response.Response:
          return this.client.post('https://www.guilded.gg/api/email/verify', headers = this.__construct_headers__({
             'Accept': 'application/json, text/javascript, */*; q=0.01',
             'Connection': 'keep-alive',
             'Content-Type': 'application/json',
             'Cookies': this.__construct_cookies__(this.cookies.cookies) + ' ' + this.__construct_cookies__(cookies),
             'DNT': '1',
             'guilded-client-id': this.client_id,
             'guilded-viewer-platform': this.agent.device,
             'Host': 'www.guilded.gg',
             'Origin': 'https://www.guilded.gg',
             'Referer': 'https://www.guilded.gg/',
             'sec-fetch-dest': 'empty',
             'sec-fetch-mode': 'cors',
             'sec-fetch-site': 'same-origin',
             'X-Requested-With': 'XMLHttpRequest'
          }))
    
      def verifyEmail(this, verification_link: str, cookies: tls_client.cookies.RequestsCookieJar) -> tls_client.response.Response:
          return this.client.get(verification_link, headers = this.__construct_headers__({
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
              'Connection': 'keep-alive',
              'Cookie': this.__construct_cookies__(this.cookies.cookies) + ' ' + this.__construct_cookies__(cookies),
              'DNT': '1',
              'Host': 'www.guilded.gg',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'none',
              'sec-fetch-user': '?1'
          }))
