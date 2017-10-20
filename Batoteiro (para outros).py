# -*- coding: utf-8 -*-
from selenium import webdriver
import selenium
import time
import copy

def cheater(numPag=0, minMon=0, username=0, password=0):
    driver = logIn(username, password)
    H = True
    while H:
        H = pageSearch(driver, numPag, minMon)
    recruitment(driver)
    driver.Dispose()
    print 'Batoteiro, o teu programa é brutal ;D'

def logIn(nameString, passString):
    driver = webdriver.Firefox()
    pag = driver.get("http://www.darkthrone.com")
    #login
    username = driver.find_element_by_name("user[email]")
    password = driver.find_element_by_name("user[password]")
    if nameString and passString:
        username.send_keys(nameString)
        password.send_keys(passString)        
    else:
        username.send_keys(raw_input("username: "))
        password.send_keys(raw_input("password: "))
    driver.find_element_by_class_name("submitbtn").click()
    return driver
    
def pageSearch(driver, numPag, minMon):
    directions = ['Previous', 'Next']
    chgDir = True
    targets =[]
    me = []
    count = 0
    driver.get("http://www.darkthrone.com/userlist/attack")
    #my data
    myId = int(driver.page_source.split("== 'character_")[1].split("'){")[0])
    myName = driver.page_source.split(str(myId))[2].split('">')[1].split('</a>')[0]
    myArmy = int(driver.page_source.split(str(myId))[2].split('<td><!--')[2].split('-->')[0])
    myLevel = int(driver.page_source.split(str(myId))[2].split('-->')[3].split('</td>')[0])
    me = [myArmy, myLevel, myId]
    print 'exercito:', myArmy, '\tnivel: ', myLevel, '\tnome: ', myName, '\tID: ', myId, '\n'
    inLevel = True
    while directions and ((numPag == 0) or (numPag > count)):
        if not inLevel:
            driver.get("http://www.darkthrone.com/userlist/attack")
            directions.remove(directions[0])
            if not directions:
                break
            driver.find_element_by_link_text(directions[0]).click()
        chunks = driver.page_source.split('<tr>')
        for i in chunks:
            #is a player?
            if 'href="/viewprofile/index' in i:
                level = int(i.split('-->')[5].split('</td>')[0])
                inLevel = abs(level - me[1]) < 3
                if inLevel:
                    targets.extend(qualify(driver.page_source, me, minMon))
                    driver.find_element_by_link_text(directions[0]).click()
                    break
        count += 1
    targets.sort(reverse=True)
    attackTarget(driver, targets)
    return len(targets)
    

def qualify(raw_page, me, minMon):
    players = []
    qualified = []
    inactive = open('inactive.txt', 'r')
    marked = copy.copy(inactive.read())
    inactive.close()
    chunks = raw_page.split('<tr>')
    for i in chunks:
        if 'href="/viewprofile/' in i:
            players.append(i.split('</tr>')[0])
    for i in players:
        money = int(i.split('<td><!--')[2].split('-->')[0])
        army = int(i.split('<td><!--')[3].split('-->')[0])
        level = int(i.split('-->')[5].split('</td>')[0])
        if money > minMon and army < me[0] and abs(level - me[1]) < 3:
            profile = int(i.split('/viewprofile/index/')[1].split('?')[0].split('" id')[0])
            inList =  str(profile) in marked
            if not inList:
                qualified.append([money, profile, army, level])
    inactive.close()
    return qualified
    
def attackTarget(driver, targets):
    count = 0
    badPlayers = ''
    victory = False
    chunk = driver.page_source.split('Turns Available: <br>')[1].split('</div>')[0].replace(',','')
    turns = [int(s) for s in chunk.split() if s.isdigit()][0] / 10
    for i in targets:
        print 'id ', i[1], '\t\t', i[0] / 1000000, 'K€'
    if min(len(targets), turns) > 0:
        print min(len(targets), turns), 'serão atacados\n'
    while (count < len(targets)) and turns:
        print count + 1, 'º target: ', targets[count]
        driver.get('http://www.darkthrone.com/viewprofile/index/' + str(targets[count][1]))
        if 'This user is inactive' not in driver.page_source:
            try:
                driver.find_element_by_link_text('Attack This Player').click()
                attackTurns = driver.find_element_by_name("turns")
                attackTurns.send_keys('10')
                driver.find_element_by_class_name("button_attack").click()
                if 'You have defeated' in driver.page_source:
####                    time.sleep(10)
##                    value = driver.page_source.split('You pillaged <span class="green">')[1].split['</span> gold and'][0]
                    print '************\tVICTÓRIA\t************\n'#Gold pillaged: ', value
                    victory = True
                elif 'has defeated you!' in driver.page_source:
                    print '# derrota #'
            except Exception as a:
                print Exception
                print a
        else:
            badPlayers += str(targets[count][1]) + '\n'
            print '...está inátivo'
        chunk = driver.page_source.split('Turns Available: <br>')[1].split('</div>')[0].replace(',','')
        turns = [int(s) for s in chunk.split() if s.isdigit()][0] / 10
        count+=1
        print ''
    inactive = open('inactive.txt', 'a+')
    inactive.write(badPlayers)
    inactive.close()
    print '\nA tua Furia foi saciada'
##    if victory:
##        driver.get("http://www.darkthrone.com/bank")
##        time.sleep(10)
##        driver.find_element_class_name("button_deposit").click()
##        print 'Valores ganhos depositados'

def recruitment(driver=0):
    if not driver:
        time.sleep(10)
        driver = logIn(1)[0]
        time.sleep(10)
    driver.get('http://www.darkthrone.com/recruiter')
    time.sleep(10)
    text = 'You have reached the maximum'
    if text not in driver.page_source:
        driver.find_element_by_id("recruit_link").click()
        print 'Início do recrutamento...'
        while text not in driver.page_source:
            time.sleep(10)
            driver.find_element_by_id("recruit_link").click()
    print 'Fim do recrutamento!'
            
a = 13333333 #valor minimo para receber 10M por ataque                                          
cheater(0, a)
