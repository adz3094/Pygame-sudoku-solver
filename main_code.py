import pygame
import pygame_widgets as pw
import sys

#Draw board and rectangles representing cells. If cell value not zero, draw number inside cell.

def DrawGrid():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (204, 102, 153), (i * inc, j * inc, inc + 1, inc + 1))
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 15, j * inc + 10))

    for i in range(10):
        if i % 3 == 0:
            width = 10  #thick line every 3 cells
        else:
            width = 5 #thin line btween each cell
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, 500), width)  
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (500, i * inc), width)  

def StopSolving():
    global IsSolving # variable issolving is declared false when the program needs to stop
    IsSolving = False

def DrawStopButton():
    Button = pw.Button(
        screen, 200, 600, 120, 50, text='Stop',
        fontSize=20, margin=20,
        inactiveColour=(255, 0, 0),
        pressedColour=(0, 255, 0), radius=20,
        onClick=StopSolving)
    Button.listen(pygame.event.get())
    Button.draw()

def SolveGrid(gridArray, i, j):
    global IsSolving
    IsSolving = True  # Set IsSolving to True at the beginning of the solving process

    # BACKTRACKING:
    while gridArray[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            IsSolving = False  # Set IsSolving to False once the puzzle is solved
            return True
    pygame.event.pump() # keeps the game responsive

# PRUNING
    for row in range(9):
        for col in range(9):
            if isinstance(gridArray[row][col], set):
                possible_values = set(gridArray[row][col])
                
                possible_values -= set(gridArray[row]) # Remove values in the same row
                
                possible_values -= {gridArray[r][col] for r in range(9)} # Remove values in the same column
                
                block_row, block_col = row // 3 * 3, col // 3 * 3 # Remove values in the same block

                possible_values -= {gridArray[r][c] for r in range(block_row, block_row + 3) for c in range(block_col, block_col + 3)}
                gridArray[row][col] = possible_values if len(possible_values) > 1 else next(iter(possible_values))

    for row in range(9):
        for col in range(9):
            if isinstance(gridArray[row][col], set):
                if len(gridArray[row][col]) == 1:
                    gridArray[row][col] = next(iter(gridArray[row][col]))

    # Iterate over values from 1 to 9
    for V in range(1, 10):  
        if IsSolving and IsUserValueValid(gridArray, i, j, V):  
            gridArray[i][j] = V
            #recursive solving of grid 
            if IsSolving and SolveGrid(gridArray, i, j):  
                return True
            elif IsSolving:  
                gridArray[i][j] = 0
        screen.fill((255, 255, 255)) #update display whilst solving
        DrawGrid()
        DrawSelectedBox()
        DrawModes()
        DrawSolveButton()
        pygame.display.update()
        pygame.time.delay(20)
    return False

#Function to set the mouse position

def SetMousePosition(p):
    global x, y
    if p[0] < 500 and p[1] < 500:
        x = p[0] // inc
        y = p[1] // inc

# for the grid m, check validity v for the indices ii and i, jj and j
def IsUserValueValid(m, i, j, v): # m - grid, i - row ind, j - column ind, v - value to check validity
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:  #checks value validity for each row and column
            return False
    #i - row j - column ii & jj - 3 x 3 cell
    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3): #checks value validity for each cell in 3x3 block
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    
    # if both these checks do not return false
    return True

# blue box for selection

def DrawSelectedBox():
    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)

# insert valye into cell
def InsertValue(Value):
    grid[int(x)][int(y)] = Value
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))

def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True

# draw the different settings
def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 0, 0)), (30, 530))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 555))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 580))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 605))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 630))

# draw the solve button
def DrawSolveButton():
    Button = pw.Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0))
    Button.draw()
    DrawStopButton()

def DisplayMessage(Message, Interval, Color):
    screen.blit(a_font.render(Message, True, Color), (220, 530))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()

