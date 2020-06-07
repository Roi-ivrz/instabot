from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import numpy as np
import keys


PATH = 'C:\Program Files (x86)\chromedriver.exe'

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
        sleep(2.5)
        #save login
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/section/div/button').click()
        sleep(2.5)
        #notification
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()
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

    def get_follower_list(self):
        #click on instagram icon to return home
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div/img')\
            .click()
        #click open profile
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a')\
            .click()
        sleep(2)
        #obtain follower count
        followerCount = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').text.split(' ')[0]
        followerCount = ''.join(followerCount.split(','))
        print(self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').text)
        #open follower tab
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')\
            .click()
        sleep(2)
        #scrollBox = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')

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
                appendFile.write(item.text + ', ')
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
        sleep(2)
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
                appendFile.write(item.text + ', ')
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
            appendFile.write(item + ', ')
        appendFile.close()
        print(not_following_back)

    def unfollow_NFB(self, count):
        file = open("not_following_back.txt","r")
        not_following_back = file.read().split(',')
        for i in range(count):
            self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div')\
                .click()
            sleep(2)
            self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div')\
                .send_keys('bruh')
            print(not_following_back[i])
            sleep(40)
            self.driver.find_elements_by_class_name('Ap253').click()
            
            




bot = Instabot(keys.username, keys.password)
#bot.get_follower_list()
bot.get_following_list()
#bot.not_following_back_list()
#bot.unfollow_NFB(2)