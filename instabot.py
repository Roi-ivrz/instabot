from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import numpy as np
import random, re, datetime, importlib, time, math, sys, io
# local files
import keys, actionCounter

PATH = 'C:\Program Files (x86)\chromedriver.exe'
chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")

LongCycle = False
max_likes_per_hour = 250
max_following_per_hour = 150
max_unfollowing_per_hour = 150


like_xpath = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/div/span'

# read white list 
file = open("white_list.txt","r")
white_list = file.read().split(',')

# randomized sleep time
def naturalSleep(value):
    global LongCycle
    deviation = 0.3
    if LongCycle:
        # print('long cycle')
        value = value * 1.7
    upperBound,lowerBound = round(value + value*deviation)*100, round(value - value*deviation)* 100
    newVal = float(random.randrange(lowerBound, upperBound))/100
    sleep(newVal)

def oneAction(actionType):
    importlib.reload(actionCounter)
    now = datetime.datetime.now()
    today = now.strftime('%m.%d')
    current_hour = now.strftime('%H')

    if actionType == 'actionCount':
        print('actions: '+ str(actionCounter.daily_actions))
        if actionCounter.daily_actions > 500: print('exceeded 500 actions today')
    else:
        if actionCounter.date == today: actionCounter.daily_actions += 1
        else: actionCounter.daily_actions = 1

        if actionType == 'like': 
            actionCounter.total_likes += 1
            if actionCounter.hour == current_hour:
                actionCounter.hour_likes += 1
            else:actionCounter.hour_likes = 1

        elif actionType == 'follow': 
            actionCounter.total_follows += 1
            if actionCounter.hour == current_hour:
                actionCounter.hour_follows += 1
            else:actionCounter.hour_follows = 1

        elif actionType == 'unfollow': 
            actionCounter.total_unfollows += 1
            if actionCounter.hour == current_hour:
                actionCounter.hour_unfollows += 1
            else:actionCounter.hour_unfollows = 1

        elif actionType == 'comment': actionCounter.total_comments += 1
        elif actionType == 'DM': actionCounter.total_DMs += 1

        with open("actionCounter.py", "w") as f:
            f.write("date = '"+ str(today) + "'\n")
            f.write("hour = '"+ str(current_hour) + "'\n")
            f.write('hour_likes = ' + str(actionCounter.hour_likes) + '\n')
            f.write('hour_follows = ' + str(actionCounter.hour_follows) + '\n')
            f.write('hour_unfollows = ' + str(actionCounter.hour_unfollows) + '\n')
            f.write('daily_actions = ' + str(actionCounter.daily_actions) + '\n')
            f.write('\n')
            f.write('total_likes = ' + str(actionCounter.total_likes) + '\n')
            f.write('total_comments = ' + str(actionCounter.total_comments) + '\n')
            f.write('total_follows = ' + str(actionCounter.total_follows) + '\n')
            f.write('total_unfollows = ' + str(actionCounter.total_unfollows) + '\n')
            f.write('total_DMs = ' + str(actionCounter.total_DMs) + '\n')

