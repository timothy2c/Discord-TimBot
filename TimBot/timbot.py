import discord # import discord.py
import random
import mysql.connector
import asyncio
import math
import time
from config import api_key
from  lists import *
from discord.ext import commands # import commands
from databasefunctions import *
from botfunctions import *



bot = commands.Bot(command_prefix = 'tb')
bot.current_users = set() # current users in a command (wordle)

# get all of the emojis
for item in custom_emojis_ids:
    bot.get_emoji(item)

#---BOOT UP BOT---
@bot.event
async def on_ready():
    print("timbot is ready.")
    
#---EVENT ROLL ACTIVE?---
event_roll = False

#---ROLL COMMAND---
@bot.command(aliases=['r'], help='Roll for a timbit. Cooldown of 2 hours.')
@commands.cooldown(1,7200, commands.BucketType.user)
async def roll(ctx): # roll for a timbit
        response = rollfxn(ctx)
        msg_author = (ctx.message.author)
        await ctx.send(msg_author.mention + response) # makes the bot say what you rolled
    
#--- ROLL ERROR AND EVENT ROLL---
@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if event_roll == True: # if there's an event roll happening
            await ctx.send(ctx.message.author.mention + " " + event_rollfxn(ctx))
        
        else:
            seconds_left = roll.get_cooldown_retry_after(ctx)
            hours_left = math.floor(seconds_left / 3600)
            minutes_left = (seconds_left - (hours_left * 3600)) / 60
            minutes_left = math.floor(minutes_left)
            msg = "Oh no! That command is on cooldown! Please try again in " + str(hours_left) + "H " + str(minutes_left) + "M"
            await ctx.send(msg)
    else:
        raise error


