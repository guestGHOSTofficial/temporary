#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:10:26 2020

@author: b
"""

path = "/Ressources/Logfiles+Films/"
logfile1 = "film1csv.csv"

def analyzeLog(path, filename):
    f = open(path+filename, "r")
    out = open(path+"test_analyzed_"+filename,"w")
    line=f.readline()
    strng = 'Guid'
    maneuver = 'unassigned; '
    command = [0,0]
    offset = 0
    while(line):
        output = ''
        where_guid = line.find(strng)
        if(where_guid >= 0):
            #print 'guid found'
            if (line.find('/FOLLOW') >= 0):
                maneuver = "GoStraight; "
                command[0] = 0 + offset
            where_pic = line.find('/TURN_SINGLE_')     #all the turns except uturns
            if (where_pic >= 0):
               # print 'turn single'
                if(line[where_pic+13:where_pic+15] == '00'):       #'/TURN_SINGLE_ is 13 long
                    maneuver = "GoStraight; "
                    command[0] = 0 + offset
                elif(line[where_pic+13:where_pic+14] == '3'):
                    maneuver = "GoSlightLeft; "
                    command[0] = 1 + offset
                elif(line[where_pic+13:where_pic+14] == '2'):
                    maneuver = "GoLeft; "
                    command[0] = 2 + offset
                elif(line[where_pic+13:where_pic+15] == '04'):
                    maneuver = "GoSlightRight; "
                    command[0] = 4 + offset
                elif((line[where_pic+13:where_pic+15] == '09')|(line[where_pic+13:where_pic+15] == '13')):
                    maneuver = "GoRight; "
                    command[0] = 5 + offset
            else:
                where_pic = line.find('/UTURN_')
                if (where_pic >= 0):
                    if(line[where_pic + 7:where_pic + 8] == 'L'):
                        maneuver = "GoUturnLeft; "
                        command[0] = 3 + offset
                    elif(line[where_pic + 7:where_pic + 8] == 'R'):
                        maneuver = "GoUturnRight; "
                        command[0] = 6 + offset
            where_step = line.find( 'guideStep: NONE')
            if(where_step>=0):
                command[0] = -1
                output = str(line.split(',')[2]) + '; None; ' + maneuver + str(command) + '\n'
            else:
                where_step = line.find( 'guideStep: PREPARATION') 
                if(where_step >= 0):
                    command[1] = 0
                    output =str(line.split(',')[2]) + '; Preparation; ' + maneuver + str(command) + '\n'
                else:
                    where_step = line.find('guideStep: APPROACH')
                    if(where_step >= 0):
                        command[1] = 1
                        output =str(line.split(',')[2]) + '; Approach; ' + maneuver + str(command) + '\n'
                    else:
                        where_step = line.find('guideStep: ACTION')
                        if(where_step >= 0):
                            command[1] = 2
                            output =str(line.split(',')[2]) + '; Action; ' + maneuver + str(command) + '\n'
            if(output):
                out.write(output)
            #else:
            #    out.write("guid found, but no definite instructions: " + line)
        line=f.readline()
    f.close()
    out.close()
    
analyzeLog(path,logfile1)