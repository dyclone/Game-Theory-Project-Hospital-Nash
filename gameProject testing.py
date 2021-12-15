# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 13:36:45 2021

@author: dcsab
"""

import numpy as np
import math
import random

#function to get user input about game variables
def game_Elements():
    mask_Res = int(input("Please input the number of available mask resources:"))
    vent_Res = int(input("Please input the number of available ventilator resources:"))
    
    print("\n\nFor each player state the amount of resource!")
    play1_masks = int(input("Please input the amount of masks Player 1 wants:"))
    play1_vents = int(input("Please input the amount of ventilators Player 1 wants:"))
    
    play2_masks = int(input("\n\nPlease input the amount of masks Player 2 wants:"))
    play2_vents = int(input("Please input the amount of ventilators Player 2 wants:"))
    
    return mask_Res, vent_Res, play1_masks, play1_vents, play2_masks, play2_vents, None, None

#Utility Function for when both players choose the same action
def utility2PG_PayoffBOTH(game_Masks, game_Vents, p1_masks_given, p1_masks_Request, p1_vents_given, p1_vents_Request,\
                     p2_masks_given, p2_masks_Request, p2_vents_given, p2_vents_Request, action, p1ORp2):
        if action == "MM":
            if p1ORp2 == "p1":
                return (p1_masks_Request - ((game_Masks * 0.5) + p1_masks_given))\
                       - ((p1_vents_Request - p1_vents_given) + (0.25 * (p2_masks_Request - ((game_Masks * 0.5) + p2_masks_given))))
            else:
                return (p2_masks_Request - ((game_Masks * 0.5) + p2_masks_given))\
                       - ((p2_vents_Request - p2_vents_given) + (0.25 * (p1_masks_Request - ((game_Masks * 0.5) + p1_masks_given))))
        else:
            if p1ORp2 == "p1":
                return (p1_vents_Request - ((game_Vents * 0.5) + p1_vents_given))\
                       - ((p1_masks_Request - p1_masks_given) + (0.25 * (p2_vents_Request - ((game_Vents * 0.5) + p2_vents_given))))
            else:
                return (p2_vents_Request - ((game_Vents * 0.5) + p2_vents_given))\
                       - ((p2_masks_Request - p2_masks_given) + (0.25 * (p1_vents_Request - ((game_Vents * 0.5) + p1_vents_given))))

#Utility Function for when each players choose a different action
def utility2PG_PayoffMixed(game_Masks, game_Vents, p1_masks_given, p1_masks_Request, p1_vents_given, p1_vents_Request,\
                     p2_masks_given, p2_masks_Request, p2_vents_given, p2_vents_Request, action, p1ORp2):
        
        if action == "MV":
            if p1ORp2 == "p1":
                return (p1_masks_Request - (game_Masks + p1_masks_given))\
                       - ((p1_vents_Request - p1_vents_given) + (0.25 * (p2_vents_Request - (game_Vents + p2_vents_given))))
            else:
                return (p2_vents_Request - (game_Vents + p2_vents_given))\
                       - ((p2_masks_Request - p2_masks_given) + (0.25 * (p1_masks_Request - (game_Masks + p1_masks_given))))
        else:
            if p1ORp2 == "p1":
                return (p1_vents_Request - (game_Vents + p1_vents_given))\
                       - ((p1_masks_Request - p1_masks_given) + (0.25 * (p2_masks_Request - (game_Masks + p2_masks_given))))
            else:
                return (p2_masks_Request - (game_Masks + p2_masks_given))\
                       - ((p2_vents_Request - p2_vents_given) + (0.25 * (p1_vents_Request - (game_Vents + p1_vents_given))))

#Create Game Matrix with each cell being the payoff of choosing an action
def create_Matrix2PG(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want):
    
    p1_c1 = utility2PG_PayoffBOTH(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "MM", "p1")
    p2_c1 = utility2PG_PayoffBOTH(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "MM", "p2")
    p1_c2 = utility2PG_PayoffMixed(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "MV", "p1")
    p2_c2 = utility2PG_PayoffMixed(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "MV", "p2")
    p1_c3 = utility2PG_PayoffMixed(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "VM", "p1")
    p2_c3 = utility2PG_PayoffMixed(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "VM", "p2")
    p1_c4 = utility2PG_PayoffBOTH(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "VV", "p1")
    p2_c4 = utility2PG_PayoffBOTH(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                     p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want, "VV", "p2")
    cell_1 = str(p1_c1) + "," + str(p2_c1)
    cell_2 = str(p1_c2) + "," + str(p2_c2)
    cell_3 = str(p1_c3) + "," + str(p2_c3)
    cell_4 = str(p1_c4) + "," + str(p2_c4)
    return np.array([[cell_1, cell_2],[cell_3, cell_4]])


#Finds player 1s best responses
def playerA_best(a_matrix):
    #Initalize Variables
    rows = a_matrix.shape[0]
    columns = a_matrix.shape[1]
    row_num = 0
    col_num = 0
    A_Best_Responses = []
    A_choice = -999
    row_best_num = ""
    
    #Loop through Matrix to find best responses for Player A
    while col_num < columns:
        while row_num < rows:
            matrix_ele = a_matrix[row_num][col_num].split(",")
            if (float(matrix_ele[0]) > A_choice):
                A_choice = float(matrix_ele[0])
                row_best_num = str(row_num)
            elif (float(matrix_ele[0]) == A_choice):
                row_best_num += str(row_num)
            row_num += 1
        #Update List
        for x in row_best_num:
            A_Best_Responses.append(x + "," + str(col_num))
        
        #Reset Variables
        A_choice = -999
        row_best_num = ""
        row_num = 0
        #Increment Variable
        col_num += 1
    return A_Best_Responses


#Finds player 2s best repsonses
def playerB_best(a_matrix):
    #Initalize Variables
    rows = a_matrix.shape[0]
    columns = a_matrix.shape[1]
    row_num = 0
    col_num = 0
    B_Best_Responses = []
    B_choice = -999
    col_best_num = ""
    
    #Loop through Matrix to find best responses for Player B
    while row_num < rows:
        while col_num < columns:
            matrix_ele = a_matrix[row_num][col_num].split(",")
            if (float(matrix_ele[1]) > B_choice):
                B_choice = float(matrix_ele[1])
                col_best_num = str(col_num)
            elif (float(matrix_ele[1]) == B_choice):
                col_best_num += str(col_num)
            col_num += 1
        #Update List
        for x in col_best_num:
            B_Best_Responses.append(str(row_num) + "," + x)
        
        #Reset Variables
        B_choice = -999
        col_best_num = ""
        col_num = 0
        #Increment Variable
        row_num += 1
    return B_Best_Responses


#Find Nash Equilibrium 
def findNash(playerA_Best_List, playerB_Best_List):
    nash = list(set(playerA_Best_List) & set(playerB_Best_List))
    
    if len(nash) == 0:
        return random.choice(["0,0", "0,1", "1,0","1,1"])
    elif len(nash) == 1:
        return nash[0]
    elif len(nash)>= 2:
        return random.choice(nash)

#Find out how much a player is over resources
def reduceAmount(given, need):
    return given - need
 
#When there are no more resources end the second game or continue
def resources_gone(num_masks, num_vents):
    if num_masks == 0 and num_vents == 0:
        return False 
    else: 
        return True

#Set up the variables for second game based on amount of resources left
def sec_Variables(left_masks, left_vents):
    if left_masks >= 20 and left_vents >= 20:
        game_Masks = math.floor(left_masks * 0.1)
        game_Vents = math.floor(left_vents * 0.1)
        g_counter = 10
        left_masks = left_masks % 10
        left_vents = left_vents % 10
        #print("1st if")
    elif left_masks < 20 and left_vents >= 20:
        game_Masks = 0
        game_Vents = math.floor(left_vents * 0.1) 
        g_counter = 10
        left_masks = left_masks
        left_vents = left_vents % 10
        #print("2nd if)")
    elif left_masks >= 20 and left_vents < 20:
        game_Masks = math.floor(left_masks * 0.1)
        game_Vents = 0
        g_counter = 10
        left_masks = left_masks % 10
        left_vents = left_vents 
        #print("3rd if")
    elif (left_masks < 20 and left_masks != 0 and left_masks != 1 and left_masks != 3)\
        and (left_vents < 20 and left_vents != 0 and left_vents != 1 and left_vents != 3):
        game_Masks = math.floor(left_masks / 2)
        game_Vents = math.floor(left_vents / 2)
        g_counter = 2
        left_masks = left_masks % 2
        left_vents = left_vents % 2
        #print("4th if")
    elif left_masks == 3 and left_vents == 3:
        game_Masks = 2
        game_Vents = 2
        g_counter = 1
        left_masks = 1
        left_vents = 1
    elif left_masks == 3 and (left_vents < 20 and left_vents != 3):
         #print("5th if")
         if left_vents == 0 or left_vents == 1:
             game_Masks = 2
             game_Vents = 0
             g_counter = 1
             left_masks = 1
             left_vents = left_vents
             #print("inner if")
         else:
             game_Masks = 0
             game_Vents = math.floor(left_vents / 2) 
             g_counter = 2
             left_masks = left_masks
             left_vents = left_vents % 2
             #print("inner else")
    elif (left_masks < 20 and left_masks != 3) and left_vents == 3:
         #print("6th if")
         if left_masks == 0 or left_masks == 1:
             game_Masks = 0
             game_Vents = 2
             g_counter = 1
             left_masks = left_masks
             left_vents = 1
             #print("inner if")
         else:
             game_Masks = math.floor(left_masks / 2) 
             game_Vents = 0
             g_counter = 2
             left_masks = 1
             left_vents = left_vents
             #print("inner else")
    elif (left_masks < 20 and left_masks != 0 and left_masks != 1 and left_masks != 3)\
        and (left_vents == 0 or left_vents == 1):
        game_Masks = math.floor(left_masks / 2)
        game_Vents = 0
        g_counter = 2
        left_masks = left_masks % 2
        left_vents = left_vents
    elif (left_masks == 0 or left_masks == 1)\
        and (left_vents < 20 and left_vents != 0 and left_vents != 1 and left_vents != 3):
        game_Masks = 0
        game_Vents = math.floor(left_vents / 2)
        g_counter = 2
        left_masks = left_masks 
        left_vents = left_vents % 2
    else:
        #print("final else")
        game_Masks = 0
        game_Vents = 0
        g_counter = 0
        left_masks = left_masks
        left_vents = left_vents
    return game_Masks, game_Vents, g_counter, left_masks, left_vents


#Allocate extra resources from second game
def final_Resources(left_over_m, left_over_v, p1_rec_m, p1_want_m, p1_rec_v, p1_want_v,\
                    p2_rec_m, p2_want_m, p2_rec_v, p2_want_v):
    mask_rand = random.randrange(0, 2)
    vent_rand = random.randrange(0, 2)
    if mask_rand == 0:
        p1_rec_m += math.floor(left_over_m / 2) + (left_over_m % 2)
        p2_rec_m += math.floor(left_over_m / 2)
    else:
        p1_rec_m += math.floor(left_over_m / 2) 
        p2_rec_m += math.floor(left_over_m / 2) + (left_over_m % 2)
        
    if vent_rand == 0:
        p1_rec_v += math.floor(left_over_v / 2) + (left_over_v % 2)
        p2_rec_v += math.floor(left_over_v / 2)
    else:
        p1_rec_v += math.floor(left_over_v / 2) 
        p2_rec_v += math.floor(left_over_v / 2) + (left_over_v % 2)
        
    if p1_rec_m > p1_want_m:
        resources = reduceAmount(p1_rec_m, p1_want_m)
        p1_rec_m -= resources
        p2_rec_m += resources
    if p1_rec_v > p1_want_v:
        resources = reduceAmount(p1_rec_v, p1_want_v)
        p1_rec_v -= resources
        p2_rec_v += resources
    if p2_rec_m > p2_want_m:
        resources = reduceAmount(p2_rec_m, p2_want_m)
        p2_rec_m -= resources
        p1_rec_m += resources
    if p2_rec_v > p2_want_v:
        resources = reduceAmount(p2_rec_v, p2_want_v)
        p2_rec_v -= resources
        p1_rec_v += resources
    return p1_rec_m, p1_rec_v, p2_rec_m, p2_rec_v    
    

#function to run the game: ask for input, create matrix, generate nash 
def run_game():
    #Creating Game Variables
    print("Welcome to the Hospital Resource Allocation simulator!")
    ava_Masks, ava_Vents,\
    p1_masks_want, p1_vents_want,\
    p2_masks_want, p2_vents_want,\
    p3_masks_want, p3_vents_want = game_Elements()
    
    sub_masks = math.floor(ava_Masks * 0.1)
    sub_vents = math.floor(ava_Vents * 0.1)
    p1_masks_rec = 0
    p1_vents_rec = 0
    p2_masks_rec = 0
    p2_vents_rec = 0
    mask_carry_over = ava_Masks % 10
    vent_carry_over = ava_Vents % 10
    
    #Play Subgames
    subgames = 1
    while subgames < 11:
             
        #Create matrix
        game_Matrix = create_Matrix2PG(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                 p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want)
        #print(game_Matrix)
        
        #Find Nash
        game_Nash = findNash(playerA_best(game_Matrix), playerB_best(game_Matrix))
        
        #update variables
        if game_Nash == "0,0":
            mask_carry_over += sub_masks % 2
            p1_masks_rec += math.floor(sub_masks * 0.5)
            p2_masks_rec += math.floor(sub_masks * 0.5)
            vent_carry_over += sub_vents
        elif game_Nash == "0,1":
            p1_masks_rec += sub_masks
            p2_vents_rec += sub_vents
        elif game_Nash == "1,0":
            p1_vents_rec += sub_vents
            p2_masks_rec += sub_masks
        elif game_Nash == "1,1":
            vent_carry_over += sub_vents % 2
            p1_vents_rec += math.floor(sub_vents * 0.5)
            p2_vents_rec += math.floor(sub_vents * 0.5)
            mask_carry_over += sub_masks
            
        #Check that Players dont go over resource need
        if p1_masks_rec > p1_masks_want:
            resources = reduceAmount(p1_masks_rec, p1_masks_want)
            p1_masks_rec -= resources
            mask_carry_over += resources
        if p1_vents_rec > p1_vents_want:
            resources = reduceAmount(p1_vents_rec, p1_vents_want)
            p1_vents_rec -= resources
            vent_carry_over += resources
        if p2_masks_rec > p2_masks_want:
            resources = reduceAmount(p2_masks_rec, p2_masks_want)
            p2_masks_rec -= resources
            mask_carry_over += resources
        if p2_vents_rec > p2_vents_want:
            resources = reduceAmount(p2_vents_rec, p2_vents_want)
            p2_vents_rec -= resources
            vent_carry_over += resources
        
        subgames += 1

        #Display allocation
        print("SUBGAME: ", subgames-1)
        print("Player 1 has received")
        print("masks:" + str(p1_masks_rec) + "/" + str(p1_masks_want))
        print("ventilators:" + str(p1_vents_rec) + "/" + str(p1_vents_want))

        print("Player 2 has received")
        print("masks:" + str(p2_masks_rec) + "/" + str(p2_masks_want))
        print("ventilators:" + str(p2_vents_rec) + "/" + str(p2_vents_want))
        print("\n")
        print("Total masks remaining: " + str(ava_Masks - p1_masks_rec - p2_masks_rec))
        print("Total ventilators remaining: " + str(ava_Vents - p1_vents_rec - p2_vents_rec))
        print("\n")

    #Second set of subgames using left over resoruces 
    final_masks = 0
    final_vents = 0
    while resources_gone(mask_carry_over, vent_carry_over):
        #define variables
        sub_masks, sub_vents, game_counter, mask_carry_over, vent_carry_over = sec_Variables(mask_carry_over, vent_carry_over)
        
        #Play Second Game
        while game_counter != 0:
            #Create matrix
            game_Matrix = create_Matrix2PG(sub_masks, sub_vents, p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want,\
                 p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want)
            
            #Find Nash
            game_Nash = findNash(playerA_best(game_Matrix), playerB_best(game_Matrix))
            
            #update variables
            if game_Nash == "0,0":
                p1_masks_rec += math.floor(sub_masks * 0.5)
                p2_masks_rec += math.floor(sub_masks * 0.5)
                final_masks += (sub_masks % 2)
                final_vents += sub_vents
            elif game_Nash == "0,1":
                p1_masks_rec += sub_masks
                p2_vents_rec += sub_vents
            elif game_Nash == "1,0":
                p1_vents_rec += sub_vents
                p2_masks_rec += sub_masks
            elif game_Nash == "1,1":
                p1_vents_rec += math.floor(sub_vents * 0.5)
                p2_vents_rec += math.floor(sub_vents * 0.5)
                final_masks += sub_masks
                final_vents += (sub_vents % 2)
            
            #Check that Players dont go over resource need
            if p1_masks_rec > p1_masks_want:
                resources = reduceAmount(p1_masks_rec, p1_masks_want)
                p1_masks_rec -= resources
                final_masks += resources
            if p1_vents_rec > p1_vents_want:
                resources = reduceAmount(p1_vents_rec, p1_vents_want)
                p1_vents_rec -= resources
                final_vents += resources
            if p2_masks_rec > p2_masks_want:
                resources = reduceAmount(p2_masks_rec, p2_masks_want)
                p2_masks_rec -= resources
                final_masks += resources
            if p2_vents_rec > p2_vents_want:
                resources = reduceAmount(p2_vents_rec, p2_vents_want)
                p2_vents_rec -= resources
                final_vents += resources
                
            game_counter -= 1
        
        #Check if there is only one resource left
        if mask_carry_over == 1:
            random_pick = random.randrange(0,2)
            if random_pick == 0:
                p1_masks_rec += 1
                mask_carry_over -= 1
            else:
                p2_masks_rec += 1
                mask_carry_over -= 1
        elif vent_carry_over == 1:
            random_pick = random.randrange(0,2)
            if random_pick == 0:
                p1_vents_rec += 1
                vent_carry_over -= 1
            else:
                p2_vents_rec += 1
                vent_carry_over -= 1
    
    #Final allocation of unallocated resoruces 
    p1_masks_rec, p1_vents_rec, p2_masks_rec, p2_vents_rec = final_Resources(final_masks, final_vents,\
        p1_masks_rec, p1_masks_want, p1_vents_rec, p1_vents_want, p2_masks_rec, p2_masks_want, p2_vents_rec, p2_vents_want)
   
    #Display allocation
    print("Player 1 has received")
    print("masks:" + str(p1_masks_rec) + "/" + str(p1_masks_want))
    print("ventilators:" + str(p1_vents_rec) + "/" + str(p1_vents_want))
    print("\n")
    print("Player 2 has received")
    print("masks:" + str(p2_masks_rec) + "/" + str(p2_masks_want))
    print("ventilators:" + str(p2_vents_rec) + "/" + str(p2_vents_want))
    
run_game()


