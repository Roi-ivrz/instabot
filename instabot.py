from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import numpy as np
import random, re, datetime
# local files
import keys

PATH = 'C:\Program Files (x86)\chromedriver.exe'

def naturalSleep(value):
    deviation = 0.6
    upperBound,lowerBound = round(value + value*deviation), round(value - value*deviation)
    newVal = random.randrange(lowerBound, upperBound)
    sleep(newVal)

def oneAction():
    import actions_per_day
    now = datetime.datetime.now()
    today = now.strftime('%m.%d')

    if actions_per_day.date == today:
        actions_per_day.actions += 1
        print('date existing, actions: '+ str(actions_per_day.actions))
        f = open("actions_per_day.py", "w")
        f.write("date = '"+ str(today) + "'\n")
        f.write('actions = ' + str(actions_per_day.actions))
        f.close()
    else:
        print('new date')
        f = open("actions_per_day.py", "w")
        f.write("date = '"+ str(today) + "'\n")
        f.write('actions = 1')
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
        

    def scrolling_list(self, maxNum):
        actions = ActionChains(self.driver)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        nameLinks = 1
        while int(nameLinks) < int(maxNum):
            scrollBox.click()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            sleep(0.5)
            nameLinks = len(scrollBox.find_elements_by_class_name('FPmhX'))
            actions.send_keys(Keys.PAGE_DOWN).perform()
            print('current:', nameLinks, '/', maxNum, 'max')
            sleep(0.5)
        return scrollBox
    
    def liked_scrolling_list(self):
        actions = ActionChains(self.driver)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        iterations = 0
        while iterations <= 6:
            try:
                userToFollow = self.driver.find_elements_by_class_name('y3zKF')
                for item in userToFollow:
                    item.click()
            except Exception as e:
                sleep(0.1)
            item.click()
            sleep(5)
            scrollBox.click()
            actions.send_keys(Keys.PAGE_DOWN).perform()
            print(iterations)
            sleep(0.6)
            iterations += 1

    def unique_post(self):
        btn = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')
        aria_label = btn.find_element_by_css_selector('svg').get_attribute("aria-label")
        sleep(2)
        if aria_label == 'Like':
            return True
        else:
            return False


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
        sleep(2)
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')

        #scrolling
        bot.scrolling_list(followerCount)

        #clear previous data on the following text file
        file = open("follower_list.txt","r+")
        file. truncate(0)
        file. close()

        #generating names from each element
        print('end of scrolling, generating followers list...')   
        followerNameList = []
        followerList = scrollBox.find_elements_by_tag_name('a')
        appendFile = open('follower_list.txt', 'a')
        for item in followerList:
            if item.text != '':
                followerNameList.append(item.text)
                appendFile.write(item.text + ',')
        appendFile.close()
            
        print('follower list generated!')
        #close followers tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button')\
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
        scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')

        #scrolling
        bot.scrolling_list(followingCount)

        #clear previous data on the following text file
        file = open("following_list.txt","r+")
        file. truncate(0)
        file. close()

        #generating names from each element
        print('end of scrolling, generating following list...')   
        followingNameList = []
        followingList = scrollBox.find_elements_by_tag_name('a')
        appendFile = open('following_list.txt', 'a')
        for item in followingList:
            if item.text != '':
                followingNameList.append(item.text)
                appendFile.write(item.text + ',')
        appendFile.close()
            
        print('following list generated!')
        #close following tab
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button')\
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
        for item in range(count):
            name = not_following_back[item]
            self.driver.get('https://instagram.com/' + name)
            naturalSleep(10)
            
            try:
                self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div/span')\
                .click()
                naturalSleep(15)
                self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
                not_following_back.remove(name)
                print('successfully unfollowed', name)
            except Exception as e:
                print('******failed to unfollow user', name)
                not_following_back.remove(name)
            naturalSleep(10)
        file.close()
        appendFile = open("not_following_back.txt","w")
        for item in not_following_back:
            appendFile.write(item + ',')
        appendFile.close()
        print('successfully unfollowed', count, 'users')
      
    def follow(self):
        target_found = False
        while target_found == False:
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
                naturalSleep(10)
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
                ratio = abs(int(follower) - int(following)) / int(following)
                print('Ratio:', ratio)
                naturalSleep(10)

                #randomly like their post and follower others that liked the post
                if ratio <= 4 and int(follower) < 6000:
                    '''
                    posts = self.driver.find_elements_by_tag_name('a')
                    hrefs = [item.get_attribute('href') for item in posts
                                 if '.com/p/' in item.get_attribute('href')]
                    self.driver.get(hrefs[random.randrange(0,8)])
                    '''
                    self.driver.get('https://www.instagram.com/p/CAjx-dCnJwk/')
                    naturalSleep(6)
                    self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button')\
                            .click()
                    naturalSleep(10)
                    
                    self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[2]/div/div[2]/button')\
                        .click()
                    naturalSleep(12)
                    
                    bot.liked_scrolling_list()
            
                    target_found = True

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
            print('---------------switching to next hashtag: #' + hashtag_list[i] + '---------------')
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
            target_posts = random.sample(hrefs, random.randint(12,16))
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
                    oneAction()
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
                        oneAction()
                        file.close()
                        naturalSleep(15)
                    print('count: ' + str(count))
                else:
                    print('post already interacted')

            

    
 
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                




bot = Instabot(keys.username, keys.password)
# bot.get_follower_list()
# bot.get_following_list()
# bot.not_following_back_list()
# bot.unfollow_NFB(50)
# bot.follow()
bot.hashtag_like_and_comment(1000)

import actions_per_day
print('total actions today: '+ str(actions_per_day.actions))