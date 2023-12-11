from random import shuffle, randrange

FILENAME = "territories.txt"

class TooMany(Exception):
  def message():
    print("There are not enough territories for that")

class Teritory:
  def __init__(self, name, population, gdp, area):
    self.neighbours = {""}
    self.name = name
    self.area=area
    self.population=population
    self.gdp=gdp
    self.armies=population

  def addNeighbours (self, neigh):
    neigh = set(neigh)
    self.neighbours = self.neighbours.union(neigh)

  def armyNumber(self):
    maxNumber = self.armies - 1
    armyNo = pickNumber(maxNumber)
    self.armies -= int(armyNo)
    return int(armyNo)

  def conquered(self, invadingArmies):
    if self.population > 1:
      self.population -= 1
    if self.gdp > 1:
      self.gdp -=1
    if invadingArmies > self.population * 2:
      print(self.name, "can only support ", self.population * 2, "armies")
      self.armies = self.population * 2
    else:
      self.armies = invadingArmies

  def __repr__(self):
    return "\n" + self.name + " " + self.__class__.__name__ + " with " + str(self.area) + \
        " square km " + str(self.population) + " people " + str(self.gdp) + " gdp " + \
            str(self.armies) + " armies."

  def __add__(self, other):    
    added = Empire(self.name)
    added.addNeighbours(self.neighbours)
    added.addNeighbours(other.neighbours)
    added.gdp = self.gdp + other.gdp
    if type(self) == Empire and type(other) == Teritory: 
      added.territories=self.territories
      added.territories.add(other)
    else:
      print("not an empire and teritory") 
    added.population = self.population + other.population
    added.area = self.area + other.area
    added.armies = self.armies + other.armies
    return added

