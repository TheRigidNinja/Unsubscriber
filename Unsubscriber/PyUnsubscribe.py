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
import math


 def channel(mode,data):
     file = open("channel.json","r+")
    
     if mode == "read":
         return json.loads(file.read())

     elif mode == "write":
         fileWrite = open("channel.json","w")
         fileWrite.write(json.dumps(data))

     elif mode == "update":
         fileWrite = file.write(json.dumps(data))


 # Image grab ------------------------------##
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

     # Gey the image ------------------------------##
     if GrayScale == True:
         image = cv2.imread('TruckPoints/Main.jpeg')
         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
         cv2.imwrite('TruckPoints/Main.jpeg',gray_image)

 # Read text from Images ------------------------------##
 def imgText(img):
     return pytesseract.image_to_string(Image.open("TruckPoints/Main.jpeg"))


 # Returns Coordnates for template images ------------------------------##
 GmailH,GmailW,GmailX,GmailY = 0,0,0,0
 ScreenPos = [[0],[]]
 screensize = 0

 def CoordnatesActions(TemplateImg,Offset,Screensize):
     global GmailH,GmailW,GmailX,GmailY

     ChromeActive = True
     coordnates = []

     if TemplateImg != "Standby":
          if TemplateImg == "Unsubscribe" and ScreenPos[0]:
              Screenshot(GmailX,GmailY,GmailW,ScreenPos[0][0],True)
          elif TemplateImg == "Block" and ScreenPos[1]:
               Screenshot(ScreenPos[1][0],ScreenPos[1][1],ScreenPos[1][2],ScreenPos[1][3],True)
          else:
              Screenshot(GmailX,GmailY,GmailW,GmailH,True)
              img_rgb = cv2.imread("TruckPoints/Main.jpeg")
              img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
              template = cv2.imread("TruckPoints/"+TemplateImg+".jpeg",0)
              w, h = template.shape[::-1]
              res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
              threshold = 0.8
              loc = np.where( res >= threshold)

         for pt in zip(*loc[::-1]):
             xpos = int((Screensize[0]+pt[0])+Offset[0]+GmailX)
             ypos = int(pt[1]+Offset[1])
             ChromeActive = False

             coordnates.append((xpos,ypos))
             if TemplateImg == "GmailHome":
                 GmailX = pt[0]-120
                 GmailH = pt[1]+35
             elif TemplateImg == "DetectEdge":
                 GmailW = pt[0]+55
                  ScreenPos[0][0] = GmailH/2
                  ScreenPos[0][1] = GmailH/2
              elif TemplateImg == "Block":
                  ScreenPos[1][0] = 0
                  ScreenPos[1][1] = 0
                  ScreenPos[1][2] = 0
                  ScreenPos[1][3] = 0

             if TemplateImg in ["Identify","GmailHome","DetectEdge","Unsubscribe","Unsubscribe2"]:
                 break
     else:
         ChromeActive = False
         coordnates.append((0,0))

     if ChromeActive == True and TemplateImg in ["Identify","GmailHome","DetectEdge",]:
         return "Chrome",False
     elif ChromeActive == True:
         return "TemplateImg Issue",False
     else:
         return coordnates,True


 backCoord = [0,0]
 inboxScroll = 0
 
 #Mouse actions / events ------------------------------##
 def MouseAction(Type,xpos,ypos):
     duration = 0.5

     if Type == "Click":
         ctypes.windll.user32.SetCursorPos(xpos,ypos)
         sleep(duration)
         pyautogui.click()

     if Type == "Select":
         ctypes.windll.user32.SetCursorPos(xpos-445,ypos)
         pyautogui.click()

     if Type == "SelectAll":
         ctypes.windll.user32.SetCursorPos(xpos,ypos)
         pyautogui.click()

     if Type == "Inspect":
         sleep(2)
         ctypes.windll.user32.SetCursorPos(xpos,ypos)

     if Type == "Scroll":
         ctypes.windll.user32.mouse_event(0x0800, 0, 0, -15000, 0)

     if Type == "ScrollInbox":
         print(inboxScroll)
         ctypes.windll.user32.mouse_event(0x0800, 0, 0, -inboxScroll, 0)
         Screenshot(0,0,0,0,True)

     if Type == "GoBack":
         ctypes.windll.user32.SetCursorPos(backCoord[0],backCoord[1])
         sleep(duration)
         pyautogui.click()

     if Type == "Delete":
         ctypes.windll.user32.SetCursorPos(backCoord[0]+150,backCoord[1])
         pyautogui.click()
         sleep(2)

     if type(Type) == dict:
         pyautogui.tripleClick()
         pyautogui.hotkey("backspace")
         sleep(duration)
         pyautogui.typewrite(Type["Write"])
         pyautogui.hotkey("enter")

     if Type == "Unsubscribe":
         res = CoordnatesActions("Unsubscribe",[30,0],screensize)
         if res[1] == True:
             ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
             pyautogui.click()

             res = CoordnatesActions("Unsubscribe2",[150,25],screensize)
             if res[1] == True:
                 ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
                 sleep(duration)
                 pyautogui.click()

                 res = CoordnatesActions("Identify",[5,5],screensize)
                 if res[1] == True:
                     ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
                     pyautogui.click()
                 else:
                     return res[1]
             else:
                 return res[1]
         else:
             return res[1]

     if Type == "Block":
         res = CoordnatesActions("Block",[95,5],screensize)
         if res[1] == True:
             ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
             pyautogui.click()

             res = CoordnatesActions("Block2",[95,5],screensize)
             if res[1] == True:
                 ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
                 pyautogui.click()

                 res = CoordnatesActions("Block3",[120,10],screensize)
                 if res[1] == True:
                     ctypes.windll.user32.SetCursorPos(res[0][0][0],res[0][0][1])
                     pyautogui.click()
                     Screenshot(0,0,0,0,True)
                 else:
                     return res[1]
             else:
                 return res[1]
         else:
             return res[1]

     if Type == "DeleteAll":
         ctypes.windll.user32.SetCursorPos(backCoord[0]+10,backCoord[1])
         pyautogui.click()
         ctypes.windll.user32.SetCursorPos(backCoord[0]+150,backCoord[1])
         pyautogui.click()
         sleep(duration)

     if Type == "EndScroll":
         res = CoordnatesActions(Type,[95,5],screensize)
         if res[1] == True:
             return "Next"
         else:
             return res[1]

     if Type == "nextPage":
         res = CoordnatesActions(Type,[95,5],screensize)
         if res[1] == True:
             ctypes.windll.user32.SetCursorPos(res[0][0][0]-100,res[0][0][1]+10)
             pyautogui.click()
             return "End"
         else:
             return res[1]

     if Type == "Trash":
         ctypes.windll.user32.SetCursorPos(backCoord[0]+150,backCoord[1])
         pyautogui.tripleClick()
         pyautogui.hotkey("backspace")
         sleep(duration)
         pyautogui.typewrite(Type["Write"])
         pyautogui.hotkey("enter")

 # Opens Gmail and perform actions ------------------------------##
 def Pyunsubscribe():
     global screensize , backCoord,inboxScroll

     rules = channel("read",0)

     select = ""
     scroll = "ScrollInbox"
     
     if rules["Workplace"]["Delete"] !="":
         select = "Select"
         scroll = ""
     
