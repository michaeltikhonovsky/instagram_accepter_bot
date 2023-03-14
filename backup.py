'''
This code is not protected in any way
Feel free to do whatever you like with it
@michael.tikhonovsky
'''

import sys, os
from colorama import Fore
from InstagramAPI import InstagramAPI
from halo import Halo
import time, json
import replit
from colorama import init
init(autoreset=True)
username = ''
password = ''
number = 0
spinner = Halo(text='\nAccepted followers: ' + str(number), spinner='dots')

from contextlib import contextmanager

@contextmanager
def hide():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value

def getPendingFollowRequests(self):
  return self.SendRequest('friendships/pending?')

def approve(self, userId):
  data = json.dumps({'_uuid':self.uuid, 
   '_uid':self.username_id, 
   'user_id':userId, 
   '_csrftoken':self.token})
  return self.SendRequest('friendships/approve/' + str(userId) + '/', self.generateSignature(data))

def getPendingInfo(insta):
  idsUser = []
  if getPendingFollowRequests(insta):
    info = insta.LastJson
    for i in info['users']:
      idsUser.append(i['pk'])
    return (idsUser)

def usernameInput():
  username = input("Username:\n")
  return username

def passwordInput():  
  password = input("Password:\n")
  return password

replit.clear()

print('Instagram follow request accepter, get in touch with me at @michael.tikhonovsky if you have any questions\n')
print('<<<THIS IS A ' + Fore.GREEN + 'FREE' + Fore.RESET + ' ACCEPTER, IF YOU WERE CHARGED FOR THIS YOU HAVE BEEN SCAMMED>>>')
username = usernameInput()
password = passwordInput()
insta = InstagramAPI(username, password)

while insta.isLoggedIn == False:
  global select
  with hide():
    insta.login()
  try:
    if insta.LastJson['two_factor_required']:
      replit.clear()
      print(Fore.RED + 'Instagram Login has failed')
      print(Fore.RED + 'Two factor authentication error!')
      authID = insta.LastJson['two_factor_info']['two_factor_identifier']
      authcode = input('Please input SMS code here: \n')
      insta.finishTwoFactorAuth(authcode, authID)
  except:
    pass
  try:
    while 'challenge_required' in insta.LastJson['message']:
      replit.clear()
      print(Fore.RED + 'Instagram Login has failed')
      print(Fore.RED + 'Challenge required error!')
      print('Do one of these three things to sign in:')
      print(Fore.GREEN + '1 - Open the Instagram app and click "This was me" on the prompt')
      print(Fore.GREEN + '2 - Go to the following link and sign in')
      CHALLENGE = insta.LastJson['challenge']['url'] 
      print(CHALLENGE)
      print(Fore.GREEN + '3 - Get code from email (must have verified email linked to account)')
      print('\nIf you choose to do either of the first two, complete it and then press enter')
      select = input('If you choose to do the third option, type the number "3" and press enter\n')
      if select == 3:
        insta.get_id(username)
        insta.completeCheckpoint1()
        AUTHCODE = input('Enter code recieved from email: ')
        insta.completeCheckpoint2(AUTHCODE)
      with hide():
        insta.login
      if 'challenge_required' in insta.LastJson['message']:
        print(Fore.RED +'Challenge has not been resolved!')
        print(Fore.RED +'Please try again')
        time.sleep(2)
  except:
    pass
  if insta.isLoggedIn == False:
    replit.clear()
    print(Fore.RED + 'Instagram Login has failed.')
    username = usernameInput()
    password = passwordInput()
    insta = InstagramAPI(username, password)

replit.clear()
spinner.start()

while __name__ == '__main__':
  try:
    userid = getPendingInfo(insta)
  except:
    pass
  if userid:
    for check in range(150):
      try:
        currentUserID = userid[check]
        approve(insta, currentUserID)
        number += 1
        spinner.start('\nFollowers accepted: ' + str(number))
      except:
        pass