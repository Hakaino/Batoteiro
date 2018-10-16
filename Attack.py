# -*- coding: utf-8 -*-
import copy

def fetch(numPag, minMon, driver):
    directions = ['Previous', 'Next']
    targets =[]
    for direction in directions:
        driver.get("http://www.darkthrone.com/userlist/attack")
        something = True
        if direction == 'Previous':
            #my data
            myId = between("id == 'character_", "'){", driver)
            myArmy = int(driver.page_source.split(str(myId))[2].split('<td><!--')[2].split('-->')[0])
            myLevel = between('Level: ', '<br', driver)
        else:
            driver.find_element_by_link_text(direction).click()
        while something:
            c1 = between("from levels ", " to ", driver)
            c2 = between(str(c1) + " to ", ".</p>", driver) + 1
            something = False
            for chunk in driver.page_source.split('<tr>'):
                #is a player?
                if 'href="/viewprofile/index' in chunk:
                    level = int(chunk.split('-->')[5].split('</td>')[0])
                    if level in range(c1, c2):
                        something = True #checks if the page has any player in range
                        subject = qualify(chunk, myArmy, minMon)
                        if subject:
                            targets.append(subject)
            driver.find_element_by_link_text(direction).click()  
    targets.sort(reverse=True)
    attackTarget(targets, driver)
    return len(targets)
    

def qualify(player, mArmy, minMon):
    inactive = open('inactive.txt', 'r')
    blackList = copy.copy(inactive.read())
    inactive.close()
    money = int(player.split('<td><!--')[2].split('-->')[0])
    army = int(player.split('<td><!--')[3].split('-->')[0]) / 1.0  #enemy army size
    if money > minMon and army < mArmy:
        profile = int(player.split('/viewprofile/index/')[1].split('?')[0].split('" id')[0])
        if str(profile) not in blackList:
            return([money, profile])
    return None
    
def attackTarget(targets, driver):
    count = 0
    chunk = driver.page_source.split('Turns Available: <br>')[1].split('</div>')[0].replace(',','')
    turns = [int(s) for s in chunk.split() if s.isdigit()][0] / 10
    gain = 0
    for i in targets:
        print 'id %d\t\t%dM€' %(i[1], i[0] / 1000000)
        gain += i[0]
    print '\nLucro estimado:\t%dM€' %(gain * 0.75 / 1000000)
    if min(len(targets), turns) > 0:
        print '%s alvos serão atacados\n' %(min(len(targets), turns))
    while (count < len(targets)) and turns:
        number= count + 1
        target = targets[count][1]
        print '%dº - %d' %(number, target)
        driver.get('http://www.darkthrone.com/viewprofile/index/' + str(targets[count][1]))
        if 'inactive' not in driver.page_source:
            if 'You may only attack a user 5 times within 24 hours' in driver.page_source:
                destroyed.append(target)
                print 'O pobre coitado já não aguenta mais'
                pass
            try:
                driver.find_element_by_link_text('Attack This Player').click()
                attackTurns = driver.find_element_by_name("turns")
                attackTurns.send_keys('10')
                driver.find_element_by_class_name("button_attack").click()
            except Exception as e:
                print str(e)
            if 'You have defeated' in driver.page_source:
                value = between('You pillaged <span class="green">', '</span>', driver)
                print '************\tVICTÓRIA\t************\n'
                victory = True
            else:
                print '????' #############\tDERROTA\t############'
        else:
            badPlayer = str(targets[count][1]) + '\n'
            inactive = open('inactive.txt', 'a+')
            inactive.write(badPlayer)
            inactive.close()
            print '___inátivo___'
        chunk = driver.page_source.split('Turns Available: <br>')[1].split('</div>')[0].replace(',','')
        turns = [int(s) for s in chunk.split() if s.isdigit()][0] / 10
        count+=1

        
def between(a, b, driver):
    return int(driver.page_source.split(a)[1].split(b)[0].replace(',', ''))

if __name__ == '__main__':
    print 'ssssss'
