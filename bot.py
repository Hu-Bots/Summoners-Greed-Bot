from detectors import *
import pyautogui
import cv2
from time import sleep
import random
import os

class Monster():
    def __init__(self, name=str, portrait_img=object, rarity=str):
        self.name = name
        self.is_placed = False
        self.portrait_img = portrait_img
        self.rarity = rarity

class UI():
    def __init__(self):

        #positions and areas
        self.achievements_btn_pos = [1135,124]
        self.achievement_collectable_rgb = (165,238,66)
        self.waveBanner_pos = (1137,69)
        self.challengeTab_pos = (1055,163)
        self.back_arrow_pos = (1890,1011)
        self.ad_closing_area = (609,41,677,339)
        self.achievements_area = [1060,88,155,81]
        self.im_dificilBtn_pos = (1038,490)
        self.refresh_energyBtn_pos = (1058,557)
        self.seleccionarBtn_pos = (1045,825)
        self.monsterSelectorBottom_pos = (919,884)
        self.monsterSelectorTop_pos = (919,243)
        self.confirmBtn_pos = (922,990)
        self.closeGameX_pos = (520,12)
        self.misJuegosTab_pos = (84,79)
        self.BSMaximizeLogo_area = (1750,1,105,83)

        #window references
        self.chest_img = cv2.imread("imgs/chest.png",0)
        self.selectMap_img = cv2.imread("imgs/selectMap.png",0)
        self.monitormanWin_img = cv.imread("imgs/monitorman.png",0)
        self.salesmanWin_img = cv.imread("imgs/salesman.png",0)
        self.modoEdicion_img = cv.imread("imgs/modoEdicion.png",0)
        self.BSWinLoadedRef_img = cv2.imread("imgs/BSWinLoadedRef.png",0)

        #buttons
        self.achievementBtn_img = cv.imread("imgs/achievement_available_img.png",0)
        self.quitarBtn_img = cv.imread("imgs/quitarBtn.png",0)
        self.seleccionarBtn_img = cv.imread("imgs/seleccionarBtn.png",0)
        self.eligeHabilidadBtn_img = cv.imread("imgs/eligeHabilidadBtn.png",0)
        self.seleccionarBtnLost_img = cv.imread("imgs/seleccionarBtnLost.png",0)
        self.OneXSpeed_img = cv.imread("imgs/1XSpeed.png",0)

        # X Buttons
        self.totalXButtons = 3
        self.XBtn_img_ls = []
        for i in range(1,self.totalXButtons+1):
            self.XBtn_img_ls.append(cv2.imread(f"imgs/x{i}.png",0))

        #templates
        self.attack_boost_img =  cv2.imread("imgs/attack_boost.png",0)
        self.summon_100_img = cv2.imread("imgs/summoning_100.png",0)
        self.summon_okayBtn_img = cv2.imread("imgs/summoning_okay.png",0)
        self.gameLogo_img = cv2.imread("imgs/gameLogo.png",0)
        self.BSLogo_img = cv2.imread("imgs/BSLogo.png",0)
        self.BSLogoName_img = cv2.imread("imgs/BSLogoName.png",0)
        self.BSMaximizeLogo_img = cv2.imread("imgs/BSMaximizeLogo.png",0)

        #challenge charges
        self.challengeChargImgs_ls = [
            cv2.imread("imgs/im_0charges.png",0),
            cv2.imread("imgs/im_1charges.png",0),
            cv2.imread("imgs/im_2charges.png",0),
            cv2.imread("imgs/im_3charges.png",0),
            cv2.imread("imgs/im_4charges.png",0),
            cv2.imread("imgs/im_5charges.png",0)
        ]

        #ad x img list
        self.total_adx_imgs = 6
        self.adX_img_ls = []
        for i in range(1,self.total_adx_imgs+1):
            self.adX_img_ls.append(cv2.imread(f"imgs/adx{i}.png",0))

        #ad arr img list
        self.total_adarr_imgs = 4
        self.adArr_img_ls = []
        for i in range(1,self.total_adarr_imgs+1):
            self.adArr_img_ls.append(cv2.imread(f"imgs/adarr{i}.png",0))

        #grid
        self.matchGrid = [
            1,2,3,
            4,5,6,
            7,8,9
            ]
        self.grid_start_pos = (817,276)
        self.gridXincrement = 118
        self.grid_YIncrement = 175

    def getPlaceCoordsOnGrid(self, place=int):
        
        if place == 1 or place == 4 or place == 7:
            Xmultiplier = 0
        elif place == 2 or place == 5 or place == 8:
            Xmultiplier = 1
        elif place == 3 or place == 6 or place == 9:
            Xmultiplier = 2

        if place / 3 <= 1:
            Ymultiplier = 0
        elif place / 3 <= 2:
            Ymultiplier = 1
        elif place / 3 <= 3:
            Ymultiplier = 2

        x = (Xmultiplier * self.gridXincrement) + self.grid_start_pos[0]
        y = (Ymultiplier * self.grid_YIncrement) + self.grid_start_pos[1]

        print(f"Position for monster at {x, y}")

        return [x,y]

    def match_window_active(self):
        #the chest is the reference to the main screen
        chest_screen_pos = [842,770,188,187]
        x,y,w,h = chest_screen_pos

        pyautogui.screenshot("computer_vision.png", (x,y,w,h))

        result = matchtemplate_method(self.chest_img, "computer_vision.png")

        if type(result) is tuple:
            res_x, res_y = result
            res_x+=x
            res_y+=y
            result = (res_x,res_y)
            print(f"Match window is active, chest at: {result}")
            return result
        else:
            print("Game window is not active.")
            self.close_third_window()
            return result
    
    def collect_achievement_reward(self, loops=3):
        x,y,w,h = self.achievements_area

        pyautogui.screenshot("computer_vision.png", (x,y,w,h))

        result = matchtemplate_method(self.achievementBtn_img, "computer_vision.png")

        #if achievemnt available found, gather it.
        if type(result) is tuple:
            print("achievement is available, collecting...")
            counter = 0

            #click on the achievements icon
            x,y = self.achievements_btn_pos
            pyautogui.click(x,y)

            #search for green pixel

            for i in range(0,loops+1):
                #screenshot view
                sleep(1)
                x,y,w,h = 1076,184,1,746
                pyautogui.screenshot("computer_vision.png", (x,y,w,h))

                #open the image and convert it to rgb
                img = cv2.imread("computer_vision.png")
                img = cv.cvtColor(img, cv2.COLOR_BGR2RGB)

                #compare pixels
                for index, pixel in enumerate(img):
                    r1,g1,b1 = pixel[0]
                    r2,g2,b2 = self.achievement_collectable_rgb
                    #gather if found
                    if r1==r2 and g1==g2 and b1==b2:
                        pyautogui.click(x, y+index)
                        counter+=1
                        sleep(0.3)
                        break 
            #close tab
            self.close_third_window()
            print(f"Collected {counter} achievements.")

    def monitorman_handler(self):
        #1. look for monitorman window

        #apply matchtemplate
        x,y,w,h = 753,187,381,98
        pyautogui.screenshot("computer_vision.png", (x,y,w,h))
        result = matchtemplate_method(self.monitormanWin_img, "computer_vision.png")

        #if not found, return none.
        if result is None:
            return

        #if found, search for attack boost.
        print("monitor man has been found.")
        sleep(2)
        x,y,w,h = 675,262,509,201
        pyautogui.screenshot("computer_vision.png", (x,y,w,h))
        result = matchtemplate_method(self.attack_boost_img, "computer_vision.png")

        #if attack boost is found, click no thanks and return
        if type(result) == tuple:
            print("Attack boost detected, aborted.")
            pyautogui.click(799,588)
            sleep(1)
            return

        #if attack boost is not found, click on the watch video tab
        pyautogui.click(1067,592)
        print("watching video...")
        sleep(1)

        #2. - CLOSE AD

        for i in range(0,2):
        
            #if not, check for all other possibilities
            print("sleeping 45 more seconds")
            sleep(45)

            #if match is done, handle it and return
            if self.match_done_handler():
                return

            #first, check if the ad closed automatically
            result = self.match_window_active()
            #if  it did, collect the reward and close window.
            if type(result) is tuple:
                pyautogui.click(1049,599)
                print("ad closed on its own, reward collected.")
                self.statRegistry("Ads Watched")
                return

            #check for double arrow first
            for idx, arr_img in enumerate(self.adArr_img_ls):
                print("searching for arrow button: ", idx)
                x,y,w,h = self.ad_closing_area
                pyautogui.screenshot("computer_vision.png", (x,y,w,h))
                result = matchtemplate_method(arr_img, "computer_vision.png")

                #if a known arrow button is found, click on it
                if type(result) is tuple:
                    res_x, res_y = result
                    img_h, img_w = arr_img.shape
                    center_x = res_x + round(img_w/2) + x
                    center_y = res_y + round(img_h/2) + y
                    pyautogui.click(center_x, center_y)
                    sleep(15) #give time for x button to load
                    print("Arrow button found: ", idx, " clicked and looking for x button...")
                    break

            #check for all x buttons
            for idx, x_img in enumerate(self.adX_img_ls):

                print("searching for button: ", idx)
                x,y,w,h = self.ad_closing_area
                pyautogui.screenshot("computer_vision.png", (x,y,w,h))
                result = matchtemplate_method(x_img, "computer_vision.png")

                #if a known x is found, click on it
                if type(result) is tuple:
                    res_x, res_y = result
                    img_h, img_w = x_img.shape
                    center_x = res_x + round(img_w/2) + x
                    center_y = res_y + round(img_h/2) + y
                    pyautogui.click(center_x, center_y)
                    print("button found: ", idx, " closing ad...")
                    sleep(2)
                    break

            #if match window is visible, collect reward and return
            if type(self.match_window_active()) is tuple:
                self.collect_reward()
                self.statRegistry("Ads Watched")
                return

            #else, click back arrow button from blustacks and see if it closed the ad.
            else:
                x, y = self.back_arrow_pos
                pyautogui.click(x, y)
                sleep(5)
                if type(self.match_window_active()) is tuple:
                    self.collect_reward()
                    self.statRegistry("Ads Watched")
                    return

            #otherwise, check all arrows and xs again quick.
            pyautogui.screenshot("computer_vision.png", self.ad_closing_area)
            x,y,w,h = self.ad_closing_area
            for ad_x in self.adX_img_ls:
                result = matchtemplate_method(ad_x, "computer_vision.png")
                if type(result) is tuple:
                    x+=result[0]
                    y+=result[1]
                    pyautogui.click(x, y)
                    sleep(2)
                    if type(self.match_window_active()) is tuple:
                        self.collect_reward()
                        self.statRegistry("Ads Watched")
                        return

            for ad_arr in self.adArr_img_ls:
                result = matchtemplate_method(ad_arr, "computer_vision.png")
                if type(result) is tuple:
                    x+=result[0]
                    y+=result[1]
                    pyautogui.click(x, y)
                    sleep(2)
                    if type(self.match_window_active()) is tuple:
                        self.collect_reward()
                        self.statRegistry("Ads Watched")
                        return

        pyautogui.screenshot("UnsolvableAd.png")

        if self.restartGame() == False:
            return False

    def openBS(self):
        pyautogui.press("winleft")
        sleep(1)
        pyautogui.typewrite("bluestacks")
        sleep(1)
        pyautogui.press("enter")
        sleep(10)

        #check if the window was opened.
        pyautogui.screenshot("computer_vision.png")
        result = matchtemplate_method(self.BSLogoName_img, "computer_vision.png")
        if type(result) is tuple:
            print("BlueStacks is opened and loading...")
            counter = 0
            while True:
                pyautogui.screenshot("computer_vision.png", (self.BSMaximizeLogo_area))
                is_maximized = matchtemplate_method(self.BSMaximizeLogo_img, "computer_vision.png")
                if type(is_maximized) is tuple:
                    print("Bluestacks window is maximized.")
                    break
                else:
                    x, y = result
                    pyautogui.doubleClick(x, y, .1)
                    sleep(2)
                    counter += 1
                    if counter > 5:
                        print("unable to maximize bluestacks")
                        return False
        else:
            pyautogui.hotkey("alt", "f4")
            return False

        counter = 0
        while True:
            pyautogui.screenshot("computer_vision.png")
            result = matchtemplate_method(self.BSWinLoadedRef_img, "computer_vision.png")
            if type(result) is tuple:
                print("bluestacks window is ready")
                return True
            else:
                sleep(10)
                print("window has not loaded")
                counter += 1
                if counter > (6*5):
                    print("Too much time has passed :", counter/6, " minutes.")
                    pyautogui.screenshot("BSLoadError.png")
                    return False

    def restartGame(self):
        pyautogui.screenshot("computer_vision.png")
        result = matchtemplate_method(self.BSLogo_img, "computer_vision.png")
        if type(result) is tuple:
            print("bluestacks window is opened.")
        else:
            for i in range(0,3):
                open_BS = self.openBS()
                if open_BS == True:
                    break
            if open_BS == False:
                print("was unable to open BS.")
                return False

        x, y = self.closeGameX_pos
        pyautogui.moveTo(x, y)
        sleep(2)
        for i in range(0,3): #to close any tabs after the game one.
            pyautogui.click()
            sleep(2)

        x, y = self.misJuegosTab_pos
        pyautogui.click(x, y)
        sleep(3)

        #click on the game logo to open it
        pyautogui.screenshot("computer_vision.png")
        result = matchtemplate_method(self.gameLogo_img, "computer_vision.png")

        if type(result) is tuple:
            x, y = result
            pyautogui.click(x, y)
        else:
            pyautogui.hotkey("alt","f4")
            return False

        for i in range(0,6*5):
            sleep(10)

            #close pop up window
            if self.close_third_window() == True:
                self.statRegistry("Game Restarts")
                return True
        
        print("unable to start game")
        pyautogui.screenshot("unable to start game.png")
        return False

    def salesman_handler(self):

        #check if salesman window is open
        x,y,w,h = 753,187,381,98
        pyautogui.screenshot("computer_vision.png", (x,y,w,h))
        result = matchtemplate_method(self.salesmanWin_img, "computer_vision.png")

        #if it is, just buy whatever he sells
        if type(result) is tuple:
            #click buy
            pyautogui.click(956,594)
            sleep(3)
            pyautogui.click()
            sleep(3)
            
            self.collect_reward()
    
    def collect_reward(self):
            #scan for the accept tab 5 times
            for i in range(0,5):
                accep_reward_img = cv.imread("imgs/accept_salesman.png", 0)
                pyautogui.screenshot("computer_vision.png")
                result = matchtemplate_method(accep_reward_img, "computer_vision.png")
                if type(result) is tuple:
                    x, y = result
                    pyautogui.click(x, y)
                    print("Collected reward.")
                    continue
            
    def match_done_handler(self, mode="hard"):
        """
        @Return True if match restarted
        @Return None if visuals not found.
        """

        #check for continue button
        continue_img = cv.imread("imgs/continue.png",0)
        pyautogui.screenshot("computer_vision.png")
        result = matchtemplate_method(continue_img, "computer_vision.png")

        if type(result) is tuple:
            print("Match done, restarting")
            pyautogui.click(935,814) #click continue
            sleep(3)
            if mode=="normal":
                x, y = 762,838
            elif mode=="hard":
                x, y = 932, 834
            pyautogui.click(x, y) #click mode mode
            sleep(3)
            x, y = self.confirmBtn_pos
            pyautogui.click(x, y) #click confirm
            sleep(3)
            return True
        else:
            return False

    def close_third_window(self):
        """@Returns True if closed.
        @Returns False if not closed."""
        pyautogui.screenshot("computer_vision.png")
        for idx, XBtnImg in enumerate(self.XBtn_img_ls):
            result = matchtemplate_method(XBtnImg, "computer_vision.png")

            if type(result) is tuple:
                x, y = result
                pyautogui.click(x, y)
                sleep(3)
                print("Closed a pop-up window.")
                return True
        
        print("No pop-up window found.")
        return False

    def summon(self):
        #open the summoning window
        pyautogui.click(689,203)
        sleep(2)

        #check if can summon x 100.
        x, y, w, h = 766,976,34,42
        pyautogui.screenshot("computer_vision.png", (x, y, w, h))
        result = matchtemplate_method(self.summon_100_img, "computer_vision.png")
        #if not, return. Main loop will close window.
        if result is None:
            return

        #otherwise, click the summoning button, fast forward and wait
        x, y = 755,1000 #summoning 100 btn location.
        pyautogui.click(x, y)
        sleep(2)
        pyautogui.click(704,112)
        sleep(5)

        # scan for the okay button a max of 5 times
        for i in range(0,6):
            pyautogui.screenshot("computer_vision.png")
            result = matchtemplate_method(self.summon_okayBtn_img, "computer_vision.png")

            if type(result) == tuple:
                x, y = result
                pyautogui.click(x,y)
                self.statRegistry("Summons")
                sleep(2)
                return result

    def currentGameWindow(self):
        """
        @return "match window"
        @return "map select window"
        @return "seleccionarMapa window"
        @return "seleccionarMapaLost window"
        """

        for i in range(0,2):

            sleep(3)

            possible_windows = {
                "match window" : [self.chest_img],
                "map select window": [self.selectMap_img],
                "seleccionarMapa window" : [self.seleccionarBtn_img],
                "seleccionarMapaLost" : [self.seleccionarBtnLost_img]
                }

            pyautogui.screenshot("computer_vision.png")

            for winName, winIm_ls in possible_windows.items():

                for winImg in winIm_ls:
                    result = matchtemplate_method(winImg, "computer_vision.png")
                    if type(result) == tuple:
                        return winName
            
            self.close_third_window()

    def challengeCharges(self):
        pyautogui.screenshot("computer_vision.png")
        for i in range(0,6):
            result = matchtemplate_method(self.challengeChargImgs_ls[i], "computer_vision.png")
            if type(result) == tuple:
                return i

    def removeAllMonsters(self):
        counter = 0
        while True:
            pyautogui.screenshot("computer_vision.png")
            result = matchtemplate_method(self.quitarBtn_img, "computer_vision.png")
            if type(result) is tuple:
                x, y = result
                pyautogui.click(x, y)
                sleep(1)
            else:
                counter += 1

            if counter >= 3:
                print("All monsters have been removed.")
                return

    def placeMonster(self, monster=Monster, place=int):
        if monster.rarity == "common":
            prev_swipes = 0
        elif monster.rarity == "rare":
            prev_swipes = 1
        elif monster.rarity == "epic":
            prev_swipes = 2
        elif monster.rarity == "legendary":
            prev_swipes = 4
        elif monster.rarity == "mythical" or monster.rarity == "special":
            prev_swipes = 5

        x, y = self.getPlaceCoordsOnGrid(place)
        pyautogui.click(x, y)
        sleep(2)

        #do prev swipes
        for i in range(0,prev_swipes):
            self.swipe(self.monsterSelectorBottom_pos, self.monsterSelectorTop_pos)
            continue

        swipe_counter = 0
        while True:
            pyautogui.screenshot("computer_vision.png")
            result = matchtemplate_method(monster.portrait_img, "computer_vision.png")

            if type(result) is tuple:
                x, y = result
                pyautogui.click(x, y)
                print(f"{monster.name} had been placed in place {place}.")
                sleep(2)
                return
            else:
                if monster.rarity == "mythical":
                    self.swipe(self.monsterSelectorBottom_pos, self.monsterSelectorTop_pos, sleep_after=1)
                else:
                    self.swipe(self.monsterSelectorBottom_pos, self.monsterSelectorTop_pos)
                swipe_counter +=1
                if swipe_counter >= 5:
                    return
                continue

    def swipe(self, start_pos, end_pos, duration = 0.3, sleep_after = 0):
            x, y = start_pos
            pyautogui.mouseDown(x, y)
            x, y = end_pos
            pyautogui.moveTo(x, y, 1)
            sleep(duration)
            pyautogui.mouseUp()
            sleep(sleep_after)

    def check2XSpeed(self):
        pyautogui.screenshot("computer_vision.png")
        result = matchtemplate_method(self.OneXSpeed_img, "computer_vision.png")
        if type(result) is tuple:
            x, y = result
            pyautogui.click(x, y)
            print("2X Speed activated.")
        else:
            print("2X Speed active")

    def statRegistry(self, update_key):
        """
        "Ads Watched" : int
        "Game Restarts" : int
        "Summons" : int
        "IM Losses" : int
        "IM Matches" : int
        """

        filename = "stats.txt"
        #check if file exists. If not, create it.
        if not os.path.exists(filename):
            print("Stats file did not exist and it was created.")
            with open(filename, "w+") as file:
                text = "{'Ads Watched':0, 'Game Restarts':0, 'Summons':0, 'IM Losses':0, 'IM Matches':0}"
                file.write(text)

        #read file and populate dictionary
        with open(filename, "r+") as file:
            lines = file.read()
            stats_dict = eval(lines)
            
            #update dict
            stats_dict[update_key] += 1

        with open(filename, "w") as file:
            file.write(str(stats_dict))