class Instabot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)
        self.driver.get('https://instagram.com')
        sleep(5)
        #initial login info
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')\
            .send_keys(username)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')\
            .send_keys(password)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')\
            .click()
        sleep(5)
        #save login
        self.driver.find_element_by_xpath("//*[text()='Save Info']").click()
        sleep(5)
        #notification
        self.driver.find_element_by_xpath("//*[text()='Not Now']").click()
        sleep(5)
        
    def scrolling_list(self, maxNum, scrollbox_location):
        actions = ActionChains(self.driver)
        scrollBox = self.driver.find_element_by_xpath(scrollbox_location)
        nameLinks = 1
        repetition = 0
        while int(nameLinks) < int(maxNum):
            scrollBox.click()
            prevCount = len(scrollBox.find_elements_by_class_name('FPmhX'))
            actions.send_keys(Keys.PAGE_DOWN).perform()
            sleep(0.5)
            nameLinks = len(scrollBox.find_elements_by_class_name('FPmhX'))
            if prevCount == nameLinks: repetition += 1
            if repetition == 6: return False
            actions.send_keys(Keys.PAGE_DOWN).perform()
            print('current:', nameLinks, '/', maxNum, 'max')
            sleep(0.5)
        if int(nameLinks) >= int(maxNum): return True

    def scrolling(self, maxNum, scrollbox_location, xpath):
        i = 0
        while i < 4: 
            if bot.scrolling_list(maxNum, scrollbox_location) == True: break
            else: 
                print('scrolling failed, retrying')
                self.driver.refresh()
                i += 1
                print('trial:', i, '/4')
                sleep(3)
                self.driver.find_element_by_xpath(xpath)\
                    .click()
                sleep(2)
        if i == 4: 
            print('4 unsucessful attempt, try again later')
            return False

    def unique_post(self):
        
        btn = self.driver.find_element_by_xpath(like_xpath)
        aria_label = btn.find_element_by_css_selector('svg').get_attribute("aria-label")
        sleep(2)
        if aria_label == 'Like':
            return True
        else:
            return False    
    
    def ratio(self):
        #follower count
        follower = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')\
                    .text
        follower = ''.join(re.split(',|\.', follower))
        #following count
        following = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span')\
            .text
        following = ''.join(re.split(',|\.', following))
        #in case value in thousands
        if 'k' in follower:
            follower = follower.replace('k', '')
            follower = int(follower) *100
        if 'k' in following:
            following = following.replace('k', '')
            following = int(following) *100
        #follower to following ratio
        ratio = int(follower) / int(following)
        # print('Ratio:', ratio)
        return ratio, follower

    def get_follower_list(self):
        #click on instagram icon to return home
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img')\
            .click()
        #click open profile
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a')\
            .click()
        sleep(4)
        #obtain follower count
        followerCount = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').text.split(' ')[0]
        followerCount = ''.join(followerCount.split(','))
        print(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').text)
        #open follower tab
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')\
            .click()
        sleep(3)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        #scrolling
        bot.scrolling(int(followerCount) - 2, '/html/body/div[4]/div/div/div[2]', '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')

        #clear previous data on the following text file
        with open("follower_list.txt","r+") as file: file.truncate(0)

        #generating names from each element
        print('end of scrolling, generating followers list...')
        followerList = scrollBox.find_elements_by_tag_name('a')
        with open('follower_list.txt', 'a') as appendFile:
            for item in followerList:
                if item.text != '': appendFile.write(item.text + ',')
            
        print('follower list generated!')
        #close followers tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
            .click()

    def get_following_list(self, amount):
        #click on instagram icon to return home
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img')\
            .click()
        #click open profile
        self.driver.get('https://www.instagram.com/' + str(keys.username))
        sleep(4)
        #obtain follower count
        if amount == 'ALL':
            followingCount = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').text.split(' ')[0]
            followingCount = ''.join(followingCount.split(','))
            print(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').text)
        else:
            followingCount = int(amount)
        #click on following list
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')\
            .click()
        sleep(2)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        #scrolling
        bot.scrolling(int(followingCount) - 2, '/html/body/div[4]/div/div/div[2]', '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')

        #clear previous data on the following text file
        with open("following_list.txt","r+") as file: file.truncate(0)

        #generating names from each element
        print('end of scrolling, generating following list...')
        followingList = scrollBox.find_elements_by_tag_name('a')
        with open('following_list.txt', 'a') as appendFile:
            for item in followingList:
                if item.text != '': appendFile.write(item.text + ',')
            
        print('following list generated!')
        #close following tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
            .click()
       
    def not_following_back_list(self):
        #followers 
        with open("follower_list.txt","r") as file:
            followerNames = file.read().split(',')
        #following
        with open("following_list.txt","r") as file:
            followingNames = file.read().split(',')
        not_following_back = np.setdiff1d(followingNames, followerNames)
        with open('not_following_back.txt', 'w') as appendFile:
            for item in not_following_back:
                appendFile.write(item + ',')
        print('list of not following back users compiled:', len(not_following_back), 'total users')

    def unfollow_NFB(self, count):
        with open("not_following_back.txt","r") as file:
            not_following_back = file.read().split(',')
            print(str(len(not_following_back)) + ' users not following you back')
            i, errorCounter, global_error = 0, 1, 0
            prevName = '' 

            while i < count:
                name = not_following_back[i]
                if name not in white_list:
                    self.driver.get('https://instagram.com/' + name)
                    naturalSleep(4)
                    try:
                        naturalSleep(6)
                        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button')\
                        .click()
                        naturalSleep(6)
                        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
                        oneAction('unfollow')
                        not_following_back.remove(name)
                        i += 1
                        print(i, '/', count, 'successfully unfollowed:', name)
                        
                    except NoSuchElementException:
                        # check if following option exist for public users
                        if self.driver.find_elements_by_xpath("//*[text()='Follow']") != []:
                            print('already unfollowed user:', name)
                            not_following_back.remove(name)
                        elif self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button') != []:
                            print('already unfollowed user:', name)
                            not_following_back.remove(name)
                        # check if following option exist for private users
                        elif self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/button') != []:
                            print('already unfollowed user:', name)
                            not_following_back.remove(name)
                        else: 
                            print('error ' + str(errorCounter))
                            prevName = name

                        if prevName == name: errorCounter += 1
                        else: errorCounter = 1

                        if errorCounter == 4:
                            global_error += 1
                            not_following_back.remove(name)
                        if global_error == 4:
                            break
                        sleep(2)
                else: not_following_back.remove(name)

            oneAction('actionCount')
        with open("not_following_back.txt","w") as appendFile:
            for item in not_following_back:
                appendFile.write(item + ',')
        if count > 0:
            print('successfully unfollowed', count, 'users')
      
    def follow(self, amount):
        followed = 0
        while followed < amount:
            self.driver.get('https://instagram.com')
            sleep(3)
            targets = self.driver.find_elements_by_class_name('ZIAjV')
            userList = []
            for item in targets[:(len(targets)-1)]:
                if item.text not in userList:
                    userList.append(item.text)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)

            for names in userList:
                self.driver.get('https://instagram.com/' + names)
                naturalSleep(4)
                ratio, follower = bot.ratio()
                naturalSleep(4)
                try:
                    # picking the user to scroll their follower list
                    if followed < amount and ratio >= 0.5 and ratio < 1.1 and int(follower) > 150:
                        # clicking on their follower list
                        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
                        sleep(2)
                        bot.scrolling(150, '/html/body/div[4]/div/div/div[2]', '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
                        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
                        followerList = scrollBox.find_elements_by_tag_name('a')
                        followerNameList = [item.text for item in followerList]

                        for item in followerNameList:
                            if item != '' and item != 'ivrz.fpv' and followed < amount:
                                self.driver.get('https://instagram.com/' + item)
                                naturalSleep(10)
                                # currently not following private accounts
                                already_following = self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[2]/button')
                                already_following = np.size(already_following) > 0
                                if not already_following:
                                    ratio, follower = bot.ratio()
                                    #deciding on following new user
                                    if ratio < 1.2 and int(follower) > 120:
                                        # click on follow
                                        self.driver.find_element_by_xpath("//*[text()='Follow']").click()
                                        oneAction('follow')
                                        followed += 1
                                        print('follwed', followed, 'users')
                                        #like their posts
                                        try:
                                            posts = self.driver.find_elements_by_tag_name('a')
                                            hrefs = [item.get_attribute('href') for item in posts
                                                        if '.com/p/' in item.get_attribute('href')]
                                            if len(hrefs) < 7:
                                                likes = len(hrefs)
                                            else:
                                                likes = random.randint(3,7)

                                            for i in range(likes):
                                                self.driver.get(hrefs[i])
                                                naturalSleep(5)
                                                if bot.unique_post() == True:          
                                                    self.driver.find_element_by_xpath(like_xpath)\
                                                        .click()
                                                    oneAction('like')
                                                    naturalSleep(5)
                                                    #commenting post
                                                    if random.randint(0,10) < 4: bot.comment()

                                            print('finished liking', likes, 'posts')
                                        except Exception:
                                            print('failed to like post')

                                        oneAction('actionCount')
                                    else: print('skipping user, ratio does not qualify')
                                sleep(5)
                        print('iteration complete')
                        sleep(20) 
                except Exception:
                    print('failed to finish follow cycle with', names)

    def comment(self):
        with open("comments.txt","r") as file:
            comments = file.read().split(',')
            self.driver.find_element_by_class_name('Ypffh').click()
            sleep(1)
            chance = random.randint(0,10)
            num = random.randint(0,12)
            if chance < 3:
                self.driver.find_element_by_class_name('Ypffh').send_keys(comments[random.randrange(0,len(comments))])
            elif num < 2: # scissor hand
                self.driver.find_element_by_class_name('Ypffh').send_keys('\u270C\u270C\u270C')
            elif num < 4: # grim
                self.driver.find_element_by_class_name('Ypffh').send_keys('\u263A\u263A')
            elif num < 7: #lightning
                self.driver.find_element_by_class_name('Ypffh').send_keys('\u26A1\u26A1\u26A1')
            elif num < 10: # heart
                self.driver.find_element_by_class_name('Ypffh').send_keys('\u2764\u2764\u2764')
            else: # snowflake
                self.driver.find_element_by_class_name('Ypffh').send_keys('\u2744\u2744')
            sleep(1)
            self.driver.find_element_by_class_name('Ypffh').send_keys(Keys.ENTER)
            oneAction('comment')
        naturalSleep(15)

    def hashtag_like_and_comment(self, amount):
        with open("hashtags.txt","r") as file:
            hashtags = file.read().split(',')
            List = []
            for item in hashtags:
                List.append(item)
            hashtag_list = random.sample(List, len(List))
        count = 0
        i = 0
        while count < amount:
            print('---------------SWITCHING TO NEXT HASHTAG: #' + hashtag_list[i] + '---------------')
            naturalSleep(15)
            self.driver.get('https://www.instagram.com/explore/tags/' + hashtag_list[i])
            i += 1
            sleep(3)
            element = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/h2')
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            naturalSleep(5)

            posts = self.driver.find_elements_by_tag_name('a')
            hrefs = [item.get_attribute('href') for item in posts
                        if '.com/p/' in item.get_attribute('href')]
            target_posts = random.sample(hrefs, random.randint(16, len(hrefs)))
            naturalSleep(8)
            
            # liking random amount of post in that hashtag
            for item in target_posts:
                self.driver.get(item)
                naturalSleep(25)

                if bot.unique_post() == True:
                    #liking post
                    self.driver.find_element_by_xpath(like_xpath).click()
                    count += 1
                    oneAction('like')
                    naturalSleep(10)

                    #commenting post
                    if random.randint(0,11) < 8: bot.comment()
                        
                    if count % 10 == 0: 
                        print('count: ' + str(count))
                else:
                    print('post already interacted')
            

    def get_NFB_list(self):
        try:
            bot.get_follower_list()
            print('updated follower list')
            bot.get_following_list('ALL')
            print('updated following list')
            bot.not_following_back_list()
            print('---updated NFB list---')
        except:
            print('failed, try again later')
    
    def DM_youtube(self, amount, link):
        with open("following_list.txt","r") as file:
            followingNames = file.read().split(',')
        
        count = 0
        while count < amount:
            user = random.choice(followingNames)
            # self.driver.get('https://instagram.com/roi.zry')
            self.driver.get('https://instagram.com/' + user)
            # check that you're following user
            not_following = self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
            following = np.size(not_following) == 0

            with open("already_dm.txt","r") as file:
                alreadyDMList = file.read().split(',')
            buttons = self.driver.find_elements_by_tag_name('button')
            for item in buttons:
                if item.text == 'Message':
                    item.click()
                    break
            sleep(10)
            already_DM = self.driver.find_elements_by_xpath("//*[contains(text(), 'hey man hows it going')]")
            if user not in alreadyDMList and following:
                if len(already_DM) == 0:
                    print('new account')
                    sleep(10)
                    actions = ActionChains(self.driver)
                    '''
                    self.driver.find_element_by_tag_name('textarea').send_keys("hey hows it going")
                    actions.send_keys(Keys.ENTER).perform()
                    naturalSleep(5)
                    '''
                    self.driver.find_element_by_tag_name('textarea').send_keys("Check out this new video that I just made!")
                    actions.send_keys(Keys.ENTER).perform()
                    naturalSleep(4)
                    self.driver.find_element_by_tag_name('textarea').send_keys(link)
                    actions.send_keys(Keys.ENTER).perform()
                    oneAction('DM')
                    count += 1
                    if count % 5 == 0: print('count: ' + str(count))
                    naturalSleep(40)
                
                else:
                    print('already messaged')
                    naturalSleep(6)
                with open('already_dm.txt', 'a') as file:
                        file.write(user + ',')
                
            else: 
                print('already in DM list')
            
    def cycle(self, unfollow, follow, like, DM, continuous = False, printLog = False):
        importlib.reload(actionCounter)
        if continuous:
            cycles = 10**20
            global max_following_per_hour, max_likes_per_hour, max_unfollowing_per_hour
            if not printLog:
                text_trap = io.StringIO()
                sys.stdout = text_trap
        else:
            cycles = 1

        try:
            for _ in range(cycles):
                start_timer = time.perf_counter()
                # unfollow
                if actionCounter.hour_unfollows < max_unfollowing_per_hour:
                    if actionCounter.hour_unfollows + unfollow < max_unfollowing_per_hour:
                        bot.unfollow_NFB(unfollow)
                    else:
                        bot.unfollow_NFB(max_unfollowing_per_hour - actionCounter.hour_unfollows)
                else: print('not unfollowing, exceeded hourly limit')

                # follow
                if actionCounter.hour_follows < max_following_per_hour:
                    if actionCounter.hour_follows + follow < max_following_per_hour:
                        bot.follow(follow)
                    else:
                        bot.follow(max_following_per_hour - actionCounter.hour_follows)
                else: print('not following, exceeded hourly limit')

                # like
                if actionCounter.hour_likes < max_likes_per_hour:
                    if actionCounter.hour_likes + follow < max_likes_per_hour:
                        bot.hashtag_like_and_comment(like)
                    else:
                        bot.follow(max_likes_per_hour - actionCounter.hour_likes)
                else: print('not liking, exceeded hourly limit')

                #bot.get_following_list(700)
                bot.DM_youtube(DM, 'https://www.youtube.com/watch?v=ivzsS7iV_JQ')
                stop_timer = time.perf_counter()

                if not printLog:
                    sys.stdout = sys.__stdout__
                    with open ('test.txt', 'w') as testfile:
                        testfile.write(text_trap.getvalue())
                seconds = round((stop_timer - start_timer), 3)
                print("cycle time: ", round(int(seconds)/60, 3), 'minutes')
                sleep(random.randrange(250, 300))
        except Exception as e:
            print(e)

                


bot = Instabot(keys.username, keys.password)
# bot.get_NFB_list()


# bot.get_following_list(1000)
# bot.cycle(unfollow, follow, likes, DM)
LongCycle = False
# bot.cycle(0, 0, 0, 10, True)
bot.cycle(0, 0, 30, 7, continuous = True, printLog = True)


importlib.reload(actionCounter)
print('$$$ total actions today: '+ str(actionCounter.daily_actions) + ' $$$')