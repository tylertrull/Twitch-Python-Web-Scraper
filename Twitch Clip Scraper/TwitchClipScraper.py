from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
import random
import threading
import subprocess
import autoit
from datetime import datetime
import glob
chrome_options = webdriver.ChromeOptions()
clipper_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--mute-audio")
driversList = []
todayDate = datetime.today().strftime('(%#m-%#d-%Y)')

def Scrape_Twitch_Category(twitchCategory):
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.implicitly_wait(10)
    category = twitchCategory.replace(" ", "%20")
    print(category)
    twitchLink = "https://www.twitch.tv/directory/game/{}/clips?range=24hr".format(category)
    clipLinks = []
    count = 11;
    try:
        driver.get(twitchLink)
        print("Opening {} clips...".format(twitchCategory))
        try:
            creatorFile = open("D:\BOT VIDEOS\Creators\{}.txt".format(twitchCategory), "x") 
            for i in range(1, 3):
                creator = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div/div/div/div[5]/div[1]/div/div/div/div[{}]/article/div[1]/div/div[1]/div[2]/p[1]/a'.format(i))
                creatorFile.write(creator.text + " ")
            creatorFile.close()
            for i in range(1,count):
                clipsQuery = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/main/div[2]/div[3]/div/div/div/div/div/div[5]/div[1]/div/div/div/div[{}]/article/div[2]/div'.format(i))  
                clipsQuery.click()
                print("Clicked clip")
                try:
                    clipLinks.append(driver.current_url)
                    driver.back()
                    time.sleep(0.5)
                    print("Got clip URL and clicked back")
                except:
                    print("Couldn't get link or go back")

            try:
                try:
                    driver.quit()
                    print("Closed URL driver")
                except:
                    print("Couldn't close URL driver")
                print("Opening clipper")
                clipper = webdriver.Chrome(chrome_options = setupClipper(twitchCategory))
                driversList.append(clipper)
                clipper.implicitly_wait(10)
                clipper.get("https://clipr.xyz/")
                for clips in clipLinks:
                    try:
                        clipper.find_element_by_xpath('//*[@id="clip_url"]').send_keys(clips)
                        print("Typing in URL")
                        try:
                            clipper.find_element_by_xpath('//*[@id="app"]/main/div[1]/div/div/div/div/form/button').click()
                            try:
                                downloadLinkBox = clipper.find_element_by_xpath('//*[@id="app"]/main/div[1]/div/div/div/div/div[2]/div[2]/div[1]/a[2]')
                                downloadLinkBox.click()
                                print("Clicking download link...")
                                backButton = clipper.find_element_by_xpath('//*[@id="app"]/main/div[1]/div/div/div/a')
                                backButton.click()
                                time.sleep(1)
                            except:
                                print("Couldn't find or click CLICK TO DOWNLOAD")
                        except:
                            print("Couldn't find or click GET DOWNLOAD LINK")
                    except:
                        print("Couldn't find urlBox")
            except:
                print("Couldn't open clipper... Exiting")
                sys._exit()
        except:
            print("Couldin't find clips")
    except:
        print("Could not open {}".format(twitchCategory))
    
    try:
        print("Finished getting files for {}".format(twitchCategory))
        
    except:
        print("Couldn't close driver")
    

def setupClipper(twitchCategory):
    the_clipper_options = webdriver.ChromeOptions()
    downloadFolder = 'D:/BOT VIDEOS/Clips/{}/'.format(twitchCategory)
    isFile = os.path.exists(downloadFolder)
    if not(isFile):
        try:
            os.mkdir(downloadFolder)
        except:
            print("Couldn't make directory for {}".format(twitchCategory))
    prefs = {'download.default_directory' : 'D:\BOT VIDEOS\Clips\{}\\'.format(twitchCategory)}
    the_clipper_options.add_experimental_option('prefs', prefs)
    return the_clipper_options


