import pygame
import time
import pyautogui
import json
import threading
from win32api import GetSystemMetrics
import platform
from psutil import virtual_memory
import math


joysticks = []
pygame.init()
counter = 0
running = True
moveBy = 5
memory = virtual_memory()


debug_array = [False,False,False]
pyautogui.FAILSAFE = False

#print(mouse_pos[1])

try:
  with open("config.json") as js:
    data = json.load(js)
    #print(data)
    

    for key in data.keys():
      try:
        if data[key][0]['bool'] == True:
          debug_array[counter] = True
          
      except Exception as e:
        print(e)
      counter += 1
except Exception as e:
  print("Possible error, no file found. Program return error {}".format(e))

   
    

#print(debug_array)

for i in range(0, pygame.joystick.get_count()):
  joysticks.append(pygame.joystick.Joystick(i))
  joysticks[-1].init()
  
  if pygame.joystick.get_init() == True :
    print("\n\nDetected controller: {}\n\n".format(joysticks[i-1].get_name()))
    running = True

  else:
    print("No input device detected\n\n")


if len(joysticks) > 0:
  chosen = data['controller'][0]['device_num']
  print(chosen)
  if type(chosen) != int:
    #print("A number was expected. Program ended.\n\n")
    running = False

  try:
    print(joysticks[chosen])
  except Exception as e:
    print("The number chosen was out of the range of input devices in this computer. Program ended.\n\n")
    running = False
    exit()
else:
  chosen = 0

current_joy = pygame.joystick.Joystick(chosen)
clock = pygame.time.Clock()
mouse_pos = [0,0]


def info():
  pyautogui.alert("D-Pad buttons move the mouse accordingly\n\nX/A clicks the mouse\n\n\O/B brings up this info page\n\nSquare/X moves the mouse to the center of the screen\n\nThe left shoulder button decreases how much the mouse moves by 2.5\n\nThe right shoulder button increases how much the mouse moves by 2.5\n\nThe left stick being clicked in decreases how much the mouse moves by 12.5\n\nThe right stick being clicked in moves the mouse by 12.5\n\nThe select button quits the program\n\nThe start button shows the stats window","Info/Help")

def stat_info():
  pyautogui.alert("Mouse move by rate: {}\n\nWindow resolution: {}x{}\n\nProcessor Model: {}\n\nPhysical RAM: {}\n\nOperating system: {}".format(moveBy,GetSystemMetrics(0)
                                                                                    ,GetSystemMetrics(1),platform.processor(),memory.total,
                                                                                                             platform.system()),"Stats")
  

while running:

  mouse_pos_tup = pyautogui.position()

  mouse_pos[0] = mouse_pos_tup[0]
  mouse_pos[1] = mouse_pos_tup[1]
  clock.tick(60)


  if debug_array[0]:
    for event in pygame.event.get():
      if event.type == pygame.JOYBUTTONDOWN:
        print("Input detected from device {}".format(current_joy.get_name()),"Button ID: {}".format(event.button))

  elif debug_array[1]:
    for event in pygame.event.get():
      if event.type == pygame.JOYAXISMOTION:
        if event.axis >= 3:
          print("Input detected from {} ".format(current_joy.get_name()),"Stick type ID: {} ".format(event.axis),"Right stick detected!")
          time.sleep(0.5)
        elif event.axis <=2:
          print("Input detected from {} ".format(current_joy.get_name()),"Stick type ID: {} ".format(event.axis),"Left stick detected!")
          time.sleep(0.5)

  elif debug_array[2]:
    for event in pygame.event.get():
      if event.type == pygame.JOYHATMOTION:
        
        if current_joy.get_hat(0) == (0, 1):
            print("DPad is Up")
        elif current_joy.get_hat(0) == (0, -1):
            print("DPad is Down")
        elif current_joy.get_hat(0) == (-1, 0):
            print("DPad is Left")
        elif current_joy.get_hat(0) == (1, 0):
            print("DPad is Right")
          


  else:
    for event in pygame.event.get():
      if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0:
          pyautogui.click()

        elif event.button == 1:
          threading.Thread(target=info).start()

        elif event.button == 2:
          mouse_pos[0] = GetSystemMetrics(0) / 2
          mouse_pos[1] = GetSystemMetrics(1) / 2
          pyautogui.moveTo(mouse_pos[0],mouse_pos[1])

        elif event.button == 3:
          pyautogui.rightClick()

        elif event.button == 4:
          moveBy -= 2.5

        elif event.button == 5:
          moveBy += 2.5

        elif event.button == 6:
          pygame.quit()
          exit()

        elif event.button == 7:
          threading.Thread(target=stat_info).start()
          
        elif event.button == 8:
          moveBy -= 12.5
          
        elif event.button == 9:
          moveBy += 12.5

        elif event.button == 10:
          threading.Thread(target=info).start()
         
        



      if event.type == pygame.JOYHATMOTION:
        if current_joy.get_hat(0) == (0, 1):
            mouse_pos[1] =  mouse_pos[1] - moveBy
            pyautogui.moveTo(mouse_pos[0],mouse_pos[1])
            #print(mouse_pos)
            
        elif current_joy.get_hat(0) == (0, -1):
            mouse_pos[1] =  mouse_pos[1] + moveBy
            pyautogui.moveTo(mouse_pos[0],mouse_pos[1])
            #print(mouse_pos)
            
        elif current_joy.get_hat(0) == (-1, 0):
            mouse_pos[0] =  mouse_pos[0] - moveBy
            pyautogui.moveTo(mouse_pos[0],mouse_pos[1])
            #print(mouse_pos)
            
        elif current_joy.get_hat(0) == (1, 0):
            mouse_pos[0] =  mouse_pos[0] + moveBy
            pyautogui.moveTo(mouse_pos[0],mouse_pos[1])
            #print(mouse_pos)

      #if event.type == pygame.JOYAXISMOTION:
        #if event.axis >=3:
          #if event.value < 0.5 and event.value > -0.2:
            #mouse_pos[0] =  mouse_pos[0] + moveBy
            #pyautogui.moveTo(mouse_pos[0],mouse_pos[1])
          #time.sleep(0.32)
        #elif event.axis <=2:
          #print("Left stick value: {}".format(event.value))
          #time.sleep(0.5)

        

