import discord
import random
import asyncio
import fileinput
import time
import csv
import emoji
from lists import *
from discord.ext import commands
from config import TOKEN



#---BOOT UP BOT---

intents = discord.Intents.all()
bot = discord.Bot(intents = intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    
            



#---COMMANDS---

# WORDLE COMMAND
@bot.slash_command(name="wordle", guild_ids=[775241553710415902, 758138986546987019], description="Play a game of wordle.")
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def wordle(ctx):
    await ctx.respond("Game Started")
    player = ctx.user
    channel = ctx.channel
    guess = '' # initialize guess    
    blank_letter = '⬜'
    lines = [""]*6 # 6 guesses
    correct_guess = False # initialize guesses
    guess_counter = 0 # initialize guesses

    correct_word = random.choice(five_letter_words)
    correct_word = correct_word.lower() # generates a word to guess
    print(correct_word)  

    rows, cols = (6,5) # size of the board
    wordle = [[blank_letter for i in range(cols)] for j in range(rows)] # makes a 2D array storing the board

    # puts the board in string format so the embed can read it
    for i in range(6):
        for j in range(5):
            lines[i] += wordle[i][j] + " "
    
    embed=discord.Embed(title=player.name+"'s wordle", description = ("Correct letters will look like: " + correct_letters.get('a') + 
                                                                                          "\nIncorrect letters will look like: " + wrong_letters.get('a') + 
                                                                                          "\nCorrect letters in the wrong spot will look like: " + 
                                                                                          misplaced_letters.get('a'))) # the board in an embed format
    embed.add_field(name="\u200b",value=(lines[0]+"\n"+lines[1]+"\n"+lines[2]+"\n"+lines[3]+"\n"+lines[4]+"\n"+lines[5]), inline=False)
    embed.set_footer(text="Enter 'quit' to quit.")
    await ctx.send(embed=embed)

    #--- PLAY THE GAME
    while correct_guess == False and guess_counter < 6 and guess != 'quit':
        
        # check if the message is the right channel and author
        def check(ctx):
            return ctx.channel == channel and ctx.author == player
        try:
            guess = await bot.wait_for('message', check=check)
        except: # if the user takes too long
            await ctx.respond("You ran out of time to guess!")
            
        
        guess = guess.content
        guess = guess.lower() 
        
        if guess == 'quit':
            await ctx.respond("Game quit.")
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
        
                              
        embed=discord.Embed(title=player.name+"'s wordle", description = ("Correct letters will look like: " + correct_letters.get('a') + 
                                                                                                          "\nIncorrect letters will look like: " + wrong_letters.get('a') + 
                                                                                                          "\nCorrect letters in the wrong spot will look like: " + 
                                                                                                          misplaced_letters.get('a'))) # the board in an embed format
        
        embed.add_field(name="\u200b",value=(lines[0]+"\n"+lines[1]+"\n"+lines[2]+"\n"+lines[3]+"\n"+lines[4]+"\n"+lines[5]), inline=False)
        embed.set_footer(text="Enter 'quit' to quit.")
        await ctx.send(embed=embed)
        guess_counter +=1 # add 1 to guesses
        guess = "" # reset the guess

        if (correct_guess == False and guess_counter == 6): # if the user lost
            await ctx.respond(player.mention +" You failed to guess the right word in time! :(")
        elif(correct_guess == True):
            await ctx.respond(player.mention +" You guessed the correct word!")


@wordle.error
async def wordle_error(ctx,error):
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send("Please finish your current game first!")




def valid_word(word):
    word_dict = {'a': "aWords.txt", 'b' : "bWords.txt", 'c' : "cWords.txt", 'd' : "dWords.txt", 'e' : "eWords.txt", 'f' : "fWords.txt",
            'g' : "gWords.txt", 'h' : "hWords.txt", 'i' : "iWords.txt", 'j' : "jWords.txt", 'k' : "kWords.txt", 'l' : "lWords.txt",
            'm' : "mWords.txt", 'n' : "nWords.txt", 'o' : "oWords.txt", 'p' : "pWords.txt", 'q' : "qWords.txt", 'r' : "rWords.txt",
            's' : "sWords.txt", 't' : "tWords.txt", 'u' : "uWords.txt", 'v' : "vWords.txt", 'w' : "wWords.txt", 'x' : "xWords.txt",
            'y' : "yWords.txt", 'z' : "zWords.txt"}
    

    if len(word) <= 0:
        return False
    
    first_letter = word[0]
    file_name = word_dict[first_letter]
    temp = []
    
    for lines in fileinput.input(file_name):
        temp.append(lines.strip().lower())
    return word in temp

def get_letter_prompt():
    temp = []
    for lines in fileinput.input("letterCombinations.txt"):
        temp.append(lines.strip().lower())
    return random.choice(temp)

# VOCABULOUS COMMAND
@bot.slash_command(name="vocabulous", guild_ids=[775241553710415902, 758138986546987019], description="Play a game of vocabulous.")
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def vocabulous(ctx):
    await ctx.respond("Game started.")
    player = ctx.user
    channel = ctx.channel
    letter_prompt = get_letter_prompt()
    word_entered = ""
    message = ''
    score = 0
    used_words = []
    total_words = 0
    lost = False     

    time_limit = 7.0
    start_time = time.time() 
    
                               
    
    while(lost == False):
        embed = discord.Embed(title=player.name+"'s vocabulous", description="Score: "+ str(score))
        embed.add_field(name="\u200b",value="Enter a word containing: "+ correct_letters.get(letter_prompt[0])+ " " + correct_letters.get(letter_prompt[1]), inline=False)
        embed.add_field(name="Word entered: ", value=str(word_entered), inline=False)
        embed.set_footer(text="Words entered: " + str(total_words))
        await ctx.send(embed=embed)

        #timer
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            await ctx.respond(player.mention + " You ran out of time! Your final score was: " + str(score))
            return

        def check(ctx):
            return ctx.channel == channel and ctx.author == player
        try:
            message = await bot.wait_for('message', check=check, timeout=time_limit)
            
        except: # if the user takes too long
            await ctx.send(player.mention + " You ran out of time! Your final score was: " + str(score))
            return
        word_entered = message.content
        word_entered= word_entered.lower().strip()
        


        if ((word_entered not in used_words) and (letter_prompt in word_entered)): # word is not used and contains the right letters
            
            if valid_word(word_entered): # if the word passes, increase score
                await message.add_reaction('✅')
                elapsed_time = 0
                start_time = time.time()
                letter_prompt = get_letter_prompt()
                used_words.append(word_entered)
                score += len(word_entered)
                total_words += 1
            else: # tell the user that their word is invalid
                await message.add_reaction('❌')
                await ctx.send("Invalid word!")
        else:
            if word_entered in used_words: # if the word is used already
                await message.add_reaction('❌')
                await ctx.send("You used that word already!")
            else: # if the word doesnt exist and does not contain the right letters
                await message.add_reaction('❌')
                await ctx.send("Invalid word!")
        
@vocabulous.error     
async def vocabulous_error(ctx,error):
    if isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send("Please finish your current game first!")



    

@bot.slash_command(name="vocabulous_duel", guild_ids=[775241553710415902, 758138986546987019], description="challenge a friend to a vocabulous duel! Takes place in DM's")
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
async def vocabulous_duel(ctx, player_two: discord.User):
    player_one = ctx.user
    channel = ctx.channel
    message = ''
    letter_prompt = get_letter_prompt()
    round_no = 1

    player_one_health = 50
    player_two_health = 50
    player_one_message = ''
    player_two_message = ''
    player_one_used_words = []
    player_two_used_words = []
    player_one_word_length = 0
    player_two_word_length = 0
    round_winner = ''
    round_loser = ''
    damage = 0

    time_limit = 7.0
    start_time = time.time()

    # make sure the user is not dueling themself or the bot
    if player_two == player_one:
        await ctx.respond("You cannot duel yourself!", ephemeral= True)
        return
    if player_two == bot.user:
        await ctx.respond("You cannot duel me!", ephemeral= True)
        return


    # notify the targeted user of the duel
    def check(ctx):
        return ctx.channel == channel and ctx.author == player_two
    await ctx.respond(player_two.mention + ", " + player_one.mention + " has challenged you to a duel! (Y/N)")

    # get response
    try:
        message = await bot.wait_for('message', check=check, timeout=10.0)
            
    except: # if the user takes too long to respond
        await ctx.send("Duel timed out.")
        return
    
    if message.content == 'y' or message.content =='Y':
        await ctx.send("Game started")
    
    if message.content == 'n' or message.content == 'N':
        await ctx.send("Duel declined.")
        return
    
    # start the game
    while player_one_health > 0 and player_two_health > 0:
        embed = discord.Embed(title="Round " + str(round_no), description="Enter a word containing: "+ correct_letters.get(letter_prompt[0])+ " " + correct_letters.get(letter_prompt[1]))
        embed.add_field(name=player_one.name, value=player_one.name+ "'s health: " + str(player_one_health), inline=True)
        embed.add_field(name=player_two.name, value=player_two.name+ "'s health: " + str(player_two_health), inline=True)
        embed.add_field(name=player_one.name + 's word: ', value= player_one_message, inline= False)
        embed.add_field(name=player_two.name + 's word: ', value= player_two_message, inline= False)

        # send to player 1 first
        await player_one.send(embed=embed)
        
        try:
            player_one_message = await bot.wait_for('message', check=lambda message: message.author == player_one and isinstance(message.channel, discord.DMChannel), timeout=60)
            player_one_message = player_one_message.content.lower().strip()
        except:
            await player_one.send("You ran out of time to enter a word!")
            print("player one timed out")
            player_one_message = ''
            



        # send to player 2 next
        await player_two.send(embed=embed)
        try:
            player_two_message = await bot.wait_for('message', check=lambda message: message.author == player_two and isinstance(message.channel, discord.DMChannel))
            player_two_message = player_two_message.content.lower().strip()
        except:
            await player_two.send("You ran out of time to enter a word!")
            print("player two timed out")
            player_two_message = ''
        
        # compare the words
        if valid_word(player_one_message) and letter_prompt in player_one_message and player_one_message not in player_one_used_words:
            player_one_word_length = len(player_one_message)
        else:
            player_one_word_length = 0

        if valid_word(player_two_message) and letter_prompt in player_two_message and player_two_message not in player_two_used_words:
            player_two_word_length = len(player_two_message)
        else:
            player_two_word_length = 0

        if player_one_word_length >= player_two_word_length: # if player 1 wins the round
            damage = player_one_word_length - player_two_word_length
            player_two_health -= damage
            round_winner = player_one.name
            round_loser = player_two.name

        if player_two_word_length > player_one_word_length: # if player 2 wins the  round
            damage = player_two_word_length - player_one_word_length
            player_one_health -= damage
            round_winner = player_two.name
            round_loser = player_one.name

        # Update the embed
        embed = discord.Embed(title="Round " + str(round_no), description="Enter a word containing: "+ correct_letters.get(letter_prompt[0])+ " " + correct_letters.get(letter_prompt[1]))
        embed.add_field(name=player_one.name, value=player_one.name+ "'s health: " + str(player_one_health), inline=True)
        embed.add_field(name=player_two.name, value=player_two.name+ "'s health: " + str(player_two_health), inline=True)
        embed.add_field(name=player_one.name + 's word: ', value= player_one_message, inline= False)
        embed.add_field(name=player_two.name + 's word: ', value= player_two_message, inline= False)
        
        await player_one.send(embed=embed)
        await player_one.send(round_winner + " won the round! " + round_loser + " took " + str(damage) + " damage!" )
        await player_two.send(embed=embed)
        await player_two.send(round_winner + " won the round! " + round_loser + " took " + str(damage) + " damage!" )
        await ctx.send(embed=embed)
        await ctx.send(round_winner + " won the round! " + round_loser + " took " + str(damage) + " damage!" )
        letter_prompt = get_letter_prompt()
        player_one_word_length = 0
        player_two_word_length = 0
        round_no += 1
    
        if player_one_health <= 0 or player_two_health <= 0:
            if player_one_health > 0:
                embed = discord.Embed(title=player_one.name + " vs " + player_two.name, description="Enter a word containing: "+ correct_letters.get(letter_prompt[0])+ " " + correct_letters.get(letter_prompt[1]))
                embed.add_field(name=player_one.name, value=player_one.name+ "'s health: " + str(player_one_health), inline=True)
                embed.add_field(name=player_two.name, value=player_two.name+ "'s health: " + str(player_two_health), inline=True)
                embed.add_field(name=player_one.name + 's word: ', value= player_one_message, inline= False)
                embed.add_field(name=player_two.name + 's word: ', value= player_two_message, inline= False)
                await ctx.send(embed=embed)
                await player_one.send(embed=embed)
                await player_one.send("You won!")
                
                await player_two.send(embed=embed)
                await player_two.send("You lost!")
                await ctx.respond("Game over! " + player_one.mention + " wins!")
            else:
                embed = discord.Embed(title=player_one.name + " vs " + player_two.name, description="Enter a word containing: "+ correct_letters.get(letter_prompt[0])+ " " + correct_letters.get(letter_prompt[1]))
                embed.add_field(name=player_one.name, value=player_one.name+ "'s health: " + str(player_one_health), inline=True)
                embed.add_field(name=player_two.name, value=player_two.name+ "'s health: " + str(player_two_health), inline=True)
                embed.add_field(name=player_one.name + 's word: ', value= player_one_message, inline= False)
                embed.add_field(name=player_two.name + 's word: ', value= player_two_message, inline= False)
                await ctx.send(embed=embed)
                await player_one.send(embed=embed)
                await player_one.send("You lost!")
                await player_two.send(embed=embed)
                await player_two.send("You won!")
                await ctx.respond("Game over! " + player_two.mention + " wins!")
        
        
       
@bot.slash_command(name="jeopardy_add", guild_ids=[758138986546987019], description="Add a question and answer to the jeopardy pool (Duds Exclusive)")
@commands.max_concurrency(1, per=commands.BucketType.user, wait=False)     
async def jeopardy_add(ctx, question: str, answer: str):
    row = [str(question), emoji.demojize(str(answer)), emoji.demojize(str(ctx.user))]
    filename = "jeopardy.csv"
    with open(filename, "a",encoding ='UTF8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)
    await ctx.respond(emoji.emojize("Successfully added question to the jeopardy! :thumbsup:"))

@bot.slash_command(name="start_jeopardy",guild_ids=[758138986546987019], description="Start Jeopardy with stored questions")
@commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)  
async def start_jeopardy(ctx):
    await ctx.respond("Jeopardy Started.")
    file = open("jeopardy.csv", "r")
    questions = list(csv.reader(file, delimiter=","))
    file.close()
    random.shuffle(questions) # randomize the list of questions

    print(questions)

    for i in range(len(questions)):
        embed = discord.Embed(title="Jeopardy Question "+ str(i + 1),colour=discord.Colour.blue(),description="React to the embed to go to the next part.")
        embed.add_field(name="Question",value=questions[i][0])
        embed.set_footer(text="Author: " + str(questions[i][2]))
        msg = await ctx.send(embed=embed)

        await bot.wait_for('reaction_add')
        await msg.delete()
        embed = discord.Embed(title="Jeopardy Question "+ str(i+1),colour=discord.Colour.blue(),description="React to the embed to go to the next part.")
        embed.add_field(name="Question",value=emoji.demojize(questions[i][0]))
        embed.insert_field_at(1, name="Answer", value=emoji.demojize(questions[i][1]))
        embed.set_footer(text="Author: " + str(questions[i][2]))
        msg = await ctx.send(embed=embed)
        await bot.wait_for('reaction_add')
        await msg.delete()

        if (i == len(questions)-1):
            embed = discord.Embed(title="Game Over!")
            await ctx.send(embed=embed)








    


bot.run(TOKEN)