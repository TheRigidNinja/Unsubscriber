import json
from time import sleep
import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import image_to_string
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
import win32gui, win32ui, win32con, win32api,ctypes
import pyautogui
import webbrowser

# Image grab
def Screenshot(x,y,wdth,hght,GrayScale):
	width = wdth
	height = hght
	left = x-1440
	top = y

	hwin = win32gui.GetDesktopWindow()
	if wdth == 0:
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
	if hght == 0:
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
	if x == 0:
		left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
	if y == 0:
		top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
	bmp.SaveBitmapFile(memdc, 'TruckPoints/Main.jpeg');

	# Gey the image
	if GrayScale == True:
		image = cv2.imread('TruckPoints/Main.jpeg')
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('TruckPoints/Main.jpeg',gray_image)

# Read text from Images
def imgText(img):
	return pytesseract.image_to_string(Image.open("TruckPoints/Main.jpeg"))


# Returns Coordnates for template images
GmailH,GmailW,GmailX,GmailY = 0,0,0,0
screensize = 0

def CoordnatesActions(TemplateImg,Offset,Screensize):
	ChromeActive = True
	coordnates = []
	
	Screenshot(GmailX,GmailY,GmailW,GmailH,True)

	img_rgb = cv2.imread("TruckPoints/Main.jpeg")
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	template = cv2.imread("TruckPoints/"+TemplateImg+".jpeg",0)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( res >= threshold)

	for pt in zip(*loc[::-1]):
		xpos = int((Screensize[0]+pt[0])+Offset[0])
		ypos = int(pt[1]+Offset[1])
		ChromeActive = False

		coordnates.append((xpos,ypos))

		if TemplateImg in ["Identify","GmailHome","DetectEdge","Unsubscribe","Unsubscribe2"]:
			break
		
	if ChromeActive == True and TemplateImg in ["Identify","GmailHome","DetectEdge",]:
		return "Chrome",False
	elif ChromeActive == True:
		return "TemplateImg Issue",False
	else:
		return coordnates,True


backCoord = [0,0]
inboxScroll = 0
#Mouse events
def MouseAction(Type,xpos,ypos):
	duration = 0.3

	if Type == "Click":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.SetCursorPos(xpos,ypos)
		pyautogui.click()

	if Type == "Select":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.SetCursorPos(xpos-445,ypos)
		pyautogui.click()

	if Type == "SelectAll":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.SetCursorPos(xpos,ypos)

	if Type == "Inspect":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.SetCursorPos(xpos,ypos)

	if Type == "Scroll":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.mouse_event(0x0800, 0, 0, -15000, 0)

	if Type == "ScrollInbox":
		print(Type,"-->")
		sleep(duration)
		ctypes.windll.user32.mouse_event(0x0800, 0, 0, -inboxScroll, 0)
		Screenshot(0,0,0,0,True)

	if Type == "GoBack":
		print(Type,"-->")
		ctypes.windll.user32.SetCursorPos(backCoord[0],backCoord[1])
		pyautogui.click()
		sleep(duration)

	if type(Type) == dict:
		print("Typing")
		pyautogui.tripleClick()
		pyautogui.hotkey("backspace")
		sleep(duration)
		pyautogui.typewrite(Type["Write"])
		pyautogui.hotkey("enter")
		sleep(1)

	if Type == "Unsubscribe":
		sleep(duration)
		print(Type,"-->")

		res = CoordnatesActions("Unsubscribe",[30,0],screensize)
		if res[1] == True:
			ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
			pyautogui.click()
			res = CoordnatesActions("Unsubscribe2",[150,25],screensize)
			ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
			pyautogui.click()
			res = CoordnatesActions("Identify",[5,5],screensize)
			ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
			pyautogui.click()

	if Type == "Block":
		sleep(duration)
		print(Type,"-->")
		res = CoordnatesActions("Block",[95,5],screensize)
		ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
		pyautogui.click()
		res = CoordnatesActions("Block2",[95,5],screensize)

		if res[1] == True:
			ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
			pyautogui.click()
			res = CoordnatesActions("Block3",[120,10],screensize)
			ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
			pyautogui.click()
			Screenshot(0,0,0,0,True)

	if Type == "DeleteAll":	
		print("SelectAll")
		res = CoordnatesActions("SelectAll",[95,5],screensize)
		ctypes.windll.user32.SetCursorPos(res[0][0][0]-95,res[0][0][1]+5)
		pyautogui.click()
		ctypes.windll.user32.SetCursorPos(res[0][0][0]-2,res[0][0][1]+5)
		pyautogui.click()

	if Type == "EndScroll":
		print("EndScroll Action")
		res = CoordnatesActions(Type,[95,5],screensize)

		if res[1] == True:
			return "Next"

	if Type == "nextPage":	
		res = CoordnatesActions(Type,[95,5],screensize)
		ctypes.windll.user32.SetCursorPos(res[0][0][0]-100,res[0][0][1]+10)
		pyautogui.click()
		return "End"