def SetGridMode(Mode):
    global grid
    screen.fill((255, 255, 255))
    DrawModes()
    DrawSolveButton()
    DrawStopButton()
    if Mode == 0:  
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    elif Mode == 1:  
        grid = [
            [4, 1, 0, 2, 7, 0, 8, 0, 5],
            [0, 8, 5, 1, 4, 6, 0, 9, 7],
            [0, 7, 0, 5, 8, 0, 0, 4, 0],
            [9, 2, 7, 4, 5, 1, 3, 8, 6],
            [5, 3, 8, 6, 9, 7, 4, 1, 2],
            [1, 6, 4, 3, 2, 8, 7, 5, 9],
            [8, 5, 2, 7, 0, 4, 9, 0, 0],
            [0, 9, 0, 8, 0, 2, 5, 7, 4],
            [7, 4, 0, 9, 6, 5, 0, 2, 8],
        ]
    elif Mode == 2:  
        grid = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
    elif Mode == 3:  
        grid = [
            [3, 2, 0, 8, 0, 7, 0, 9, 6],
            [0, 0, 0, 0, 6, 0, 0, 0, 0],
            [0, 1, 0, 9, 0, 2, 0, 4, 0],
            [8, 0, 2, 0, 0, 0, 5, 0, 1],
            [0, 3, 0, 0, 0, 0, 0, 8, 0],
            [1, 0, 4, 0, 0, 0, 9, 0, 7],
            [0, 6, 0, 1, 0, 4, 0, 7, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [2, 4, 0, 6, 0, 9, 0, 5, 3],
        ]

def ResetGrid():
    global grid
    # Reset the grid to its initial state
    SetGridMode(0)

def HandleEvents():
    global IsRunning, grid, x, y, UserValue, IsSolving
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_1:
                    UserValue = 1
                if event.key == pygame.K_2:
                    UserValue = 2
                if event.key == pygame.K_3:
                    UserValue = 3
                if event.key == pygame.K_4:
                    UserValue = 4
                if event.key == pygame.K_5:
                    UserValue = 5
                if event.key == pygame.K_6:
                    UserValue = 6
                if event.key == pygame.K_7:
                    UserValue = 7
                if event.key == pygame.K_8:
                    UserValue = 8
                if event.key == pygame.K_9:
                    UserValue = 9
                if event.key == pygame.K_c:
                    if IsUserWin() or (IsSolving and IsUserWin()):  # Check if either the player wins or the AI wins
                        SetGridMode(0)  # Reset the grid if the puzzle is solved
                    else:
                        SetGridMode(0)  # Clear the grid normally
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
    Button = pw.Button(
        screen, 350, 600, 120, 50, text='Solve',
        fontSize=20, margin=20,
        inactiveColour=(0, 0, 255),
        pressedColour=(0, 255, 0), radius=20,
        onClick=lambda: SolveGrid(grid, 0, 0))
    Button.listen(events)
    Button.draw()

# enter the user selectted valye into the grid
def DrawUserValue():
    global UserValue, IsSolving
    if UserValue > 0:
        if IsUserValueValid(grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON !", 5000, (0, 255, 0))
            else:
                UserValue = 0
        else:
            DisplayMessage("Incorrect Value !", 500, (255, 0, 0))
            UserValue = 0
# initialise main components and start the main loop
def InitializeComponent():
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    DrawSolveButton()
    DrawStopButton() 
    pygame.display.update()

# main game thread or loop for code running

def GameThread():
    IsSolving = False
    InitializeComponent()
    while IsRunning:
        HandleEvents()
        DrawGrid()
        DrawSelectedBox()
        DrawUserValue()
        pygame.display.update()

if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((500, 675))  
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  
    b_font = pygame.font.SysFont("times", 15, "bold")
    inc = 500 // 9  
    x = 0
    y = 0
    UserValue = 0
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    IsRunning = True
    IsSolving = False
    GameThread()