user_interface = UI()

#MONSTERS

#epic
speedy = Monster("Speedy", cv2.imread("imgs/monSpeedy.png",0), "epic")
forty = Monster("Forty", cv2.imread("imgs/monForty.png",0), "epic")

#legendaries
kevin = Monster("Kevin", cv2.imread("imgs/monKevin.png",0), "legendary")
ash = Monster("Ash", cv2.imread("imgs/monAsh.png",0), "legendary")
puffy = Monster("Puffy", cv2.imread("imgs/monPuffy.png",0), "legendary")
deathbite = Monster("Deathbite", cv2.imread("imgs/monDeathbite.png",0), "legendary")
slimeking = Monster("Slime King", cv2.imread("imgs/monSlimeking.png",0), "legendary")
frostbite = Monster("Frostbite", cv2.imread("imgs/monFrostbite.png",0), "legendary")
lightning = Monster("Lightning", cv2.imread("imgs/monLightning.png",0), "legendary")

#Special
kronos = Monster("Kronos", cv2.imread("imgs/monKronos.png",0), "special")

#Mythical
jiraya = Monster("Jiraya", cv2.imread("imgs/monJiraya.png",0), "mythical")
zeus = Monster("Zeus", cv2.imread("imgs/monZeus.png",0), "mythical")