def uploadtoYoutube():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--windowsize==1920,1080")
    chrome_options.add_argument("--mute-audio")
    driver = webdriver.Chrome(chrome_options = chrome_options)
    gamesFile = open('C:/Users/Tyler/Documents/Twitch Clip Scraper/Games.txt')
    driver.implicitly_wait(10)
    email = "TwitchClipBot733733@gmail.com"
    password = "Thisisthetwitchclipbotpassword12"
    driver.get("https://www.youtube.com")
    signInButton = driver.find_element_by_xpath('//*[@id="buttons"]/ytd-button-renderer')
    signInButton.click()
    print("Signing in to Youtube...")
    emailTextBox = driver.find_element_by_xpath('//*[@id="identifierId"]')
    emailTextBox.send_keys(email)
    nextButton = driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/span')
    nextButton.click()
    passwordTextBox = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    passwordTextBox.send_keys(password)
    nextButton = driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/span')
    nextButton.click()
    print("Going to upload prompt...")
    createButton = driver.find_element_by_xpath('//*[@id="button"]/a')
    createButton.click()
    uploadLiveButton = driver.find_element_by_xpath('//*[@id="primary-text-container"]')
    uploadLiveButton.click()
    print("Selecting files to upload...")
    selectFilesButton = driver.find_element_by_xpath('//*[@id="burst"]')
    selectFilesButton.click()
    print("Autoit filling out Windows File Dialog...")
    autoit.win_wait_active("Open")
    autoit.send("D:\BOT VIDEOS\Processing")
    autoit.send("{Enter}")
    games = gamesFile.readlines()
    files = ""
    fileNames = open('D:\BOT VIDEOS\FileNames.txt')
    fileNames_lines = fileNames.readlines()
    
    for name in fileNames_lines:
        name = name.replace("\n","")
        files += '"{}'.format(name)
    autoit.send(files)
    print("Upload files")
    autoit.send("{Enter}")
    input("Press ENTER to finish upload...")
    driver.close()

def deleteFiles():
    print("Deleting Clip Files and Rendered Videos")
    #Remove Clip files
    files = glob.glob('D:\BOT VIDEOS\Clips\*.mp4')
    for f in files:
        os.remove(f)
    #Remove Rendered Videos
    files2 = glob.glob('D:\BOT VIDEOS\Processing\*.mp4')
    for f in files2:
        os.remove(f)
    #Remove Creators txt file
    files3 = glob.glob('D:\BOT VIDEOS\Creators\*.txt')
    for f in files3:
        os.remove(f)
    #Remove Filenames txt file
    os.remove("D:\BOT VIDEOS\FileNames.txt")
    print("Files deleted :)")
    
def main():
    print(todayDate)
    gamesFile = open('C:/Users/Tyler/Documents/Twitch Clip Scraper/Games.txt')
    readLines = gamesFile.readlines()
    threads = []
    for line in readLines:
        line = line.replace("\n", "")
        newThread = threading.Thread(target = Scrape_Twitch_Category, args =(line,))
        threads.append(newThread)

    for thread in threads:
        thread.start()

    for threadEnd in threads:
        threadEnd.join()

    print("Waiting for downloads and then Closing {} clippers".format(len(driversList)))
    time.sleep(5)
    for drivers in driversList:
        try:
            drivers.quit()
            print("Clipper closed")
        except:
            print("Couldn't close clipper :(")

    print("Opening Vegas Pro...")
    subprocess.run(["C:/Program Files/VEGAS/VEGAS Pro 16.0/vegas160.exe", "-SCRIPT:C:/Program Files/VEGAS/VEGAS Pro 16.0/Script Menu/RenderScript.cs"])
    print("Vegas Pro terminated")
    print("Opening Youtube...")
    uploadtoYoutube()
    deleteFiles()
    print("Enjoy :), sleeping 10 seconds and then closing")
    time.sleep(10)
    
if __name__ == "__main__":
    main()