# Opens Gmailmail and perform actions
def Pyunsubscribe(Email,Rules):
	global screensize , backCoord,inboxScroll
	
	Tasks = {
		"Identify":{"Action":["Click"],"Offset":[5,5],"Reiterate":0},
		"GmailHome":{"Action":["None"],"Offset":[0,0],"Reiterate":0},
		"DetectEdge":{"Action":["None"],"Offset":[0,0],"Reiterate":0},
		# # "Search":{"Action":["Click",{"Write":"in:inbox -in:starred"}],"Offset":[400,20],"Reiterate":0},
		"Search":{"Action":["Click",{"Write":""}],"Offset":[400,20],"Reiterate":0},
		"GetLink":{"Action":["Click","Unsubscribe","Block","GoBack"],"Offset":[450,0],"Reiterate":"All"},
		"GetLink#1":{"Action":["DeleteAll"],"Offset":[450,0],"Reiterate":0},
		}

	# Correct screensize Capture ------------------------------##
	user32 = ctypes.windll.user32
	screensizeMulti = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
	screensizeSingle = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	if(np.array_equal(screensizeMulti, screensizeSingle)):
		screensize = (0,0)
	else:
		# screensize = (0,0)
		screensize = (screensizeSingle[0]-screensizeMulti[0],screensizeSingle[0]-screensizeMulti[1])


	# Task Compiler ------------------------------##
	LoopStopper = True
	Chrome = False
	elapse = 0
	while LoopStopper:
		elapse+=1

		if elapse > 1:
			print("Sleep active",elapse)
			sleep(8/2-elapse/2)
			if elapse >= 3 and Chrome == True:
				print("Finished")
				return "Some Function Failed"

		for task in Tasks:
			holdTask = task
			if "#" in task:
				task = task[:task.index("#")]

			response = CoordnatesActions(task,Tasks[task]["Offset"],screensize)
			task = holdTask
			
			#  Start new tab if can't find gmail tab
			if (response[1] == False and response[0] == "Chrome") and Chrome == False:
				print("Chrome Gmail tab was not detected!")
				print("Lunching Tab...")
				webbrowser.open_new_tab("https://mail.google.com/")
				Chrome = True
				break

			elif (response[1] == False and response[0] == "Chrome") and elapse >= 7:
				LoopStopper = False
				print("Problem Detected, Stopping Loop...")
				return "Time Out! Please Open up your Gmail Account and Try again!"

			elif response[0] == "TemplateImg Issue":
				print("Failed")
				Chrome = True
				break

			elif response[1] == False:
				if  elapse <= 1:
					LoopStopper = True
				else:
					LoopStopper = False
					print("Cannot see the whole Chrome window")

				Chrome = True
				break

			elif response[1] == True:
				Chrome = True
				elapse = 0

				# Mouse actions 
				if Tasks[task]["Reiterate"] == "All":
					Reiterate = len(response[0])
				else:
					Reiterate = Tasks[task]["Reiterate"]+1

				for event in range(0,Reiterate):
					for action in Tasks[task]["Action"]:
						xpos = response[0][event][0]
						ypos = response[0][event][1]
						MouseAction(action,xpos,ypos)

						if task == "GetLink" and inboxScroll == 0:
							inboxScroll = response[0][len(response[0])-1][1]-70

						if backCoord and task == "Search":
							backCoord[0] = xpos-190
							backCoord[1] = ypos

		if MouseAction("EndScroll",0,0) == "Next":
			MouseAction("nextPage",0,0)

				






Pyunsubscribe("Email","Rules")
# sleep(5)
# Screenshot(0,0,0,0,True)