def main(game_mode = "joint revenge", reset_stats = True):
    """
    game modes
    "joint revenge"
    "evil summoner"
    """

    if reset_stats == True and os.path.exists("stats.txt"):
        os.remove("stats.txt")

    summoning_loops = 0
    window_inactive_counter = 0

    if game_mode == "joint revenge":

        while True:
            if user_interface.match_window_active() is None:
                if type(user_interface.match_done_handler()) is tuple:
                    continue
                window_inactive_counter += 1
                if window_inactive_counter >= 20:
                    print("game window inactive too long...")
                    user_interface.restartGame()
                continue

            window_inactive_counter = 0

            if user_interface.monitorman_handler() == False:
                print("Unable to continue.. check log.")
                return

            user_interface.salesman_handler()

            user_interface.collect_achievement_reward()

            if summoning_loops >= 200:
                summoned = user_interface.summon()
                if summoned is None:
                    summoning_loops = 0

            if summoning_loops == 1:
                user_interface.check2XSpeed()

            summoning_loops+=1

            sleep(3)

    if game_mode == "evil summoner":
        while True:
            lost = False

            #1. - Set up window
            while True:

                currentWin = user_interface.currentGameWindow()

                if currentWin is None:
                    continue

                if currentWin == "match window":
                    x, y = user_interface.waveBanner_pos
                    pyautogui.click(x, y)
                    sleep(2)
                
                if currentWin == "seleccionarMapa window" or currentWin == "seleccionarMapaLost window":
                    x, y = user_interface.seleccionarBtn_pos
                    pyautogui.click(x, y)
                    sleep(2)

                x,y = user_interface.challengeTab_pos
                pyautogui.click(x, y)
                sleep(2)

                currentChallengeCharges = user_interface.challengeCharges()
                print(f"There are currently {currentChallengeCharges} charges left")
                break

            #click on the hard mode btn
            while True:
                x, y = user_interface.im_dificilBtn_pos
                pyautogui.click(x, y)
                sleep(2)

                if currentChallengeCharges == 0:
                    x, y = user_interface.refresh_energyBtn_pos
                    pyautogui.click(x, y)
                    currentChallengeCharges = 5
                    sleep(2)
                    continue
                
                currentChallengeCharges -= 1
                break


            #2. remove all monsters
            user_interface.removeAllMonsters()

            #3. WAVES

            #Wave 1 . - no monsters are placed.
            user_interface.placeMonster(ash, 1)
            user_interface.placeMonster(kevin, 2)
            user_interface.placeMonster(deathbite, 3)
            user_interface.close_third_window()
            sleep(2)
            x, y = user_interface.confirmBtn_pos
            pyautogui.click(x, y)
            sleep(2)
            user_interface.collect_achievement_reward()

            #wait for wave to end
            print("waiting for wave 1 to end")
            while True:
                if lost == True:
                    print("Lost in wave 1, restarting.")
                    break
                pyautogui.screenshot("computer_vision.png")
                result = matchtemplate_method(user_interface.modoEdicion_img, "computer_vision.png")
                if type(result) == tuple:
                    print("wave 1 has ended.")
                    break
                else:
                    #click on the lost btn if lost
                    result = matchtemplate_method(user_interface.seleccionarBtnLost_img, "computer_vision.png")
                    if type(result) is tuple:
                        x, y = result
                        pyautogui.click(x, y)
                        lost = True
                    sleep(5)

            if lost == True:
                print("Back to main loop 1")
                continue

            #wave 2 . - some monsters might be placed.
            user_interface.placeMonster(lightning, 4)
            user_interface.placeMonster(zeus, 5)
            user_interface.placeMonster(puffy, 6)
            user_interface.close_third_window()
            sleep(2)

            #wait for wave to end
            print("waiting for wave 2 to end.")
            while True:
                if lost == True:
                    print("lost on wave 2, restarting.")
                    break
                pyautogui.screenshot("computer_vision.png")
                result = matchtemplate_method(user_interface.modoEdicion_img, "computer_vision.png")
                if type(result) == tuple:
                    print("wave 2 has ended.")
                    break
                else:
                    #click on the lost btn if lost
                    result = matchtemplate_method(user_interface.seleccionarBtnLost_img, "computer_vision.png")
                    if type(result) is tuple:
                        x, y = result
                        pyautogui.click(x, y)
                        lost = True
                    sleep(5)
            
            if lost == True:
                print("back to main loop 2")
                continue

            #wave 3 . - All monster are probably gone
            user_interface.placeMonster(frostbite, 1)
            user_interface.placeMonster(speedy, 2)
            user_interface.placeMonster(slimeking, 3)
            user_interface.placeMonster(jiraya, 7)
            user_interface.placeMonster(forty, 8)
            user_interface.placeMonster(kronos, 9)
                        
            user_interface.close_third_window()
            sleep(2)

            #wait for wave to end
            print("waiting for wave 3 to end.")
            while True:
                if lost == True:
                    print("lost in wave 3, restarting...")
                    break
                pyautogui.screenshot("computer_vision.png")
                result = matchtemplate_method(user_interface.eligeHabilidadBtn_img, "computer_vision.png")
                if type(result) == tuple:
                    x, y = result
                    print("wave 3 has ended.")
                    break
                else:
                    #click on the lost btn if lost
                    result = matchtemplate_method(user_interface.seleccionarBtnLost_img, "computer_vision.png")
                    if type(result) is tuple:
                        x, y = result
                        pyautogui.click(x, y)
                        lost = True
                        break
                    sleep(5)

            if lost == True:
                print("gone back to main loop 3")
                user_interface.statRegistry("IM Losses")
                continue

            #click on the choose ability button three times.
            for i in range(0,3):
                pyautogui.click(x, y)
                sleep(random.randint(1,4))

            user_interface.statRegistry("IM Matches")
            
            #wait until match done window appears
            for i in range(0,6):
                if user_interface.currentGameWindow() == "seleccionarMapa window":
                    break
                else:
                    sleep(10)

main(
    game_mode="joint revenge",
    reset_stats=True
    )