#     Giving program instructions ------------------------------##
     Tasks = {
         "Identify":{"Action":["Click"],"Offset":[5,5],"Reiterate":0},
         "GmailHome":{"Action":["None"],"Offset":[0,0],"Reiterate":0},
         "DetectEdge":{"Action":["None"],"Offset":[0,0],"Reiterate":0},
         "Search":{"Action":["Click",{"Write":rules["Workplace"]["Selector"]}],"Offset":[100,-50],"Reiterate":0},
         "GetLink":{"Action":["Click","Unsubscribe",rules["Workplace"]["Block"],"GoBack",select],"Offset":[450,0],"Reiterate":2},
         "Standby":{"Action":[rules["Workplace"]["Delete"]],"Offset":[450,0],"Reiterate":0},
         "GetLink#1":{"Action":["Inspect",scroll],"Offset":[0,0],"Reiterate":0},
         }

     Tasks2 = {
         "Search2":{"Action":["Click",{"Write":rules["Workplace"]["Trash"]}],"Offset":[100,-50],"Reiterate":0},
         "Trash":{"Action":["Click"],"Offset":[50,0],"Reiterate":0}
         }

     # Correct screensize Capture ------------------------------##
     user32 = ctypes.windll.user32
     screensizeMulti = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
     screensizeSingle = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
     if(np.array_equal(screensizeMulti, screensizeSingle)):
         screensize = (0,0)
     else:
         screensize = (screensizeSingle[0]-screensizeMulti[0],screensizeSingle[0]-screensizeMulti[1])


     # Task Compiler ------------------------------##
     filterAction = []
     LoopStopper = True
     Chrome = False
     elapse = 0
     OperationDone = False
     ScrollEnd = 0

     while LoopStopper:
         print(Tasks)
         #  Tracks number of time this loop as undergon ------------------------------##
         elapse+=1
         if elapse > 8:
             if rules["Workplace"]["Trash"] != "" and LoopStopper == True:
                 Tasks = Tasks2
                 elapse = 0
                 LoopStopper = False

             if OperationDone == True:
                 channel("write",{"Activity":"Finished","Progress":100})
                 return "Finished!"
             else:
                 channel("write",{"Activity":"Failed","Progress":100})
                 return "Some Function Failed!"

         elif elapse > 1:
             print("Sleep active",elapse)
             sleep(8/2-elapse/2)

         # Start compiling Tasks ------------------------------##
         for task in Tasks:
             if task not in filterAction:
                 holdTask = task
                 if "#" in task:
                     task = task[:task.index("#")] # Incase we have multiple tasks of the same thing ------------------------------##

                 if task in ["Search","Identify","GmailHome","DetectEdge","Search2"]: #Filter those action from taking place again ------------------------------##
                     filterAction.append(holdTask)

                 response = CoordnatesActions(task,Tasks[task]["Offset"],screensize)
                 task = holdTask

                 #  Start new tab if can't find gmail tab ------------------------------##
                 if (response[1] == False and response[0] == "Chrome") and Chrome == False:
                     print("Chrome Gmail tab was not detected!")
                     print("Lunching Tab...")
                     webbrowser.open_new_tab("https://mail.google.com/")
                     Chrome = True
                     break

                 # If all fails the followings stops the loop ------------------------------##
                 elif (response[1] == False and response[0] == "Chrome") and elapse >= 7:
                     LoopStopper = False
                     print("Problem Detected, Stopping Loop...")
                     return "Time Out! Please Open up your Gmail Account and Try again!"

                 # fires when can't detect template image on the current screenshot
                 elif response[0] == "TemplateImg Issue":
                     print("Failed")
                     Chrome = True
                     break

                 # Works when can't see the whole gmail tab
                 elif response[1] == False:
                     if  elapse <= 1:
                         LoopStopper = True
                     else:
                         LoopStopper = False
                         print("Cannot see the whole Chrome window")

                     Chrome = True
                     break

                 # Process mouse actions
                 elif response[1] == True:
                     Chrome = True
                     elapse = 0

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
                                 backCoord[0] = xpos-100
                                 backCoord[1] = ypos+50

                     if list(Tasks)[len(list(Tasks))-1] == task:
                         if MouseAction("EndScroll",0,0) != False:
                             if ScrollEnd == 1 and rules["Workplace"]["Trash"] != "":
                                 Tasks = Tasks2
                             elif ScrollEnd == 2:
                                 print("KIll")
                                 LoopStopper = False

                             ScrollEnd+=1
                         else:
                             OperationDone = True

 Pyunsubscribe()
 # Screenshot(0,0,0,0,True)
