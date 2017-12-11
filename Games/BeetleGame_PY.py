# Name: Rohit Pawar
# Date: 7/6/2017
# CS 524
# Program Assignment 1
# Description: Its a console program in Python that allows users to play the dice game Beetle. Program uses the object-oriented style of programming.
# Python Version 2.7



from random import *
class Die:
    # Die class will provide a funtion for rolling the dice.

    items = [1, 2, 3, 4, 5, 6, 4, 5, 6, 1, 2, 3]

    def roll(self):
        # this function will generate an random number that falls between 1 to 6
        return sample(self.items,  1)[0]

class Player:
    # This class will store the player information like his name, score, printing beetle.

    name ='';
    score = 0; 

    def __init__(self,name):
        # constructor called to initialize name of the player.
        self.name=name;

    def playTurn(self):
        # This function will perform action of rolling a dice for a player and calculating his score.

        if(self.name != 'Computer'):
            #if player is computer don't ask to roll a dice
            yourTurn = raw_input("\n"+self.name+"'s turn: [Press Enter to roll dice]")
        
        rolledDie = Die().roll()

        print("\n"+self.name+" rolled "+str(rolledDie)+"\n")

        if(rolledDie == 1 and self.score ==0):
            self.score = 1;
        if(rolledDie == 2 and self.score ==1):
            self.score = 3;
        if(rolledDie == 3 and (self.score ==3 or self.score ==6)):
            self.score = self.score + 3;
        if(rolledDie == 4 and (self.score ==9 or self.score ==13)):
            self.score = self.score + 4;
        if(rolledDie == 5 and (self.score == 17 or self.score ==22)):
            self.score = self.score + 5;

    def printBeetle(self):
        # Print a Beetle according to score of the player.

        printing = "\n\n\n"

        if(self.score >= 13):   
             printing = printing +  "\t    \\"
        if(self.score >= 17): 
             printing = printing + " /"
        printing = printing + "\n"
        if(self.score >= 3): 
             printing = printing + "\t   #####\n\t  #"
        if(self.score >= 22): 
             printing = printing + "o"
        else:
            printing = printing + " "
        if(self.score == 27): 
             printing = printing + "   o"
        else:
            printing = printing + "    "
        if(self.score >= 3):
            printing = printing + "#"
        printing = printing + "\n"
        if(self.score >= 1): 
             printing = printing + "\t  #######"
        printing = printing + "\n"

        count=0;

        while(count < 3):
            if(self.score >= 6): 
                 printing = printing + "      /^\\"
            else:
                printing = printing +"\t "
            if(self.score >= 1): 
                 printing = printing + "#   |   #"
            if(self.score >= 9): 
                 printing = printing + "/^\\"
            printing = printing + "\n"
            count += 1;

        if(self.score >= 1): 
             printing = printing + "\t  #######"

        printing = printing + "\n"

        print(printing)

    def wins(self):
        # Check if a player is winning.

        if(self.score == 27):
            # Player has won display a congratulations message.
            print("\n\n#############################  !!Congratulations!!  #####################################\n#\t\t\t\t\t\t\t\t\t\t\t#\n#\t\t\t\t"+self.name+" Wins\t\t\t\t\t\t#\n#\t\t\t\t\t\t\t\t\t\t\t#\n#########################################################################################\n\n")
            
            return True
        else:
            return False



class Beetle:
    #Beetle game class provies functionality to start playing.

    playingOption = 1;

    def start(self):
        #Start playing the game. Choose between an  option of Multiplayer and Bot accordingly create an instance and start taking turns to roll the dice.
        
        self.playingOption = raw_input("\t[PRESS 0 FOR GAME MANUAL]\n\tChoose Player\n\t1. Multiplayer [Press \"1\"] \n\t2. Player Vs Bot [Press \"2\"]\n\t: ");
        try:
            #try to parse user input into int else through exception of type ValueError.
            if (int(self.playingOption) != 1 and int(self.playingOption) != 2 and int(self.playingOption) != 0):
                raise ValueError()

            player1 = ''
            player2 = ''

            if(int(self.playingOption) == 0):
                # Show user with Game Manual which will help him to understand the game.
                print("\n\t################## Player Guide ########################\n")
                print("\t ~ Start with rolling a dice on your turn.\n\t ~ If a 1 is rolled, the player earns the body of the beetle.\n\t ~ If a 2 is rolled, the head is added.\n\t ~ If a 3 is rolled, the left 3 legs are added.\n\t ~ The second 3 allows the right 3 legs to be added.\n\t ~ If a 4 is rolled, one antenna is added to the beetle's head.\n\t ~ Another 4 is required to add the second antenna to the beetle's head.\n\t ~ If a 5 is rolled, one eye is added. \n\t ~ A second 5 results in the second eye being added.\n\t ~ Now, your beetle is complete! The player to complete their beetle first wins!\n")
                print("\t##########################################################\n")
                return

            if(int(self.playingOption) == 1):
                #'Player Vs Player' Create player instance and start playing Multiplayer mode.
                print('\nPlayer Vs Player\n')
                player1 = Player('Player 1')
                player2 = Player('Player 2')
            else:
                #Player Vs Computer Create player and bot instance and start playing in Bot mode.
                print('\nPlayer Vs Computer\n')
                player1 = Player('Player 1')
                player2 = Player('Computer')
                
            while(not player1.wins() and not player2.wins()):
                #Continue to play until one of the player wins.
                player1.playTurn()
                player2.playTurn()
                #Print each players Beetle
                print("\n "+player1.name+" Beetle")
                player1.printBeetle()
                print("\n "+player2.name+" Beetle")
                player2.printBeetle()

        except ValueError:
            print("\nPlease choose between option 0, 1 and 2 only.\n\n")
    
    def welcome(self):
        #Welcome user with brief details about the game.
        print("\t*****************************************************************\n\t*\t\t\t\t\t\t\t\t*\n\t*  Welcome to the exiciting game of Beetle.\t\t\t*\n\t*  You can play against other player or against computer.\t*\n\t*  Thank you and Happy Gaming!\t\t\t\t\t*\n\t*\t\t\t\t\t\t\t\t*\n\t*****************************************************************")

game = Beetle();
#Create an instance of Beetle game to start playing.
game.welcome();
while(True):
    #While true to keep game continious running.
    game.start();



