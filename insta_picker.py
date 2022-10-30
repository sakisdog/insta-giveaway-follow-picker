from datetime import datetime
from time import sleep
from requests import session
import requests
import random
from types import SimpleNamespace

def get_id(username,session):
	url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
	response = session.get(url)
	respJSON = response.json()
	try:
		for i in respJSON["users"]:
			if (i["user"]["username"] == username):
				return (i["user"]["pk"])
	except:
		return "Unexpected error"

session = requests.Session()
myusername = input("Enter your instagram username: ")
mypassw = input("Enter your instagram password: ")
usernametofetch = input("Enter the username of the user you want to fetch: ")
profileidtofetch = "18918467"
endcursor =""
hasnextpage = False
#Getting mid cookie
midurl = "https://i.instagram.com/api/v1/web/login_page/"

headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.79 Mobile Safari/537.36 Instagram 255.1.0.17.102",
  "X-Requested-With": "XMLHttpRequest",
  "X-Instagram-AJAX": "1",
  "Host": "www.instagram.com",
  "Origin": "https://www.instagram.com",
  "Accept-Language": "el,en;q=0.9"
}
session.headers.update(headers)
response = session.get(midurl)
csrftoken = response.cookies.get("csrftoken")
midtoken = response.cookies.get("mid")
igdidtoken = response.cookies.get("ig_did")
session.headers.update({"X-CSRFToken":csrftoken})
#Login
enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), mypassw)
login = session.post('https://www.instagram.com/accounts/login/ajax/',data={'enc_password': enc_password, 'username': myusername}, allow_redirects=True)
loginjson = login.json()
if "errors" in loginjson:
    print("Error: " + loginjson["errors"]["error"][0])
    exit()
#Get user id
profileidtofetch = get_id(usernametofetch,session)
if profileidtofetch == "Unexpected error":
    print(profileidtofetch)
    exit()
followersurl = "https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={\"id\":\""+profileidtofetch+"\",\"first\":50}"
count = 0
usernames = []
while True:
    request = session.get(followersurl)
    jsonresponse = request.json(object_hook=lambda d: SimpleNamespace(**d))
    followers = jsonresponse.data.user.edge_followed_by.edges
    if len(followers) < 1:
        print("No followers or error occured.")
        exit()
    for follower in followers:
        usernames.append(follower.node.username)
        print(follower.node.username)
    count += 50
    print("Got {0} of {1}".format(count,jsonresponse.data.user.edge_followed_by.count))
    if jsonresponse.data.user.edge_followed_by.page_info.has_next_page == True:
        endcursor = jsonresponse.data.user.edge_followed_by.page_info.end_cursor
        followersurl = "https://www.instagram.com/graphql/query/?query_hash=37479f2b8209594dde7facb0d904896a&variables={\"id\":\""+profileidtofetch+"\",\"first\":50,\"after\":\"" + endcursor + "\"}"
        sleep(1)
    else:
        break
if len(usernames) > 0:
    winner1 = usernames.pop(random.randrange(len(usernames)))
    print("Winner1 is: " + winner1)

# # Saving the winners in the winners.txt file
# file = open("winners.txt", 'w+')
# file.write(winner1 + "\n" + winner2 + "\n" + winner3)
