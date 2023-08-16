import discord
import random
from databasefunctions import *
from lists import *

#---ROLL FUNCTION---
def rollfxn(ctx) -> str:
    msg_author = ctx.message.author
    user_id = msg_author.id
    # getting the rarity
    rarity = random.choices(rarities, weights=(450,350,150,50,3,0), k=1)
    rarity = rarity[0].strip().lower()
    
    # picking a bit from the rarity
    temp = bits[rarity]
    bit = random.choice(temp)
    
    # get the current amount of that bit that the user has
    bitCount = getValue("user_bits", str(bit), user_id) + 1 # increase the amount of the bit by 1
    bitLevel = getValue("bit_levels", str(bit), user_id) # set the level to 0
    
    # add the bit to the db
    insertIntoTable("user_bits", str(bit), user_id, bitCount)
    
    bit_no_space = bit.replace("_", " ")
    if rarity != 'legendary':
        response = (" You rolled: A(n) " + rarity + " " + bit_no_space+ "! "+bit_emojis.get(bit))
    else:
        response = ("OMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMGOMG YOU HIT THE LEGO!!!! YOU ROLLED A(N): " + rarity + " " + bit_no_space+ "! "+ bit_emojis.get(bit))
    return response

#---EVENT ROLL FUNCTION---
def event_rollfxn(ctx)->str:
    roll_cost = 50000
    user_id = ctx.message.author.id
    user_crumbs = getValue("user_crumbs","crumbs",user_id)
    
    if roll_cost > user_crumbs: # if the user cannot afford event roll
        return("EVENT ROLL:" + ctx.message.author.mention + " you can't afford that! Event roll price: " + str(roll_cost) + " crumbs")
    else: # if the user can afford event roll
        subtractCrumbs(user_id, roll_cost)
        message = "EVENT ROLL: you spent " + str(roll_cost) + " crumbs, and " + rollfxn(ctx)
        return (message)
        
    

#--- CRUMBS FUNCTION---
def crumbsfxn(user_id:int) -> int:
    balance = getValue('user_crumbs', 'crumbs', user_id)
    return balance


#--- SUPERSCRIPT FUNCTION---
def numToSuper(num:int) -> str:
    numstr = str(num) # convert from int to string
    supernum = "" # set an empty string to add digits to
    
    # ---- FORMATTING -------
    if len(numstr) == 1:
        supernum += superscript.get('0') + superscript.get('0')
    elif len(numstr) == 2:
        supernum += superscript.get('0')
    
    for digit in numstr: # for each digit, add the superscript equivalent
        supernum += superscript.get(digit)
    return supernum
# ---SUBSCRIPT FUNCTION---
def numToSub(num:int) -> str: # used to convert bit levels to subscript
    numstr= str(num)
    subnum = ""
    if len(numstr) == 1:
        subnum += subscript.get('0')
    for digit in numstr:
        subnum += subscript.get(digit)
    return subnum

# ---BITS FUNCTION---
def bitsfxn(user_id :int) -> str:
    common_message = "**C** " # start an empty string to store bits per rarity
    uncommon_message = "**U** "
    rare_message = "**R** "
    epic_message = "**E** "
    legendary_message = "**L** "  
    event_message = "**?** "
    
    for bit_name in all_bits:
        bit_count = getValue("user_bits", bit_name, user_id)
        bit_level = getValue("bit_levels", bit_name, user_id)
        if bit_count != 0: # if user has at least one of that bit
            bit_rarity = ""
            for rarity in rarities: # find the bit's rarity
                if bit_name in bits.get(rarity):
                    bit_rarity = rarity
                    break
            if bit_rarity == 'common':
                common_message += numToSub(bit_level) + bit_emojis.get(bit_name) + numToSuper(bit_count)
                
            elif bit_rarity == 'uncommon':
                uncommon_message += numToSub(bit_level) + bit_emojis.get(bit_name) + numToSuper(bit_count)
                
            elif bit_rarity == 'rare':
                rare_message += numToSub(bit_level) + bit_emojis.get(bit_name) + numToSuper(bit_count)
                
            elif bit_rarity == 'epic':
                epic_message += numToSub(bit_level) + bit_emojis.get(bit_name) + numToSuper(bit_count)
                
            elif bit_rarity == 'legendary':
                legendary_message += numToSub(bit_level) +  bit_emojis.get(bit_name) + numToSuper(bit_count)
            elif bit_rarity == 'event':
                event_message += numToSub(bit_level) +  bit_emojis.get(bit_name) + numToSuper(bit_count)
                
    print(common_message+"\n"+uncommon_message+"\n"+rare_message+"\n"+epic_message+"\n"+legendary_message+"\n"+event_message)
    
    return common_message+"\n"+uncommon_message+"\n"+rare_message+"\n"+epic_message+"\n"+legendary_message+"\n"+event_message
            
#--- DAILY CALCULATOR FUNCTION---
def dailyValue(user_id: int)-> int:
    
    value = 1000
    for bit_name in all_bits:
        bit_count = getValue("user_bits", bit_name, user_id)
        
        if bit_count != 0:
            
            for rarity in rarities: # find the bit's rarity
                if bit_name in bits.get(rarity):
                    bit_rarity = rarity
                    break
            if bit_rarity == 'common':
                value += 1000 * bit_count
                
            elif bit_rarity == 'uncommon':
                value += 10000 * bit_count
                
            elif bit_rarity == 'rare':
                value += 50000 * bit_count
                
            elif bit_rarity == 'epic':
                value += 200000 * bit_count
                
            elif bit_rarity == 'legendary':
                value += 1000000 * bit_count
            elif bit_rarity == 'event':
                value+= 500000 * bit_count
    return value
    
    
#--- GIVE FUNCTION---
def givefxn(user_id:int)-> bool:
    crumbs_transferred = False # initialize if the crumbs were transferred
    
def initializeBits():
    newbits =[]
    print(newbits)
    for item in newbits:
        addColumn('user_bits', item, 'int')
        addColumn('bit_levels', item, 'int')




    


