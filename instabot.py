from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import numpy as np
import random, re, datetime, importlib
# local files
import keys, actionCounter

PATH = 'C:\Program Files (x86)\chromedriver.exe'

def naturalSleep(value):
    deviation = 0.6
    upperBound,lowerBound = round(value + value*deviation), round(value - value*deviation)
    newVal = random.randrange(lowerBound, upperBound)
    sleep(newVal)

def oneAction(actionType):
    importlib.reload(actionCounter)
    now = datetime.datetime.now()
    today = now.strftime('%m.%d')

    if actionCounter.date == today: actionCounter.daily_actions += 1
    else: actionCounter.daily_actions = 1

    if actionType == 'like': actionCounter.total_likes += 1
    elif actionType == 'comment': actionCounter.total_comments += 1
    elif actionType == 'follow': actionCounter.total_follows += 1
    elif actionType == 'unfollow': actionCounter.total_unfollows += 1
    
    if actionCounter.date == today: 
        print('actions: '+ str(actionCounter.daily_actions))
        if actionCounter.daily_actions > 500: print('exceeded 500 actions today')
    else: print('new date')

    f = open("actionCounter.py", "w")
    f.write("date = '"+ str(today) + "'\n")
    f.write('daily_actions = ' + str(actionCounter.daily_actions) + '\n')
    f.write('total_likes = ' + str(actionCounter.total_likes) + '\n')
    f.write('total_comments = ' + str(actionCounter.total_comments) + '\n')
    f.write('total_follows = ' + str(actionCounter.total_follows) + '\n')
    f.write('total_unfollows = ' + str(actionCounter.total_unfollows) + '\n')
    f.close()



