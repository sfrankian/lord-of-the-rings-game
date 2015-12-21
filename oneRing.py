#Stephanie Frankian and Caylene Parrish 
#CS111 Project
# The One Ring Hunt

from Tkinter import *
import random

#size of each cell that Frodo travels through
sizeOfStep = 50
stockColor='black' #stock color for the foreground (which is replaced with the landscapes)
huntColor='gray30' #the color shown behind frodo and behind each object (the ring, and evilObjs)

class Hunt:
    '''The class Hunt creates the GUI using dimensions width and height'''
    def __init__(self, width, height):
        #these elements are provided when the user chooses either a medium or hard
        #game
        self.width = width
        self.height = height
        self.F = []
        
        for i in range(height):
            self.F.append([])
   
class OneRing(Toplevel):
    '''The class OneRing uses the GUI created to display a scene where the 
    user must hope that the next direction (up,down,left,right) chosen does 
    not also see the randomized creation of an evil object there. The evil objects 
    are harmless if they are added to the scene and you do not land on them, serving
    as a visual obstruction to the user. The game ends when the Ring is found or 
    when the user 'hits' (or steps on to a step where a new evil object is created)
    and decrements the tally to -100.'''   
    def __init__(self, width, height):
        #initializes Toplevel, which will allow for the dynamism of the game
        Toplevel.__init__(self)
        self.width = width
        self.height = height
        #calling on the previously made class Hunt for the GUI creation
        self.OR = Hunt(self.width, self.height)
        #setting the title of the game
        self.title('The One Ring Hunt')
        self.grid()
        #initializing the createWidgets method, which contains the 
        # information used to design the game (frodo picture, journeyPicture)
        self.createWidgets()
        #if the difficulty is 'Easy', then the point counter starts at 0 since the
        #ring is visible
        if difficulty == 'Easy':
            self.pointCounter = 0
        else: 
            #for 'medium', the point counter starts at 100, since the incident
            #of injury is greater and the ring is hidden from sight
            self.pointCounter = 50
        
    def setHuntLabel(self, img, clr, row, col):
        '''The setHuntLabel method creates a method that represents each
        cell's appearance, location, and size. This is how each cell looks when Frodo is 
        not on it'''
        self.huntLabels[row][col].destroy()
        #creating the label that displays in all locations (essentially, it is
        #either mordor, moria, or the shire, depending on the user's choice
        self.huntLabels[row][col] = Label(self, image=img, bg=clr, width=sizeOfStep, height=sizeOfStep)
        #sets each row and column to the image that the user chooses as the journey location
        #moria, mordor, shire
        self.huntLabels[row][col].img = img
        #grids the image in all cells
        self.huntLabels[row][col].grid(row=row,column=col,sticky=N+E+W+S)
    def setFrodoLabel(self):
        #creates the label for Frodo, whose position will be tracked due to the
        #ability we have of moving him around via arrow keys
        row = self.frodoPosition[0]
        col = self.frodoPosition[1]
        #set the label to the picture of frodo in the specific cell he is in
        self.setHuntLabel(self.frodoImage, huntColor, row, col)
        #when one's mouse goes over Frodo, it returns the message defined below
        self.huntLabels[row][col].bind('<Enter>', self.frodoMouseEnter)
        self.huntLabels[row][col].bind('<Leave>', self.mouseLeave)

    def frodoMouseEnter(self, event):
        '''The method frodoMouseEnter temporarily changes the banner text'''
        self.banner.set('Feed me lembas bread to fortify my health!')

    def mouseLeave(self, event):
        '''The method mouseLeave reverts the banner to the original message'''
        self.banner.set(self.bannerText)

    def setRingLabel(self):
        '''the method setRingLabel changes the journeyImage in a specific cell to
        the image of the Ring, which serves as Frodo's objective.'''
        self.setHuntLabel(self.ringImage, huntColor,self.ringPosition[0], self.ringPosition[1])
        #on scrolling over the Ring label, the message is flashed on entering, and reverts
        #to the original on leaving
        self.huntLabels[self.ringPosition[0]][self.ringPosition[1]].bind('<Enter>', self.ringMouseEnter)
        self.huntLabels[self.ringPosition[0]][self.ringPosition[1]].bind('<Leave>', self.mouseLeave)
    def ringMouseEnter(self, event):
        '''Changes the banner message to a different message'''
        self.banner.set('The Ring is near')

    def bindArrowKeys(self):
        '''The method bindArrowKeys binds the directional movements to their 
        respective keys'''
        self.bind('<Left>', self.leftKey)  # When left arrow key is pressed, invoke self.leftKey method
        self.bind('<Right>', self.rightKey)  # When right arrow key is pressed, invoke self.rightKey method
        self.bind('<Up>', self.upKey)  # When up arrow key is pressed, invoke self.upKey method
        self.bind('<Down>', self.downKey)  # When down arrow key is pressed, invoke self.downKey method

    def unbindArrowKeys(self):
        '''Conversely, unbindArrowKeys unbinds the keys, namely when the game is over
        (upon reaching -100 or the Ring)'''
        self.unbind('<Left>')
        self.unbind('<Right>')
        self.unbind('<Up>')
        self.unbind('<Down>')

    def leftKey(self, event):
        '''The method leftKey becomes relevant when the user moves left, causing
        a series of methods 'truth' to be checked and consequently run'''
        #saves Frodo's movements (ie location)
        row = self.frodoPosition[0]
        col = self.frodoPosition[1]
        self.frodoPosition = (row, col-1) #changes his location to one less
        #or one to the left
        self.setHuntLabel(self.changingImage,huntColor,row,col) #changes the image 
        #of the previous cell to that of the journey
        self.setFrodoLabel() #resets Frodo's image at his new location
        self.frodoAteBread()  #checks to see if Frodo ate bread (shared same position)
                                # to increment to his points
        self.isFrodoAtEvil()  #checks to see if Frodo stepped into a cell at the same time
                            #that an evil object was generated and placed there
        self.frodoHitEvil  #detracts 50 if this is the case (only if Frodo's position
                            # = position of newly placed evil)
        self.losingBattle() #checks to see if the game reached -100; is so, the game is ended
        self.handleGameOver() #checks to see if the ring was retrieved by Frodo

    def rightKey(self, event):
        '''The method rightKey becomes relevant when the user moves right, causing
        a series of methods 'truth' to be checked and consequently run'''
        row = self.frodoPosition[0]
        col = self.frodoPosition[1]
        self.frodoPosition = (row, col+1)
        self.setHuntLabel(self.changingImage,huntColor,row,col) #changes the image 
        #of the previous cell to that of the journey
        self.setFrodoLabel() #resets Frodo's image at his new location
        self.frodoAteBread()  #checks to see if Frodo ate bread (shared same position)
                                # to increment to his points
        self.isFrodoAtEvil()  #checks to see if Frodo stepped into a cell at the same time
                            #that an evil object was generated and placed there
        self.frodoHitEvil  #detracts 50 if this is the case (only if Frodo's position
                            # = position of newly placed evil)
        self.losingBattle() #checks to see if the game reached -100; is so, the game is ended
        self.handleGameOver() #checks to see if the ring was retrieved by Frodo
    def upKey(self, event):
        '''The method upKey becomes relevant when the user moves up, causing
        a series of methods 'truth' to be checked and consequently run'''
        row = self.frodoPosition[0]
        col = self.frodoPosition[1]
        self.frodoPosition = (row-1, col)
        self.setHuntLabel(self.changingImage,huntColor,row,col) #changes the image 
        #of the previous cell to that of the journey
        self.setFrodoLabel() #resets Frodo's image at his new location
        self.frodoAteBread()  #checks to see if Frodo ate bread (shared same position)
                                # to increment to his points
        self.isFrodoAtEvil()  #checks to see if Frodo stepped into a cell at the same time
                            #that an evil object was generated and placed there
        self.frodoHitEvil  #detracts 50 if this is the case (only if Frodo's position
                            # = position of newly placed evil)
        self.losingBattle() #checks to see if the game reached -100; is so, the game is ended
        self.handleGameOver() #checks to see if the ring was retrieved by Frodo

    def downKey(self, event):
        '''The method downKey becomes relevant when the user moves down, causing
        a series of methods 'truth' to be checked and consequently run'''
        row = self.frodoPosition[0]
        col = self.frodoPosition[1]
        self.frodoPosition = (row+1, col)
        self.setHuntLabel(self.changingImage,huntColor,row,col) #changes the image 
        #of the previous cell to that of the journey
        self.setFrodoLabel() #resets Frodo's image at his new location
        self.frodoAteBread()  #checks to see if Frodo ate bread (shared same position)
                                # to increment to his points
        self.isFrodoAtEvil()  #checks to see if Frodo stepped into a cell at the same time
                            #that an evil object was generated and placed there
        self.frodoHitEvil  #detracts 50 if this is the case (only if Frodo's position
                            # = position of newly placed evil)
        self.losingBattle() #checks to see if the game reached -100; is so, the game is ended
        self.handleGameOver() #checks to see if the ring was retrieved by Frodo
        
    ########### The code for checking positions #############   
    
    def isFrodoAtRing(self):
        '''The method isFrodoAtRing() checks to see if Frodo and the Ring share the same position.
        If this is true, then handleGameOver() is invoked to shut down the game'''
        return (self.frodoPosition[0]==self.ringPosition[0]) and (self.frodoPosition[1]==self.ringPosition[1])  
             
    def isFrodoAtBread(self):
        '''The method isFrodoAtBread() checks to see if Frodo and the lembas bread share the 
        same position. If so, then frodoAteBread() is invoked to increment Frodo's point tally'''
        return (self.frodoPosition[0] == self.breadx) and (self.frodoPosition[1] == self.bready)
        
    def handleGameOver(self):
        '''If frodo and  the ring share the same position, then the GUI is updated to show different
        messages displaying that the user has won, and also increments the tally by 100. The arrow keys
        are unbound, and a quit button appears to allow easy exist from the canvas'''
        if self.isFrodoAtRing():
            self.bannerText = 'You found the Ring! Humanity is restored (or is it?)'
            self.banner.set(self.bannerText) #set the banner to the new message
            self.pointCounter = self.pointCounter + 100 #increment by 100
            self.points.set('Points: '+ str(self.pointCounter))
            #creates quit button for easy exit
            quitButton = Button(self,fg='black',bg='CornflowerBlue',text = 'Leave Middle Earth', command = self.onQuitButtonClick)
            quitButton.grid(row=10,column= 0)
            self.unbindArrowKeys() #unbinding arrow keys to stop movement
            
    def losingBattle(self): 
        '''The method losingBattle() checks to see if the pointCounter = -100. If
        so, then the game is ended, with appropriate messages of doom displayed. A quit button
        is created for easy exit'''
        if self.pointCounter <= -100: 
            self.bannerText = 'Sauron has taken over Middle Earth'
            self.banner.set(self.bannerText) #change the banner to the sad message
            self.points.set('Sauron wins') #replaces the point counter
            self.banner.set(self.bannerText)
            #creates quitButton to allow for easy exit
            quitButton = Button(self,fg='black',bg='CornflowerBlue',text = 'Leave Middle Earth', command = self.onQuitButtonClick)
            quitButton.grid(row=5,column= 5)
            self.unbindArrowKeys() #restricts movement after condition has been met
            
    def frodoAteBread(self):
        '''The method frodoAteBread() checks if isFrodoAtBread() is true. If it 
        is, then differing amounts of points are incremented to the total'''
        if self.isFrodoAtBread():
            self.bannerText= 'Lembas Bread. A few bites can feed a grown man!'
            self.banner.set(self.bannerText) #changes the bannerText 
            if difficulty == "Easy": #if the difficulty chosen was easy, then
                                #only 30 are added
                self.pointCounter = self.pointCounter + 30
            else:                   #if medium, then 50 are incremented
                self.pointCounter = self.pointCounter + 50
            self.points.set('Points: '+ str(self.pointCounter)) #resets the point counter
            self.banner.set(self.bannerText)

    def onQuitButtonClick(self):
        '''The method onQuitButtonClick will demolish the GUI when clicked 
        on. '''
        self.destroy()      
                                                                        
    def createWidgets(self):
        '''The method createWidgets creates and stores the labels, images, buttons, etc. that 
        are used in most of the other methods in the game'''
        # Hunt labels, which change the appearance of the cell       
        self.huntLabels = []
        self.changingImage = journeyStep  # ChangingImage, whose default is the chosen journeyStep (moria, mordor)
        for i in range(self.height): #for each row
            self.huntLabels.append([])
            for j in range(self.width): #for each column
                #change the huntLabel image to the default image
                self.huntLabels[i].append(Label(self,image=self.changingImage,width=sizeOfStep,height=sizeOfStep))
                clr = stockColor #the stockColor serves as a filler
                self.setHuntLabel(self.changingImage,clr,i,j)

        # Ring image and Frodo image
        if difficulty == 'Easy': #the ring is visible for the game
            self.ringImage = PhotoImage(file = 'oneRing.gif')
        else: 
            #obstructs the Ring from view
            self.ringImage = journeyStep
        #randomly choosing a location for the ring
        self.ringPosition = (self.height-random.randint(1,11), self.width- random.randint(0,11))  # Position of ring
        self.setRingLabel() #updating the label accordingly
        #saving the frodoImage as that which was chosen by the user
        self.frodoImage = frodoChoice
        self.frodoPosition = (1,1)  # Frodo's starting position
        self.setFrodoLabel()
    
        # Banner label   
        self.banner = StringVar()
        self.bannerLabel = Label(self,bg=stockColor,fg=huntColor,font='Verdana 18',textvariable=self.banner)
        self.bannerText = 'Guide Frodo to the One Ring. Lembas might help!'
        self.banner.set(self.bannerText) #update the banner
        self.bannerLabel.grid(row=self.height,columnspan=self.width,sticky=N+E+W+S)

        #Creating the lembas bread by randomly choosing an x and y value
        self.breadx = random.randint(0,10)
        self.bready = random.randint(0,10)
        bread = PhotoImage(file='lembasBread.gif'),
        breadLabel = Label(self, image = bread, bg='gray30')
        breadLabel.bread = bread
        breadLabel.grid(row=self.breadx, column=self.bready) #placing the lembas 
 
        # Points Counter, which by saving as a StringVar allows for changes later
        self.points = StringVar()
        self.showPointCounter = Label(self, fg='red', bg='gray30', font='Verdana 20 bold',textvariable = self.points)
        self.showPointCounter.grid(row=0,column=9,columnspan=2)
        self.points.set('Points: 0')
        # Movement with arrow keys
        self.bindArrowKeys()
    
    def isFrodoAtEvil(self): 
        '''The method isFrodoAtEvil randomly generates the location of 
        the evil objects, saruman, gollum and theEye. '''
        self.evilObj = ['saruman.gif','gollum.gif','theEye.gif']
        for i in range(0,15): #runs 15 times in one loop
            incidentOfEvil = random.randint(1,5) #randomly chooses a #
            for j in range(0,len(self.evilObj)): #for the three evil objects
                if j+1 == incidentOfEvil: #if an object equals an index of evil
                    evil = PhotoImage(file = self.evilObj[j]) #save the object as evil
                    evilx =random.randint(1,10) #randomly generate an x and y
                    evily = random.randint(0,10)
                    evilLabel = Label(self, image = evil, bg='gray30')
                    evilLabel.evil = evil
                    evilLabel.grid(row=evilx, column=evily) #put the image on the GUI
                    #if Frodo steps on to the evil object the same time it is generated. 
                    #then points are detracted when frodoHitEvil() is run
                    if (self.frodoPosition[0]== evilx) and (self.frodoPosition[1]==evily):
                        return self.frodoHitEvil()
    def frodoHitEvil(self):
        '''The method frodoHitEvil changes the banner and decrements the points'''
        self.bannerText= 'Ouch. You hit an evil object.'
        self.banner.set(self.bannerText)
        self.pointCounter = self.pointCounter - 50
        self.points.set('Points: '+ str(self.pointCounter))
        self.banner.set(self.bannerText)  


