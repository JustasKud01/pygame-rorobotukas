# Importuojamos bibliotekos
from turtle import delay
import pygame
from sys import exit
import linecache
import pathlib
path = pathlib.Path(__file__).parent.resolve()

# Nustatomas žaidimo ekrano dydis, inicijuojama pygame biblioteka
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Dirbantis robotukas")
clock = pygame.time.Clock()
surface = pygame.display.get_surface()
x,y = size = surface.get_width(), surface.get_height()

# Nustatomos vidurinės pilkos linijos dydis, spalva
vertical = pygame.Surface((2, x))
horizontal = pygame.Surface((y, 2))
vertical.fill("gray"), horizontal.fill("gray")
vertical.set_alpha(128)

# Nustatoma žalių linijų spalva, dydis
verticalMin = pygame.Surface((2, 500))
horizontalMin = pygame.Surface((500, 2))
verticalMin.fill("green")
verticalMin.set_alpha(75), horizontalMin.set_alpha(75)

# nustatoma kiek pikselių yra viena koordinatė
cordSize = 20

# Aprašomi pradžios kintamieji naudojami vėliau
displayCord = [0, 0]
time_elapsed_since_last_action = 0
file_line_number = 0

moved_right = 0
moved_left = 0
moved_up = 0
moved_down = 0

verticalLine = 0;
horizontalLine = 0;
countPackage = 0


game = True
gameoverScreen = False
error = False

without_package = True
with_Package = False
batteryToMove = False

cordsLeft = []
batteryNeeded = 0


# Nustatoma kiek yra baterijos pradžioje ir kiek kainuoja vienas ėjimas
battery = 100
batteryCost = 1

# Nustatoma taško startinė ir pabaigos pozicija pikseliais, kad taškas grįžtų į vidurį (0,0 koordinates)
start_cord_x = x/2 - 5
start_cord_y = y/2 - 5

end_cord_x = x/2 - 5
end_cord_y = y/2 - 5

# Nustatoma taško spalva ir dydis
robot = pygame.Surface((10, 10))
robot.fill('Red')
# Priskiriamos startinės taško koordinatės
screen.blit(robot, (start_cord_x, start_cord_y))  

# Nustatomas "žaidimo" šriftas ir spalvos
font = pygame.font.Font('freesansbold.ttf', 32)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
# Nustatoma "žaidimo" favicon ikona viršuje kairėj
programIcon = pygame.image.load(f'{path}\icon.png')
pygame.display.set_icon(programIcon)

# Jei taškas pajuda, nuimamas vienas procentas baterijos
def moved():
    global battery, batteryCost
    battery -= batteryCost

# Judėjimo funkcijos, jei taškas atitinka reikalavimus nurodytus žemiau, iškviečiamos šios funkcijos (pagal krypį)
def move_right():
    global start_cord_x, start_cord_y, displayCord
    displayCord[0] += 1
    start_cord_x = start_cord_x + cordSize
    moved()
        
def move_left():
    global start_cord_x, start_cord_y, displayCord
    displayCord[0] -= 1
    start_cord_x = start_cord_x - cordSize
    moved()
        
def move_up():
    global start_cord_x, start_cord_y, displayCord
    displayCord[1] += 1
    global start_cord_x, start_cord_y
    start_cord_y = start_cord_y - cordSize
    moved()
        
def move_down():
    global start_cord_x, start_cord_y, displayCord
    displayCord[1] -= 1
    start_cord_y = start_cord_y + cordSize
    moved()