#---WORDLE COMMAND---
@bot.command(aliases=['w'], help='Guess the word within 6 tries to gain crumbs.')
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def wordle(ctx):
    author = ctx.author # get the message author so other people can't play the same wordle
    channel = ctx.channel # get the message channel
    guess = '' # initialize guess    
    blank_letter = '⬜'
    lines = [""]*6 # 6 guesses
    correct_guess = False # initialize guesses
    guess_counter = 0 # initialize guesses
    msg_author = (ctx.message.author)
    user_id = msg_author.id    

    correct_word = random.choice(five_letter_words)
    correct_word = correct_word.lower() # generates a word to guess    
    
    print(correct_word)
    
    rows, cols = (6,5) # size of the board
    wordle = [[blank_letter for i in range(cols)] for j in range(rows)] # makes a 2D array storing the board
    
    # puts the board in string format so the embed can read it
    for i in range(6):
        for j in range(5):
            lines[i] += wordle[i][j] + " "
    
    embed=discord.Embed(title=ctx.message.author.name+"'s wordle", description = ("Correct letters will look like: " + correct_letters.get('a') + 
                                                                                          "\nIncorrect letters will look like: " + wrong_letters.get('a') + 
                                                                                          "\nCorrect letters in the wrong spot will look like: " + 
                                                                                          misplaced_letters.get('a'))) # the board in an embed format
    embed.add_field(name="\u200b",value=(lines[0]+"\n"+lines[1]+"\n"+lines[2]+"\n"+lines[3]+"\n"+lines[4]+"\n"+lines[5]), inline=False)
    embed.set_footer(text="Enter 'quit' to quit.")
    await ctx.send(embed=embed)
    
    # making the game function
    while correct_guess == False and guess_counter < 6 and guess != 'quit':
        
        # check if the message is the right channel and author
        def check(m):
            return m.channel == channel and m.author == author
        try:
            guess = await bot.wait_for('message', check=check)
        except: # if the user takes too long
            await ctx.send("You ran out of time to guess!")
            wordleStreak(user_id, False)
        
        guess = guess.content
        guess = guess.lower() 
        if guess == 'quit':
            wordleStreak(user_id, False)
            break 
        
        lines[guess_counter] = '' # reset the current line
        while guess not in dictionary and guess !='quit':
            await ctx.send("Enter a valid 5 letter word. Enter 'quit' to quit.")
            guess = await bot.wait_for('message', check=check)
            guess = guess.content
            guess = guess.lower()    
            lines[guess_counter] = '' # reset the current line              

        if guess == 'quit':
            lines[guess_counter] = '⬜ ⬜ ⬜ ⬜ ⬜'
            break
        # comparing the words
        if guess == correct_word: # if the guess is correct
            correct_guess = True
            for letter in guess:
                lines[guess_counter] += correct_letters.get(letter) + " "
        else: # otherwise
            for i in range(len(guess)):
                if guess[i] not in correct_word:
                    lines[guess_counter] += wrong_letters.get(guess[i]) + " "
                elif guess[i] in correct_word and guess[i] == correct_word[i]: # if the letter is in the right spot
                    lines[guess_counter] += correct_letters.get(guess[i]) + " "
                else: # if the letter is in the wrong spot
                    lines[guess_counter] += misplaced_letters.get(guess[i]) + " "
        
                              
        embed=discord.Embed(title=ctx.message.author.name+"'s wordle", description = ("Correct letters will look like: " + correct_letters.get('a') + 
                                                                                                          "\nIncorrect letters will look like: " + wrong_letters.get('a') + 
                                                                                                          "\nCorrect letters in the wrong spot will look like: " + 
                                                                                                          misplaced_letters.get('a'))) # the board in an embed format
        
        embed.add_field(name="\u200b",value=(lines[0]+"\n"+lines[1]+"\n"+lines[2]+"\n"+lines[3]+"\n"+lines[4]+"\n"+lines[5]), inline=False)
        embed.set_footer(text="Enter 'quit' to quit.")
        await ctx.send(embed=embed)
        
        guess_counter +=1 # add 1 to guesses
        guess = "" # reset the guess
        
    # end of while loop/end of wordle

    if (correct_guess == False and guess_counter == 6): # if the user lost
        wordleStreak(user_id, False)
        await ctx.send(msg_author.mention +" You failed to guess the right word in time! :(")
    
    elif(correct_guess == True): # if the user won
        wordleStreak(user_id, True)
        streak = getValue('wordle_streak', 'streak', user_id)
        if streak / 10 >= 1: # if streak is more than 10
            bonus = ((streak // 10)**2 ) * 5000
            generateCrumbs(user_id, 500 + bonus)
            await ctx.send(msg_author.mention +" You guessed the correct word!")
            await ctx.send("500 crumbs were added to your balance! STREAK BONUS! You gained an additional " + str(bonus) + " crumbs!")
        else: # if streak is less than 10
            await ctx.send(msg_author.mention +" You guessed the correct word!")
            await ctx.send("500 crumbs were added to your balance!")
    
    streak = getValue('wordle_streak', 'streak', user_id)
    embed=discord.Embed(title=ctx.message.author.name+"'s wordle", description = "The correct word was: " + correct_word.upper())
    embed.add_field(name="\u200b",value=(lines[0]+"\n"+lines[1]+"\n"+lines[2]+"\n"+lines[3]+"\n"+lines[4]+"\n"+lines[5]), inline=False)
    embed.set_footer(text="Game ended. Current streak: " + str(streak))
    await ctx.send(embed=embed)           
@wordle.error
async def wordle_error(ctx,error):
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send("Please finish your current game first!")

#---BALANCE/CRUMBS COMMAND---
@bot.command(aliases=['c','bal','balance'],help='Displays the amount of crumbs you have.')
async def crumbs(ctx):
    balance = crumbsfxn(ctx.message.author.id)
    
    await ctx.send("You currently have " + "__**"+str(balance)+"**__" + " crumbs!")



#---BITS/INV COMMAND---
@bot.command(aliases=['b'], help='Displays your current bits.')
async def bits(ctx):
    user_id = ctx.message.author.id
    titlemsg = ctx.message.author.name + "'s Bits\n"
    bitsmsg = bitsfxn(user_id)
    await ctx.send(titlemsg + bitsmsg + "\nValue: " +str(dailyValue(user_id) -1000))

#---DAILY COMMAND---
@bot.command(aliases=['d'], help='Collect your daily crumbs!')
@commands.cooldown(1,86400, commands.BucketType.user)
async def daily(ctx):
    user_id = ctx.message.author.id
    msg_author = ctx.message.author
    daily_value = dailyValue(user_id)
    newCrumbs = getValue("user_crumbs","crumbs",user_id) + daily_value
    insertIntoTable("user_crumbs","crumbs",user_id,newCrumbs)
    await ctx.send("Yay! "+ msg_author.mention +" you gained " + str(daily_value) + " daily crumbs! :D")
   
@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds_left = daily.get_cooldown_retry_after(ctx)
        hours_left = math.floor(seconds_left / 3600)
        minutes_left = (seconds_left - (hours_left * 3600)) / 60
        minutes_left = math.floor(minutes_left)
        msg = "Oh no! That command is on cooldown! Please try again in " + str(hours_left) + "H " + str(minutes_left) + "M"
        await ctx.send(msg)
        return
    else:
        raise error

#---GIVE COMMAND---
@bot.command(name='give', help='Donate crumbs to your friends!')
async def give(ctx, recipient:discord.User, amount:int):
    donator_id = ctx.message.author.id
    recipient_id = recipient.id
    donator_crumbs = getValue("user_crumbs","crumbs",donator_id)
    recipient_crumbs = getValue("user_crumbs","crumbs",recipient_id)
    
    if recipient_id != donator_id:
        if amount > donator_crumbs: # if the user doesn't have enough crumbs
            await ctx.send("You don't have enough crumbs to do that!")
        else: # if the user has enough crumbs
            subtractCrumbs(donator_id, amount)
            generateCrumbs(recipient_id, amount)
            await ctx.send(ctx.message.author.mention + " you gave " + str(amount) + " crumbs to " + recipient.mention + "!")
    else:
        await ctx.send("You can't give crumbs to yourself, silly!")
@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.UserNotFound):
        await ctx.send("Please enter a valid user!")
        return

    
#---COINFLIP COMMAND---
@bot.command(aliases=['cf'], help='GAMBLING ADDICTION GAMBLING ADDICTION GAMBLING ADDICTION GAMBLING ADDICTION')
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def coinflip(ctx, amount:int):
    user_id = ctx.message.author.id
    user_crumbs = getValue("user_crumbs","crumbs",user_id)
    if amount > 50000:
        amount = 50000
    sides = [1,0]
    if amount > user_crumbs:
        await ctx.send("You don't have enough crumbs to do that!")
    else:
        await ctx.send("Rolling " + str(amount) + " crumbs. The coin flips...")
        await asyncio.sleep(2)
        if random.choice(sides) == 1: # if the user won
            generateCrumbs(user_id, amount) # add double the bet to user
            await ctx.send("You won! You gained " + str(amount) + " crumbs!")
        else:
            subtractCrumbs(user_id, amount)
            await ctx.send("You lost! rip moneyz, you'll get it back.. copium")
 
 
@coinflip.error
async def coinflip_error(ctx, error):
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send("Please finish your current game first!")   
        return

@bot.command()
async def streak(ctx):
    streak = getValue('wordle_streak','streak', ctx.message.author.id)
    print(streak)
    await ctx.send(str(streak))
    
#---VOCABULOUS COMMAND---
@bot.command(aliases=['v'], help='Enter words containing the corresponding letters before time runs out to earn points and crumbs.')
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def vocabulous(ctx):
    author = ctx.author
    channel = ctx.channel
    word_entered = '' #initializes word entered
    msg_author = (ctx.message.author)
    user_id = msg_author.id
    combination = random.choice(combinations)
    
    embed=discord.Embed(title=ctx.message.author.name+"'s Vocabulous", description = ("Enter a word containing" + correct_letters.get[combination[0]] + correct_letters.get[combination[1]]))
    embed.add_field(name="\u200b", value=("Word Entered:\n"))
    
          
            
    
             

    


bot.run(api_key)