class DifficultyChoice(Tk): 
    '''Creating a class which allows the user to choose their
    difficulty level for the One Ring Catch: globlin (or easy) or ringwraith(medium). 
    Upon clicking one of the three buttons, the window
    disappears, and the One Ring Catch game with the correct difficulty 
    specifications begins. '''
    def __init__(self):
        Tk.__init__(self)
        self.OR_app = None #saves this for later usage
        self.title('The One Ring Hunt')
        self.configure(bg='CornflowerBlue')  #background is blue
        #saves the names and the gif images for the user's leg of the journey choice
        self.journeyWords = [' Shire ',' Moria ','Mordor']
        self.journey = ['shire.gif','moria.gif','mordor.gif']
        
        #saves the images and the names for the user's Frodo choice
        self.frodoApparel = ['teenyFrodo.gif','stylishFrodo.gif','smokingFrodo.gif']
        self.frodoWords = [' Travel Frodo', 'Stylish Frodo', '  Shire Frodo']
        self.grid()
        
        self.addInfo() #adds the information labels
        self.buttonCreation()   #creates all of the buttons
        
    def addInfo(self): 
        '''The method adds the  message 'Customize Frodo...' to the screen as 
        well as both the Journey and the Frodo labels, whose text is updating
        when the user chooses from among the radio buttons that are created for
        each journey leg (Shire, Moria, and Mordor) and for each Frodo costume 
        (Travelling, Stylish, Longbottom Leaf). The frodo image also changes with
        the specific frodo chosen'''
        #creating the label infoLabel which contains words of wisdom for the game
        self.info = StringVar()
        self.infoLabel = Label(self, fg='blue', bg='CornflowerBlue', font='Console 20 bold', textvariable=self.info)
        self.info.set('Customize Frodo for his journey to Mount Doom!')
        self.infoLabel.grid(row=1,columnspan=2)
        #to update which journey was chosen
        self.journeyChoice = StringVar()
        self.journeyLabel = Label(self,fg='blue', bg='CornflowerBlue', font = 'Times 14 bold', textvariable= self.journeyChoice)
        self.journeyChoice.set('Journey : ')
        self.journeyLabel.grid(row=2,column = 1,sticky=S+W) #grid to the south and west
        
        #to update the label displaying which frodo has been chosen
        self.frodo = StringVar()
        self.frodoLabel = Label(self,fg='blue', bg='CornflowerBlue',font = 'Times 14 bold', textvariable= self.frodo)
        self.frodo.set('Apparel : ')
        self.frodoLabel.grid(row=2,column = 1)    
        
        #to create the label that displays which frodo image you chose
        choosingFrodo = PhotoImage(file = 'teenyfrodo.gif') #the default image, at first
        self.iLabel = Label(self,image=choosingFrodo,bg='CornflowerBlue',borderwidth=3)
        self.iLabel.choosingFrodo = choosingFrodo
        self.iLabel.grid(row=1,column=0,sticky=W) #grids to the west in row 1
        
        #the title banner, in position row 0 and column 1
        landscape = PhotoImage(file = 'titleBanner.gif')
        self.landscapeLabel = Label(self,image=landscape,borderwidth=3)
        self.landscapeLabel.landscape = landscape
        self.landscapeLabel.grid(row=0,column=1,sticky=N+E) 
        
        self.whichJourneyStep= IntVar() #saves as an integer
        for i in range(0, len(self.journeyWords)): 
            #creates enough radio buttons for each element in journeyWords (3 total)
            radioButtons = Radiobutton(self,fg = 'blue', bg='CornflowerBlue',text = self.journeyWords[i], value = i, variable = self.whichJourneyStep)
            radioButtons.grid(row = i+3, column = 1, sticky=N+S+W) #increments their location
            
        self.whichFrodo= IntVar() #integer
        for f in range(0, len(self.frodoWords)): 
            #creates enough radio buttons as required
            radioB = Radiobutton(self,fg = 'blue', bg='CornflowerBlue', text = self.frodoWords[f], value = f, variable = self.whichFrodo)
            radioB.grid(row = f+3, column = 1, sticky=N+S ) #gridded to north and south
        
    def buttonCreation(self):
        '''The method buttonCreation creates 4 buttons'''
        #easy button, with command=self.onEasyButtonClick
        easyButton = Button(self, fg='blue', bg='CornflowerBlue', text='Difficulty: Goblin', command=self.onEasyButtonClick)
        easyButton.grid(row=2,column = 10, sticky=N+E+W+S)
        #medium button, with command=self.onMediumButtonClick
        mediumButton = Button(self, fg='blue', bg='CornflowerBlue', text='Difficulty: Ringwraith', command=self.onMediumButtonClick)
        mediumButton.grid(row=3,column = 10, sticky=N+E+W+S)
        
        #quit button, with command=self.onQuitButtonClick
        quitButton = Button(self,fg='black',bg='CornflowerBlue',text = 'Leave Middle Earth', command = self.onQuitButtonClick)
        quitButton.grid(row=10,column= 0)
        
        # Change picture button goes here, with command=self.onUpdateClick
        changeButton = Button(self,text='Update Game Specs', bg='CornflowerBlue',command = self.onUpdateClick)
        changeButton.grid(row = 10, column = 1, sticky=S)
        
    def onUpdateClick(self): 
        '''The method onUpdateClick() will, based on which radio button is chosen
        display the proper picture and text'''
        for i in range(0,len(self.journey)): #goes through each image file
            if self.whichJourneyStep.get() == i: #if the chosen radio equals one of the saved elements
                global journeyPic #globalizing, since it is used in onEasy and onMediumButtonClick
                journeyPic = PhotoImage(file = self.journey[i])
                self.journeyChoice.set('Journey:  ' + str(self.journeyWords[i]))
                
        for f in range(0,len(self.frodoApparel)): #goes through each apparel item
            if self.whichFrodo.get() == f:  #if the chosen radio equals an element
                global frodopic #globalizing, for later use
                frodopic = PhotoImage(file = self.frodoApparel[f]) #show the image as frodo
                self.frodo.set('Apparel:  ' + str(self.frodoWords[f]))
                self.iLabel.configure(image=frodopic) # change Label's image, so chosen
                                                    #frodo is displayed on the screen
                # store image, otherwise gets deleted when UI refreshes
                self.iLabel.image = frodopic 
                
    def onEasyButtonClick(self):
        '''The method onEasyButtonClick() globalizes the difficulty for later reference
        in the OneRing class as well as globalizes journeyPic (moria, mordor, shire) and 
        the chosen Frodo to change the appearance of the GUI. It then runs OneRing() in a 
        new GUI'''
        global difficulty
        difficulty = 'Easy'
        global journeyStep #to save the journeyStep for use in the game
        journeyStep = journeyPic
        
        global frodoChoice #to save the frodo chosen
        frodoChoice = frodopic
        
        if self.OR_app!=None:
            self.OR_app.destroy()  # Destroy existing OneRing app
        self.OR_app = OneRing(11,11) #runs the new GUI
        self.OR_app.mainloop()

    def onMediumButtonClick(self):
        '''The method onMediumButtonClick() globalizes the difficulty for later reference
        in the OneRing class as well as globalizes journeyPic (moria, mordor, shire) and 
        the chosen Frodo to change the appearance of the GUI. It then runs OneRing() in a 
        new GUI. It differs from onEasyButtonClick because the ring is not visible'''
        global difficulty #globalizing difficulty for use in OneRing
        difficulty = 'Medium'
        global journeyStep #to save the journeyStep for use in the game
        journeyStep = journeyPic
        
        global frodoChoice #to save the frodo chosen
        frodoChoice = frodopic
        
        if self.OR_app!=None: 
            self.OR_app.destroy()  # Destroy existing OneRing app
        self.OR_app = OneRing(11,11) #new Gui
        self.OR_app.mainloop()
  
    def onQuitButtonClick(self):
        '''The method onQuitButtonClick will demolish the GUI when clicked 
        on. '''
        self.destroy()
#runs the entire program
app = DifficultyChoice()
app.mainloop()