class Empire(Teritory):
  def __init__(self, name):
    super().__init__(name, 0, 0, 0)
    self.territories = set()
    self.neighbours= set()
    self.conqueredTer =set()
    self.gold=0

  def endTurn(self):
    print("in this go you conquered")
    booty = 0
    if not self.conqueredTer:
      print("no territories")
    for i in self.conqueredTer:
      print(i)
      booty += i.gdp
      self =  self + i
    self.conqueredTer = set()
    print("we earned ", booty, "gold from our conquests this round")

    tax = self.population // 10 
    industrialWealth = self.gdp // 10
      
    print("we earned", tax, "from the population")
    print("we earned", industrialWealth, "from industry")
    armyCost = self.armies //10
    self.gold = self.gold - armyCost + tax + industrialWealth + booty
    print("we paid", armyCost, "to maintain our armies")
    print("we now have", self.gold, "gold")
    self.addArmies()


  def __sub__(self, other):
    self.gdp -= other.gdp
    self.population -= other.population
    self.area -= other.area
    self.territories.remove(other)

  def dead(self):
    return len(self.territories) ==0 or self.gdp == 0 or self.population == 0

  def addArmies(self):
    answer = "yes"
    while not answer == "no" and self.gold > 1:
      answer = input("add armies at 2 gold each?")
      if answer == "yes":
        print("how many armies to add?")
        armyAdd = pickNumber(self.gold//2)
        print("which territory should get the armies")
        choiceTer = pickOption(self.territories)
        if choiceTer.armies + armyAdd > choiceTer.population * 2:
          print("population can't support the army")
        else:
          choiceTer.armies += armyAdd
          print(choiceTer, "now has", choiceTer.armies)
          self.gold -= armyAdd * 2
      elif answer == "no":
        print("continue combat!")
      else:
        print("only say yes or no please!")


def pickNumber(maxi):
  while True:
    print("you can choose up to ", maxi)
    myChoice = input("how many armies? ")
    if not myChoice.isdigit():
      print("write a whole number")
    elif int(myChoice) not in range(maxi+1):
      print("pick a number between 0 and ", maxi)
    else:
      print("you chose", myChoice)
      return int(myChoice)

#read the territories from the csv file
def readCountries():
  territoryFile = open(FILENAME)
  territoryFile.readline()
  allTerritories=[]
  for line in territoryFile:
    TerritoryList = line.split(",")
    myTerritory = Teritory(TerritoryList[0], int(TerritoryList[1]), 
    int(TerritoryList[2]), int(TerritoryList[3]))
    myTerritory.addNeighbours(TerritoryList[4:len(TerritoryList)-1])
    while "" in myTerritory.neighbours:
      myTerritory.neighbours.remove("")
    allTerritories.append(myTerritory)
  return allTerritories

def pickOption(optionsIn):
  options = list(optionsIn)
  while True:
    for i in range(len(options)):
      print("choose", i, "for", options[i])
    myChoice = input ("What do you choose?")
    if not myChoice.isdigit():
      print("write a whole number")
    elif int(myChoice) not in range(len(options)):
      print("pick a number from the list")
    else:
      myChoice=int(myChoice)
      print("you chose", myChoice, "for", options[myChoice])
      return options[myChoice]
        
#find who owns the territory you are fighting
#returns rival and the territory
def findRivalTer(empireList, rivalTer):
  for otherPlayer in empireList:
    for otherTer in otherPlayer.territories:
      if rivalTer == otherTer.name:
        print("you are fighting", otherPlayer)
        return otherPlayer, otherTer
  for otherTer in world:
    if rivalTer == otherTer.name:
      print("the territory is not owned by anyone!")
      return world, otherTer
  print("no such territory")

def combat(rivalArmies, playerArmies, player, rival, ter):
  print("COMBAT")
  print(player.name, "fights", rival.name, "over", ter)
  print(rival.name, "has", rivalArmies)
  print(player.name, "has", playerArmies)
  while rivalArmies >0 and playerArmies >0:
    input("press enter to roll")
    playerRoll = randrange(1,7)
    rivalRoll = randrange(1,7)
    print("you got", playerRoll, "they got", rivalRoll)
    if playerRoll > rivalRoll:
      if rivalArmies > playerRoll - rivalRoll:
        rivalArmies -= playerRoll - rivalRoll
        print("player won and destroyed", playerRoll - rivalRoll, "armies")
      else:
        rivalArmies = 0
    elif rivalRoll > playerRoll:
      if playerArmies > rivalRoll - playerRoll:
        playerArmies -= rivalRoll - playerRoll
        print("rival won and destroyed", rivalRoll - playerRoll, "armies")
      else:
        playerArmies = 0
    else:
      print("stalemate but battle again!")
    print("now you have", playerArmies, "they have", rivalArmies)
  if playerArmies > 0:
    print("success, reap your rewards!")
    rival = rival - ter
    ter.conquered(playerArmies)
    player.conqueredTer.add(ter)
  else:
    print("we lost this time, but we will prevail!")
    ter.armies = rivalArmies

#also makes neutral "player" at position 0
def getPlayers(territoryList):
  #get info for game
  while True:
    try:
      numPlayers = int(input("How many players? "))
      numTerritories = int(input("How many territories per player? "))
      if numPlayers * numTerritories > len(territoryList):
        raise TooMany
    except(TypeError, ValueError):
      print("use whole numbers only")
      continue
    except(TooMany):
      TooMany.message()
      continue
    else:
      break

  shuffle(territoryList)
  empireList = []
  worldPos = 0
  
  #create players
  for player in range(numPlayers):
    print("player", player + 1)
    empireName = input("What is the name of your Empire? ")
    empireList.append(Empire(empireName))
    
    #add territories
    for i in range(numTerritories):
      empireList[player] = empireList[player] + territoryList[worldPos]
      worldPos += 1
    print("empire list player", empireList[player])
    print("teritory list",empireList[player].territories)

  #create a neutral "Empire"
  empireList.insert(0, Empire("neutral"))
  for i in range(worldPos, len(territoryList)):
    empireList[0] = empireList[0] + territoryList[i] 
  return empireList

def enemyNeighbours(myTers, neighbours):
  enemyList = []
  for neigh in neighbours:
    #assume that it is a valid one to attack
    #until we see it in our list of territories
    isValid = True 
    for playerTer in myTers:
      if neigh == playerTer.name:
        isValid = False
    for playerTer in currPlayer.conqueredTer:
      if neigh == playerTer.name:
        isValid = False
    if isValid:
      enemyList.append(neigh)
  return enemyList
        
#main program!
world = readCountries()  
print("**************** CONQUEST ****************")
empireList = getPlayers(world)
gameOver = False

while not gameOver:
  for currPlayer in empireList:
    if currPlayer.name=="neutral":
      print("The remaining neutral states are")
      print(currPlayer.territories)
      continue
    if not currPlayer.territories:
      print(currPlayer.name, "has lost all teritory.  Bye")
      print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
      empireList.remove(currPlayer)
      continue
    if len(empireList)<=2:
      print(currPlayer.name,"you are the winner")
      gameOver = True
      break
    currPlayer.conqueredTer = set()
    print("\n************************\n")
    print(currPlayer.name, "turn")
    for ter in currPlayer.territories:
      print(ter)
      print("our neighbours are", ter.neighbours)
    
      #Choose fight move or sentry
      ans=pickOption(["fight", "move armies", "sentry"])

      #attack
      if ans == "fight":
        validList = enemyNeighbours(currPlayer.territories, ter.neighbours)
        if len(validList) == 0:
          print("no enemy neighbours")
        else:
          print("choose who to fight")
          rivalTer = pickOption(validList)
          try:
            rivalPlayer, rivalTer = findRivalTer(empireList, rivalTer)
          except(TypeError):
            print("type error")
            print(rivalPlayer, rivalTer, empireList)
            input()
          print("how many armies to fight")
          armiesFighting = ter.armyNumber() 
          combat(rivalTer.armies, armiesFighting, currPlayer, rivalPlayer, rivalTer)
          print("\n after combat you have", ter.armies, "armies")
          print("the fought over territory has", rivalTer.armies) 

      #move armies
      elif ans == "move armies":
        valid = []
        rivalNeighbours = enemyNeighbours(currPlayer.territories, ter.neighbours)
        for neigh in ter.neighbours:
          if neigh not in rivalNeighbours:
            print(neigh)
            valid.append(neigh)
        print(valid)
        if len(valid) == 0:
          print("no friendly neighbours")
        else:
          print("where should we move the armies to")
          destination = pickOption(valid)
          print("and how many should we move?")
          numArmies = pickNumber(ter.armies-1)
          ter.armies -= numArmies
          print(ter, "now has", ter.armies, "armies")
          for i in currPlayer.territories:
            if i.name == destination:
              i.armies += numArmies
              print(i, "now has ", i.armies, "armies")
      elif ans == "sentry":
        print("there's profit in peace, earn 1 gold")
        currPlayer.gold += 1
        print("you now have ", currPlayer.gold, "gold")
      else:
        print("sorry, invalid choice")
    currPlayer.endTurn()
    