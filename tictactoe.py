import pygame
from network import Network

# Initialize pygame
# Solve play sounds latency
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.font.init()

# Palette - RGB colors
blue = (78, 140, 243)
light_blue = (100, 100, 255)
red = (242, 89, 97)
light_red = (255, 100, 100)
dark_grey = (85, 85, 85)
light_grey = (100, 100, 100)
background_color = (225, 225, 225)

# Create the window
width = 300
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Player images
crossImg = pygame.image.load('gameData/Images/crossImg.png')
circleImg = pygame.image.load('gameData/Images/circleImg.png')

X_score = pygame.image.load('gameData/Images/X_scoreImg.png')
O_score = pygame.image.load('gameData/Images/O_scoreImg.png')

# Menu Images
playBtn = pygame.image.load('gameData/Images/button1Img.png')
playBtn_rect = playBtn.get_rect()
playBtn_rect.center = (150, 156)
logo = pygame.image.load('gameData/Images/logo.png')

def main():
    running = True
    while running:
        screen.fill(background_color)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if playBtn_rect.collidepoint((mx, my)):
                    playSound('gameData/Sounds/buttonSound.wav')
                    gameDisplay()

        screen.blit(logo, (8, 25))
        pygame.draw.rect(screen, dark_grey, (45, 120, 210, 73))
        screen.blit(playBtn, (50, 125))
        pygame.display.update()

def gameDisplay():
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player ", player)

    running = True
    while running:
        clock.tick(60)
        try:
            game = n.send("connected")
        except:
            running = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            row, col = int(mouse[0] / 100), int(mouse[1] / 100)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if row < 3 and col < 3 and game.board[row][col] == '' and game.connected() and game.playerTurn == player:
                    playSound('gameData/Sounds/buttonSound.wav')
                    data = "playerMove,"+str(row)+","+str(col)
                    n.send(data)
            elif game.win:
                playSound('gameData/Sounds/resetSound.wav')
                n.send("resetBoard")
            elif game.tie:
                playSound('gameData/Sounds/nopeSound.mp3')
                n.send("resetBoard")


        redrawWindows(screen,game,player)



def redrawWindows(screen, game,player):
    screen.fill(background_color)
    if not game.connected():
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("Waiting for Player...", 1, (0, 0, 0))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height()/2))
    else:
        for row in range(3):
            for col in range(3):
                pos = (row * 100 + 6, col * 100 + 6)
                if game.board[row][col] == 'X':
                    screen.blit(crossImg, pos)
                elif game.board[row][col] == 'O':
                    screen.blit(circleImg, pos)
        borderWidth = 5
        color = dark_grey
        pygame.draw.line(screen, color, (100, 0), (100, 300), borderWidth)
        pygame.draw.line(screen, color, (200, 0), (200, 300), borderWidth)
        pygame.draw.line(screen, color, (0, 100), (300, 100), borderWidth)
        pygame.draw.line(screen, color, (0, 200), (300, 200), borderWidth)
        # Boards
        pygame.draw.rect(screen, color, (0, 0, 5, 300))
        pygame.draw.rect(screen, color, (0, 0, 300, 5))
        pygame.draw.rect(screen, color, (295, 0, 5, 300))

        # Score
        pygame.draw.rect(screen, dark_grey, (0, 300, 300, 70))
        pygame.draw.rect(screen, light_grey, (5, 305, 290, 60))

        if player == 0:
            playerRole = 'X'
        elif player == 1:
            playerRole = 'O'
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render('You Are %s Player' % playerRole , 1, (255, 255, 255))
        screen.blit(text, (width / 2 - text.get_width() / 2, 305))

        screen.blit(X_score, (45, 330))
        screen.blit(O_score, (230, 330))
        font = pygame.font.Font('freesansbold.ttf', 32)
        scoreboard = font.render(': %d - %d :' % (game.score[0], game.score[1]), True, background_color, light_grey)
        screen.blit(scoreboard, (94, 330))

        if game.playerTurn == player:
            font = pygame.font.Font('freesansbold.ttf', 18)
            text = font.render("You Turn..", 1, (0, 0, 0))
            screen.blit(text, (width / 2 - text.get_width() / 2, 375))
        else:
            font = pygame.font.Font('freesansbold.ttf', 18)
            text = font.render("Waiting for the opponent..", 1, (0, 0, 0))
            screen.blit(text, (width / 2 - text.get_width() / 2, 375))
        if game.win:
            pygame.time.wait(1000)

    pygame.display.update()


def playSound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

if __name__ == "__main__":
	main()