# Funkcija nubraižanti žalias linijas per visą ekraną
def lines():
    global verticalLine, horizontalLine,cordSize
    for i in range(int(x)//cordSize):
        verticalLine -= cordSize;
        screen.blit(verticalMin, (250 - verticalLine, 0))
        
    for i in range(int(x)//cordSize):
        verticalLine += cordSize;
        screen.blit(verticalMin, (250 + verticalLine, 0))
            
    for i in range(int(y)//cordSize):
        horizontalLine += cordSize;
        screen.blit(horizontalMin, (0, 250 + horizontalLine))
            
    for i in range(int(y)//cordSize):
        horizontalLine -= cordSize;
        screen.blit(horizontalMin, (0, 250 - horizontalLine)) 

# Perjungiama "žaidimo" eiga, jei taškas grįžta iš koordinačių (žalias su pakuote)
def withPackage():
    global with_Package, without_package
    without_package = False
    with_Package = True
# Perjungiama "žaidimo" eiga, jei taškas eina į koordinates (raudonas be pakuotės)
def withoutPackage():
    global cord1, cord2, displayCord, with_Package, without_package,  moved_right, moved_left, moved_down, moved_up, countPackage, file_line_number
    without_package = True
    with_Package = False
    countPackage += 1
    moved_left, moved_right, moved_up, moved_down = 0, 0, 0, 0 
    displayCord[0] = 0
    displayCord[1] = 0
    

#  "Žaidimo" pabaigos funkcija, kuri suskaičiuoja, kiek baterijos dar reikėtų ir iškviečia "žaidimo" pabaigos ekraną
def gameover():
    global game, gameoverScreen, cordsLeft, batteryNeeded
    game = False
    gameoverScreen = True
    for i in cordsLeft:
        cordsLeft1, cordsLeft2 = i.split("," "")
        batteryNeeded += (int(cordsLeft1) + int(cordsLeft2))*2




# Pagrindinė "žaidimo" eiga
while game == True:
    # Žaidimo greičio nustatymas
    time_elapsed_since_last_action += clock.tick(5)
    
    # Tikrinamos taško atvaizduojamos koordinatės, jei jos yra 0, tada nuskaitoma kita eilutė iš failo
    if displayCord[0] == 0 or displayCord[0] == 0:
        file_line_number += 1
        pygame.mixer.music.load(f"{path}\music\s.wav")
        pygame.mixer.music.play(0)
    cords = linecache.getline('cord.txt', file_line_number);
    if len(cords) == 0:
        gameover()
        
    # Tikrinama failo eilutė, jei ji egzistuoja, toliau vykdoma "žaidimo eiga"
    if len(cords) != 0:
        cord1, cord2 = cords.split("," "")
        cord1 = int(cord1)
        cord2 = int(cord2) 
        
        # Tikrinama ar užteks baterijos įvykdyti užduotį, jei ne, duodama kita užduotis ir netinkama užduotis įrašoma į failą
        batteryNeeds = (abs(cord1) + abs(cord2))*2
        if battery < batteryNeeds and without_package == True:
            file_line_number += 1
            batteryToMove = False
            displayCord = [0,0]
            i = ""
            i = f"{int(cord1)},{int(cord2)}"
            cordsLeft.append(i)
        elif battery >= batteryNeeds:
            batteryToMove = True
            
        # Kiekvieną ėjimą nustatomas "žaidimo" ekranas iš naujo.
        screen.fill([0, 0, 0])
        
        # Nubraižomos pilkos linijos
        screen.blit(vertical, (x/2-1, 0))
        screen.blit(horizontal, (0, y/2-1))
        
        # Iškiečiama funkcija nubraižanti žalias linijas
        lines()

        # "Žaidimo" judėjimo eiga. Jei baterijos užtenka, nustatoma ar taškas turi pakuotę ar ne, jei turi, pagal koordinates taškas grįžta į 0,0 koordinates, jei ne, taškas eina į 0,0 koordinates
        if batteryToMove == True: 
            if with_Package == True: 
                pygame.mixer.music.load(f"{path}\music\m.wav")
                pygame.mixer.music.play(0)
                robot.fill("green")
                withPackage()
                if cord2 < end_cord_y and displayCord[1] < 0:
                    moved_up += 1
                    move_up()
                elif cord2 < end_cord_y and displayCord[1] > 0:
                    moved_down += 1
                    move_down()
                elif cord1 < end_cord_y and displayCord[0] < 0:
                    moved_right += 1
                    move_right()
                elif cord1 < end_cord_y and displayCord[0] > 0:
                    moved_left += 1
                    move_left()
                elif displayCord[0] == 0 and displayCord[1] == 0:
                    withoutPackage()


            
            if without_package == True and cord1 != 0 and cord2 != 0:
                pygame.mixer.music.load(f"{path}\music\w.wav")
                pygame.mixer.music.play(0)
                robot.fill("Red")
                if cord1 > 0 and moved_right != abs(cord1) and battery > batteryNeeds:
                    moved_right += 1
                    move_right()
                elif cord2 > 0 and moved_right == abs(cord1) and moved_up != abs(cord2):
                    moved_up += 1
                    move_up()
                elif cord2 < 0 and moved_right == abs(cord1) and moved_down != abs(cord2):
                    moved_down += 1
                    move_down()

            
                if cord1 < 0 and moved_left != abs(cord1) and battery > batteryNeeds:
                    moved_left += 1
                    move_left()
                elif cord2 > 0 and moved_left == abs(cord1) and moved_up != abs(cord2):
                    moved_up += 1
                    move_up()
                elif cord2 < 0 and moved_left == abs(cord1) and moved_down != abs(cord2):
                    moved_down += 1
                    move_down()
                elif cord1 == displayCord[0] and cord2 == displayCord[1]:
                    withPackage()
                


        # "Žaidimo" eigos teksto atvaizdavimas: baterija, dabartinės koordinatės, koordinatės į kurias taškas eina
        displayCordText = font.render(str(displayCord), True, "white", "black")
        displayCordTextReact = displayCordText.get_rect()
        displayCordTextReact.center = (50, 30)
        screen.blit(displayCordText, displayCordTextReact)
        
        displayBatteryText = font.render(f"Battery: {str(battery)} %", True, "white", "black")
        displayBatteryTextReact = displayBatteryText.get_rect()
        displayBatteryTextReact.center = (x-130, y-30)
        screen.blit(displayBatteryText, displayBatteryTextReact)
        
        displayWorkingOn = font.render(f"Working on: [{str(cord1)}, {str(cord2)}]", True, "white", "black")
        displayWorkingOnReact = displayWorkingOn.get_rect()
        displayWorkingOnReact.center = (x-160, y-470)
        screen.blit(displayWorkingOn, displayWorkingOnReact)
        
        # Taškas atvaizduojamas ekrane
        screen.blit(robot, (start_cord_x, start_cord_y))  
        
        # Programos išjungimas paspaudus išjungti mygtuką viršuje dešinėje
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        
        pygame.display.update()
        clock.tick(60)

# "Žaidimo" pabaigos atvaizavimas (kai baigiasi baterijos energija) ar failo eilutės
while gameoverScreen == True:
    screen.fill([255, 255, 255])
    if battery > 0:
        text = font.render('ROBOT DONE HIS JOB!', True, "black")
        textRect = text.get_rect()
        textRect.center = (x // 2, y // 2)
        screen.blit(text, textRect)
    elif battery == 0:
        text = font.render('ROBOT IS OUT OF BATTERY!', True, "black")
        textRect = text.get_rect()
        textRect.center = (x // 2, y // 2)
        screen.blit(text, textRect)
        
    fontgameover = pygame.font.Font('freesansbold.ttf', 12)

    packageCount = fontgameover.render(f'Packages delivered: {str(countPackage)}', True, "black")
    packageCountRect = packageCount.get_rect()
    packageCountRect.center = (x // 2, (y // 2)+50)
    screen.blit(packageCount, packageCountRect)
    
    batteryNeed = fontgameover.render(f'{str(batteryNeeded)}% more battery is needed for full job', True, "black")
    batteryNeedRect = batteryNeed.get_rect()
    batteryNeedRect.center = (x // 2, (y // 2)+70)
    screen.blit(batteryNeed, batteryNeedRect)
    
    left = fontgameover.render(f'Cords left: {str(cordsLeft)}', True, "black")
    leftRect = packageCount.get_rect()
    leftRect.center = ((x // 2)-100, (y // 2)+100)
    screen.blit(left, leftRect)
    
    # Programos išjungimas paspaudus išjungti mygtuką viršuje dešinėje
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.update()
    clock.tick(60)

# Programos išjungimas paspaudus išjungti mygtuką viršuje dešinėje
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
  
    pygame.display.update()
    clock.tick(60)