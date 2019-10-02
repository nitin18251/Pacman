# pygame
## This a simple pacman game built using pygame module of python.
As for playing this game you need to download all the file and put it into a single place, and then run the main python file.  
As pygame doesnt have any inbuilt module to take input from user in the window thatswhy I have used a module available here- 
https://github.com/Nearoo/pygame-text-input/blob/master/pygame_textinput.py  
This is how the game looks when run for the first time.  
![screenshot from 2018-11-23 02-01-11](https://user-images.githubusercontent.com/44255731/48921425-b5bf9600-eec5-11e8-8e48-44cab3dd9894.png) ![screenshot from 2018-11-23 02-02-36](https://user-images.githubusercontent.com/44255731/48921426-b9ebb380-eec5-11e8-91ee-8cad642d50e8.png) ![screenshot from 2018-11-23 02-01-34](https://user-images.githubusercontent.com/44255731/48921428-bd7f3a80-eec5-11e8-96c8-613d1821194f.png)  
for using this module you need to have pygame,numpy modules of python installed.  
This game is built using pygame1.9.2 and numpy1.15.1  
## Instructions :  
1.On the very first window one can press either 's' key to start or mouse click on start button to start the game and can press 'q' or Exit button to quit the game.   
2.Next window is to enter username. after entering the username one has to press up arrow key to start the game.  
3.NOW the game has begun. The pacman will be placed randomly at some coordinate and with some initial random direction to move . you can use arrow keys to control his movement.  
4.There are some randomly generated coins all over the place and some black holes also.(RULE is that if you pass through balck hole 2 times then GAME OVER)  
5.you can reset or quit game anytime you want by using 'r' and 'q' keys repectively.   
6.Your's score with username and time will get written to a file details.txt(it will be created if doesn't exists)
