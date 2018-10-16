# -*- coding: utf-8 -*-

from geral import *

def init(driver):
    train(driver)
    buy(driver)
            
def train(driver):
    print 'Treinando'
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
    UNITS = between('Citizens:</dt><dd>', '</dd>', driver)
##    if int(UNITS):
##        soldiers = driver.find_element_by_name("qty_c10")
##        soldiers.send_keys(UNITS)
##        workers = driver.find_element_by_name("qty_c2")
##        workers.send_keys(UNITS)
##        driver.find_element_by_name("train").click()
    return  UNITS
    
def buy(driver):
    driver.get("http://www.darkthrone.com/battleupgrades")
    banked = between("Banked Gold:</dt><dd>","</dd>", driver)
    hand = between("Hand:</dt><dd>","</dd>", driver)
    money = hand #+ banked
    #batle upgrades
    mSold = between('steeds. You have ',' of ', driver)
    mStee = int(driver.page_source.split(i)[0].split('center">')[2].split('<')[0].replace(',', ''))
    steeds = driver.find_element_by_name("qty_io_s16_0")
    steeds.send_keys(mStee - mSold)
##    driver.find_element_by_name("submitbtn").click()
    #armory
    """ this calculates the amount of money in bank and on hand
        and buy everything that it can with that money for all
        the soldiers"""
    driver.get("http://www.darkthrone.com/armory")
    attackers = between("Offensive Units:</dt><dd>","</dd>", driver)
    define = str(3)
    for i in [1,2,3,4,5,7]:
        item = "qty_io_s" + str(i) +"_" + define
        group = driver.page_source.replace(',', '').split(item)[0].split('center">')
        inventory = int(group[-4].split('</')[0])
        price = int(group[-3].split('</')[0])
        amount = money / price
        if amount < attackers - inventory:
            driver.find_element_by_name(item).send_keys(amount)
            money -= price * amount
    driver.find_element_by_name("buy").click()
    message = driver.page_source.split('"center">')[2].split('</td>')[0]
    if "Please select" not in message:
        print message
