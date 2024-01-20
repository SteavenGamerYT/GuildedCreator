import time
import json
import requests
import random

class Tempmail:
      def __init__(this, username: str, password: str, proxy: dict | None = None) -> None:
          this.proxy = proxy
          this.address = username.lower() + '@' + random.choice(this.__get_domains__())
          this.password = password
          this.creation = this.__create_email__()
          this.token = this.__get_token__().json().get('token')

      def __get_domains__(this, page: int = 1) -> list:
          return [domain['domain'] for domain in requests.get('https://api.mail.tm/domains?page={}'.format(page), proxies = this.proxy).json()['hydra:member']]

      def __create_email__(this) -> requests.Response:
          return requests.post('https://api.mail.tm/accounts', json = {'address': this.address, 'password': this.password}, proxies = this.proxy)

      def __get_token__(this) -> requests.Response:
          return requests.post('https://api.mail.tm/token', json = {'address': this.address, 'password': this.password}, proxies = this.proxy)

      def __get_messages__(this, page: int | str = 1) -> requests.Response:
          return requests.get('https://api.mail.tm/messages?page={}'.format(page), headers = {'Authorization': 'Bearer {}'.format(this.token)}, proxies = this.proxy)

      def __get_message_by_id__(this, message_id: str) -> requests.Response:
          return requests.get('https://api.mail.tm/messages/{}'.format(message_id), headers = {'Authorization': 'Bearer {}'.format(this.token)}, proxies = this.proxy)

      def __find_verification_link__(this, verification_attempts: int, verification_delay: int = 1.5) -> str | None:
          for attempt in range(verification_attempts):
              messages = this.__get_messages__().json()
              for message in messages['hydra:member']:
                  if message['subject'] == 'Verify your email on Guilded':
                     message = this.__get_message_by_id__(message['id']).json()
                     return message['html'][0].split('</div><a href="')[1].split('"')[0]
              time.sleep(verification_delay)
