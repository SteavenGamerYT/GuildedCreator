import threading
import time
from guilded.modules.console import Console
from guilded.modules.misc import __get_random_string__
from guilded.client import config, __get_proxy__, Client
from guilded.tempmail import Tempmail

console = Console()

class Sequence:
      def __start__(this) -> None:
          try:
            client = Client(__get_proxy__())

            email_username = __get_random_string__(7).lower()
            email_password = __get_random_string__(7).lower()

            tempmail = Tempmail(email_username, email_password, client.proxy)
            if tempmail.token:
               username = __get_random_string__(7)
               password = __get_random_string__(8) + '*'

               request = client.signUp(tempmail.address, password, username, config['full_name'] if config["full_name"] else __get_random_string__(5))
               if request.json().get('user'):
                  open('./data/output/accounts-session.txt', 'a+').write(f'{request.cookies.get("hmac_signed_session")}\n')
                  open('./data/output/accounts.txt', 'a+').write(f'{tempmail.address}:{username}:{password}:{request.cookies.get("hmac_signed_session")}\n')

                  console.__success__('Created Account: {} ({}**)'.format(tempmail.address, str(request.cookies.get('hmac_signed_session'))[:25]))
                  try:
                    verify = client.sendVerify(request.cookies)
                    if verify.status_code == 200:
                       console.__success__('Verification Link Sent ({}**)'.format(str(request.cookies.get('hmac_signed_session'))[:25]))

                       verifcation_link = tempmail.__find_verification_link__(config['verification_attempts'], config['verification_delay'])
                       if verifcation_link:
                          verification = client.verifyEmail(verifcation_link, request.cookies)
                          if verification.headers.get('Location') == 'https://www.guilded.gg/?emailVerified':
                             open('./data/output/accounts-verified-session.txt', 'a+').write(f'{request.cookies.get("hmac_signed_session")}\n')
                             open('./data/output/accounts-verified.txt', 'a+').write(f'{tempmail.address}:{username}:{password}:{request.cookies.get("hmac_signed_session")}\n')

                             console.__success__('Verified Email: {} ({}**)'.format(tempmail.address, str(request.cookies.get('hmac_signed_session'))[:25]))
                          else:
                             console.__failure__('Email Not Verified: {} ({}**)'.format(tempmail.address, str(request.cookies.get('hmac_signed_session'))[:25]))
                       else:
                           console.__failure__('Verification Link Not Found: {} ({}**)'.format(tempmail.address, str(request.cookies.get('hmac_signed_session'))[:25]))
                    else:
                       console.__failure__('Verification Email Not Sent: {} ({}**)'.format(tempmail.address, str(request.cookies.get('hmac_signed_session'))[:25]))
                  except Exception as E:
                         console.__unknown__('{}: {}'.format(type(E), str(E)))
               else:
                  console.__failure__('Account Not Created ({}:{})'.format(username, password))
            else:
                console.__failure__('Tempmail Not Created: {}'.format(tempmail.address))
          except Exception as E:
                 console.__unknown__('{}: {}'.format(type(E), str(E)))

def __main__():
    while 1:
       sequence = Sequence()
       sequence = sequence.__start__()
       time.sleep(config['thread_retry_delay'])

for thread in range(config['threads']):
    thread = threading.Thread(target = __main__)
    thread.start()