class Instabot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get('https://instagram.com')
        sleep(3)
        #initial login info
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')\
            .send_keys(username)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')\
            .send_keys(password)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div')\
            .click()
        sleep(3)
        #save login
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/section/div/button').click()
        sleep(2.5)
        #notification
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        sleep(1)
        

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
        btn = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')
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
        print('Ratio:', ratio)
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
        file = open("follower_list.txt","r+")
        file. truncate(0)
        file. close()

        #generating names from each element
        print('end of scrolling, generating followers list...')
        followerList = scrollBox.find_elements_by_tag_name('a')
        appendFile = open('follower_list.txt', 'a')
        for item in followerList:
            if item.text != '': appendFile.write(item.text + ',')
        appendFile.close()
            
        print('follower list generated!')
        #close followers tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
            .click()


    def get_following_list(self):
        #click on instagram icon to return home
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img')\
            .click()
        #click open profile
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a')\
            .click()
        sleep(4)
        #obtain follower count
        followingCount = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').text.split(' ')[0]
        followingCount = ''.join(followingCount.split(','))
        print(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').text)
        #click on following list
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')\
            .click()
        sleep(2)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')

        #scrolling
        bot.scrolling(int(followingCount) - 2, '/html/body/div[4]/div/div/div[2]', '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')

        #clear previous data on the following text file
        file = open("following_list.txt","r+")
        file. truncate(0)
        file. close()

        #generating names from each element
        print('end of scrolling, generating following list...')
        followingList = scrollBox.find_elements_by_tag_name('a')
        appendFile = open('following_list.txt', 'a')
        for item in followingList:
            if item.text != '': appendFile.write(item.text + ',')
        appendFile.close()
            
        print('following list generated!')
        #close following tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div/div[2]/button')\
            .click()
       
    def not_following_back_list(self):
        #followers
        file = open("follower_list.txt","r")
        followerNames = file.read().split(',')
        #following
        file = open("following_list.txt","r")
        followingNames = file.read().split(',')
        not_following_back = np.setdiff1d(followingNames, followerNames)
        appendFile = open('not_following_back.txt', 'w')
        for item in not_following_back:
            appendFile.write(item + ',')
        appendFile.close()
        print('list of not following back users compiled:', len(not_following_back), 'total users')

    def unfollow_NFB(self, count):
        file = open("not_following_back.txt","r")
        not_following_back = file.read().split(',')
        i = 0
        while i < count:
            name = not_following_back[i]
            self.driver.get('https://instagram.com/' + name)
            naturalSleep(4)
            try:
                naturalSleep(6)
                self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div/span')\
                .click()
                naturalSleep(6)
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
                oneAction('unfollow')
                not_following_back.remove(name)
                i += 1
                print(i, '/', count, 'successfully unfollowed:', name)
                
            except NoSuchElementException:
                # check if following option exist for public users
                if self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button') != []:
                    print('already unfollowed user:', name)
                    not_following_back.remove(name)
                # check if following option exist for private users
                elif self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/button') != []:
                    print('already unfollowed user:', name)
                    not_following_back.remove(name)
                else: print('error')
                sleep(2)

        file.close()
        appendFile = open("not_following_back.txt","w")
        for item in not_following_back:
            appendFile.write(item + ',')
        appendFile.close()
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
            print(userList)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)

            for names in userList:
                print('User:', names)
                self.driver.get('https://instagram.com/' + names)
                naturalSleep(4)
                ratio, follower = bot.ratio()
                naturalSleep(4)

                # randomly like their post and follower othsers that liked the post
                if ratio >= 0.5 and ratio < 1.1 and int(follower) > 150:
                    # clicking on their follower list
                    self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
                    sleep(4)
                    bot.scrolling(int(follower) - 2, '/html/body/div[4]/div/div/div[2]', '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
                    scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
                    followerList = scrollBox.find_elements_by_tag_name('a')
                    followerNameList = [item.text for item in followerList]

                    for item in followerNameList:
                        if item != '' and item != 'ivrz.fpv':
                            print(item)
                            self.driver.get('https://instagram.com/' + item)
                            naturalSleep(10)
                            # currently not following private accounts
                            already_following = self.driver.find_elements_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
                            # check their ratio
                            ratio, follower = bot.ratio()
                            if np.size(already_following) > 0 and ratio < 1.2 and followed < amount:
                                # click on follow
                                self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')\
                                    .click()
                                oneAction('follow')
                                followed += 1
                                print('follwed', followed, 'users')
                                try:
                                    posts = self.driver.find_elements_by_tag_name('a')
                                    hrefs = [item.get_attribute('href') for item in posts
                                                if '.com/p/' in item.get_attribute('href')]
                                    if len(hrefs) < 12:
                                        likes = len(hrefs)
                                    else:
                                        likes = random.randint(6, 12)

                                    for i in range(likes):
                                        self.driver.get(hrefs[i])
                                        naturalSleep(5)
                                        if bot.unique_post() == True:
                                            self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')\
                                                .click()
                                            oneAction('like')
                                            naturalSleep(5)
                                    print('finished liking', likes, 'posts')
                                except Exception:
                                    print('failed to like post')
                            else:
                                print('already following')
                            sleep(5)
                    print('iteration complete')
                    sleep(500) 

    def hashtag_like_and_comment(self, amount):
        file = open("hashtags.txt","r")
        hashtags = file.read().split(',')
        List = []
        for item in hashtags:
            List.append(item)
        hashtag_list = random.sample(List, len(List))
        print(hashtag_list)
        file.close()
        count = 0
        i = 0
        while count < (amount - 14):
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
            print(str(len(hrefs)) + ' posts detected')
            naturalSleep(8)
            
            for item in target_posts:
                self.driver.get(item)
                naturalSleep(25)

                if bot.unique_post() == True:
                    #liking post
                    self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')\
                        .click()
                    count += 1
                    oneAction('like')
                    naturalSleep(10)

                    #commenting post
                    if random.randint(0,12) < 4:
                        file = open("comments.txt","r")
                        comments = file.read().split(',')
                        self.driver.find_element_by_class_name('Ypffh').click()
                        sleep(1)
                        self.driver.find_element_by_class_name('Ypffh').send_keys(comments[random.randrange(0,len(comments))])
                        sleep(1)
                        self.driver.find_element_by_class_name('Ypffh').send_keys(Keys.ENTER)
                        oneAction('comment')
                        file.close()
                        naturalSleep(15)
                    print('count: ' + str(count))
                else:
                    print('post already interacted')

            
    def get_NFB_list(self):
        try:
            bot.get_follower_list()
            print('updated follower list')
            bot.get_following_list()
            print('updated following list')
            bot.not_following_back_list()
            print('---updated NFB list---')
        except:
            print('failed, try again later')
    
 
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                




bot = Instabot(keys.username, keys.password)
# bot.get_NFB_list()

# bot.unfollow_NFB(30)
bot.follow(30)
# bot.hashtag_like_and_comment(400)

import actionCounter
print('total actions today: '+ str(actionCounter.daily_actions))