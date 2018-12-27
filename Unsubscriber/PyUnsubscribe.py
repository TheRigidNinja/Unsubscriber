from bs4 import BeautifulSoup
import imaplib, email, os
import json
import re


# AUthenticate To User account
def auth():
	userData = open("userData.json","r")
	jsonData = json.loads(userData.read())

	#logs into the users account
	con = imaplib.IMAP4_SSL("imap.gmail.com")
	con.login(jsonData["Email"],jsonData["Password"])

	userData.close()
	return con, jsonData["Workplace"]


def search(key,value):
	global payload

	result, data  = payload[0].search(None,key,'"{}"'.format(value))
	return data


def unsub_LinkFinder(text):

	words = ["unsubscribe","here","click"]
	if "unsubscribe" in (text.lower()):
		# gets link if unsub has it
		soup = BeautifulSoup(text, "html.parser")
		links = soup.findAll("a")
		soup = str(soup)
		adjust = ""

		for href in reversed(range(0,len(links))):
			if href == len(links)-1:
				href = 0
			elif href == len(links)-2:
				href = len(links)-1
			else:
				href+=1

			for x in range(0,2):
				hrefText = re.sub(r"\s+", "",(links[href].text).lower())

				try:
					print(str(links[href]["href"])[:50])
					if words[x] in hrefText and "unsubscribe" in soup[:re.search(r'('+str(links[href]["href"])[:50]+')', soup).start()]:
						return links[href]["href"]
				except Exception as e:
					return "Null"
	else:
		return "None"


def analyseEmail():
	payload = auth()

	# Deciding where i should work
	workArea = []
	linkStore = {"[Gmail]/Spam":[],"[Gmail]/All Mail":[],"Inbox":[]}

	if payload[1]["Inbox"] == "True":
		workArea.append("Inbox")

	if payload[1]["Spam"] == "True":
		workArea.append("[Gmail]/Spam")

	if payload[1]["All_Mail"] == "True":
		workArea.append("[Gmail]/All Mail")


	for task in workArea:
		payload[0].select(task)
		status, data  = payload[0].search(None, 'ALL')
		cnt = 0

		for msgId in reversed(data[0].split()):
			linkStore[task].append(unsub_LinkFinder(str(payload[0].fetch(msgId, '(RFC822)'))))
				# break

	return linkStore

print(analyseEmail())


print(len(str("asd")) > 100)






