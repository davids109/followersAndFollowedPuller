import json
import sys
from bs4 import BeautifulSoup
import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Hi. this is a program made by davids109. it's function is to pull followers and people followed by from an instagram profile of your choosing.\nYou can input a private account, but if you do so you will be asked to input the credentials of an account that follows the account you wanna inspect.\nWhen the program will start, it will open a firefox window and start doing it's thing.\nthe data is then put on a .json file.\nAlso the program may not work on slower connections. i am working on implementation for dynamic waits.\nI do not take responsability if instagram action bans or suspends the account you are using.\n")


username = ""
password = ""
account = input("What account would you like to pull the followers from? ")
username = input("what is the username of the account you would like to use? ")
password = input("what is the password of the account you would like to use? ")
while 1==1:
    whatToPull = input("would you like to pull the followers or the followed? [followers/followed] ")
    if whatToPull == "followers":
        pull = 2
        break
    elif whatToPull == "followed":
        pull = 3
        break
    else:
        print("you didn't write the word correctly. please try again.")
input("thank you. press any key to start the program.")

driver = Firefox(executable_path='./geckodriver')

driver.get("https://www.instagram.com/"+account) #goes to the gram.
driver.implicitly_wait(5)
driver.find_element(By.CSS_SELECTOR, 'button.aOOlW:nth-child(1)').click() #eliminates invading popup
driver.find_element(By.CSS_SELECTOR, 'a.tdiEy:nth-child(1) > button:nth-child(1)').click() #entra nella page per fare il login
driver.implicitly_wait(5)
driver.find_element(By.CSS_SELECTOR, 'div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)').send_keys(username) #inserts the username
driver.find_element(By.CSS_SELECTOR, 'div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)').send_keys(password) #inserts the password
try:
    driver.find_element(By.CSS_SELECTOR, 'div.Igw0E:nth-child(3)').click() #confirms the login
except:
    input("Ops. something has gone wrong. please confirm the login manually.")

try:
    driver.find_element(By.CSS_SELECTOR, 'button.aOOlW:nth-child(1)').click()
except:
    pass
driver.implicitly_wait(3)

try:
    driver.find_element(By.CSS_SELECTOR, 'button.sqdOP:nth-child(1)').click() #confirms another invading popup
except:
    pass

driver.implicitly_wait(5)

javascript1 = "arguments[0].scrollIntoView(true);" 
perma = {}
seguito = []

n = 0
driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li['+ str(pull)+']/a').click() #entra nella lista dei seguiti
element = driver.find_element(By.CLASS_NAME, "PZuss")
for i in range(1, 1000):
    try:
        driver.execute_script(javascript1, seguito[i-1])
    except:
        print(str(i-1) + " accounts pulled")
        time.sleep(1)
        seguito = element.find_elements(By.TAG_NAME, "li")
        if n == len(seguito):
            print("breaking the loop.")
            break
        else:
            n = len(seguito)

innerHTML = element.get_attribute('innerHTML')
soup = BeautifulSoup(innerHTML, 'html.parser')
listitems = soup.find_all("li")
def follower(tag):
    return tag.has_attr('title') and tag.has_attr('tabindex') and tag.has_attr('href') 

perma[account] = soup.find_all(follower)

for i in range(len(listitems)):
    perma[account][i] = perma[account][i].get_text(strip=True)     

with open("data.json", "w") as outfile:
    json.dump(perma, outfile, indent=4)

print("made with <3 by davids109")
