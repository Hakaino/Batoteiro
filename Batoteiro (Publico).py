#! /usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import selenium
import time
import copy
import Attack
import Spend

victory = False
destroyed = []
driver = None


def main(numPag=0, minMon=0, username=0, password=0, rounds=100):
    
    global driver
    global victory
    logIn(username, password)
    #attack
    print ('\nAlvo\t\t\tQuantia')
    Attack.fetch(numPag, minMon, driver)
    #buy
    buy()
    #bank
    deposit()
    #train
    UNITS = train()
    #Recrutamento
    recruitment()
    print ('Batoteiro, o teu programa é brutal ;D')

def logIn(nameString, passString):
    global driver
    driver = webdriver.Firefox()
    pag = driver.get("http://www.darkthrone.com")
    #login
    username = driver.find_element_by_name("user[email]")
    password = driver.find_element_by_name("user[password]")
    username.send_keys(nameString)
    password.send_keys(passString) 
    driver.find_element_by_class_name("submitbtn").click()
    time.sleep(5)

def recruitment():
    print ('Recrutando')
    global driver
    driver.get('http://www.darkthrone.com/recruiter')
    time.sleep(10)
    text = 'You have reached the maximum'
    if text not in driver.page_source:
        t = time.time()
        driver.find_element_by_id("recruit_link").click()
        while text not in driver.page_source:
            try:
                driver.find_element_by_id("recruit_link").click()
            except WebDriverException as e:
                print ('>>> '), e
                pass
        print ('\nO recrutamento demorou %fm\n') %(time.time() - t) / 60
            
def train():
    print ('Treinando')
    global driver
    #mercenaries
    driver.get("http://www.darkthrone.com/mercenaries")
    driver.find_element_by_name("buy_all").click()
    #untrain
    driver.get("http://www.darkthrone.com/training")
    name = ["qty_c3", "qty_c4", "qty_c5", "qty_c6"]
    for i in name:
        job = driver.find_element_by_name(i)
        job.send_keys(int(driver.page_source.split(i)[0].split('middle">')[-3].split('<')[0].replace(',', '')))
    driver.find_element_by_name("untrain").click()
    #train
    UNITS = between('Citizens:</dt><dd>', '</dd>')
##    soldiers = driver.find_element_by_name("qty_c10")
##    soldiers.send_keys(UNITS)
    workers = driver.find_element_by_name("qty_c2")
    workers.send_keys(UNITS)
##    guards = driver.find_element_by_name("qty_c2")
##    guards.send_keys(UNITS)
    driver.find_element_by_name("train").click()
    return  UNITS
    
def buy():
    global driver
    global UNITS
    #armory
    """ this calculates the amount of money in bank and on hand
        and buy everything that it can with that money for all
        the soldiers"""
    driver.get("http://www.darkthrone.com/armory")
    offensive = between("Offensive Units:</dt><dd>","<")
    defensive = between("Defensive Units:</dt><dd>","<")
    banked = between("Banked Gold:</dt><dd>","<")
    hand = between("Hand:</dt><dd>","<")
    define = str(3)
    money = hand # + banked
    for Type in [("qty_id_s", defensive), ("qty_io_s", offensive)]:
        for i in [1,2,3,4,5,7]:
            item = Type[0] + str(i) +"_" + define
            group = driver.page_source.replace(',', '').split(item)[0].split('center">')
            inventory = int(group[-4].split('</')[0])
            price = int(group[-3].split('</')[0])
            amount = money / price
            if (amount < Type[1] - inventory) and (amount > 0):
                driver.find_element_by_name(item).send_keys(amount)
                money -= price * amount
    driver.find_element_by_name("buy").click()
    message = driver.page_source.split('"center">')[2].split('</td>')[0]
    if "Please select" not in message:
        print (message.replace('\t',''))
    
    #batle upgrades
##    driver.get("http://www.darkthrone.com/battleupgrades")
##    Type = ["qty_io_s16_0", "qty_id_s16_0"]
##    x = ['Steed ']
##    for i in range(len(Type)):
##        man = driver.page_source.split('You have ')[i].split(' of these')[0]
##        item =
##        if man > item:
##            dif = man - item
##            buy = driver.find_element_by_name(Type[i])
##            buy.send_keys(dif)
            
##    steeds = driver.find_element_by_name("qty_io_s16_0")
##    steeds.send_keys(UNITS)
##    driver.find_element_by_name("submitbtn").click()
        
def deposit():
    global driver
    value = 30 * (10 ** 6)
    driver.get("http://www.darkthrone.com/bank")
    enough = True
    if between('Remaining:</strong>', '</p>') and enough:
        driver.find_element_by_name("deposit").click()
        enough = between('Gold: ', '<') > value
        print ('> Depositado')
        
def between(a, b, integrer=True):
    global driver
    if integrer:
        
        value = int(driver.page_source.split(a)[1].split(b)[0].replace(',', ''))
    else:
        value = driver.page_source.split(a)[1].split(b)[0].replace('\t', '').replace('\n', '')
    return value

def Shoping(n, p):
    logIn(n, p)
    buy()

nameString = raw_input("username: ")
passString = raw_input("password: ")
                                          
if __name__ == '__main__':
##    Shoping(nameString, passString)
    main(0, 13333333, nameString, passString)
