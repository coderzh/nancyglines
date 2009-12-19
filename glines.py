import pygame
from pygame.locals import *
import random
import math
import time
import copy
import os
from sys import exit
import md5

screenSize = (378, 420)
gameSize = (378, 378)

scoreFile = 'score'
gameTitle = 'Nancy GLines'
gameBackground = (117, 144, 174)
screenBackground = (237,236,235)
lineCount = 9
gridWidth = gameSize[0] / lineCount
gameStartPos = (0, gridWidth)
gameBorderColor = (51, 51, 51)
fontColor = (251, 102, 10)
colorList = [(255, 128, 0), (0, 255, 255), (0, 255, 0),
			 (255, 0, 255), (255, 255, 0), (0, 0, 255),
			 (255, 0, 0)]
ballBorderColor = (0, 0, 0)
ballRadius = int(gridWidth/2.5)
sBallRadius = gridWidth/10
insideBallColor = (255, 255, 255)
gameOverPos = (gameStartPos[0] + 2 * gridWidth, gameStartPos[1] + 2 * gridWidth)
gameOverContinuePos = (gameOverPos[0] + 0.5 * gridWidth, gameOverPos[1] + 1.5 * gridWidth)

pygame.init()
my_font_gameover = pygame.font.SysFont("arial", 45)
icon = pygame.image.load("glines.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(screenSize, 0, 32)
pygame.display.set_caption(gameTitle)
status = [[-1 for x in range(lineCount)] for y in range(lineCount)]
blankGridCount = lineCount * lineCount
score_font = pygame.font.SysFont("arial", 18)
score_pos = (gameStartPos[0] + 6.5 * gridWidth, 10)
highscore_pos = (gameStartPos[0] + 4 * gridWidth, 10)
activeBall = None
gameOver = False
ballCount = 0
score = 0
highscore = -1
nextBallColors = []
def display():
	"""display the balls"""
	global rx
	screen.fill(screenBackground)
	if len(nextBallColors) > 0:
		for n in range(3):
			pygame.draw.circle(screen, 
							   ballBorderColor,
								(gridWidth * (n + 1), gridWidth/2),
								ballRadius,
								1)
			pygame.draw.circle(screen, 
							   colorList[nextBallColors[n]],
							   (gridWidth * (n + 1), gridWidth/2),
							   ballRadius - 1)
	text_score = score_font.render('Your:' + str(score), True, (0, 0, 255))
	screen.blit(text_score, score_pos)
	text_hightscore = score_font.render('Highest:' + str(highscore), True, (255, 0, 255))
	screen.blit(text_hightscore, highscore_pos)
	pygame.draw.rect(screen, gameBackground, ((gameStartPos[0], gameStartPos[1]), (gameSize[0], gameSize[1])))
	for x in range(lineCount):
		pygame.draw.line(screen, 
						 gameBorderColor, 
						 (gameStartPos[0], gameStartPos[1] + x * gridWidth), 
						 (gameStartPos[0] + gameSize[0], gameStartPos[1] + x * gridWidth))
		pygame.draw.line(screen, 
						 gameBorderColor, 
						 (gameStartPos[0] + x * gridWidth, gameStartPos[1]), 
						 (gameStartPos[0] + x * gridWidth, gameStartPos[1] + gameSize[1]))
		for y in range(lineCount):
			if status[x][y] <> -1:
				pygame.draw.circle(screen, 
								   ballBorderColor,
								   (gameStartPos[0] + x * gridWidth + gridWidth/2, gameStartPos[1] + y * gridWidth + gridWidth/2),
								   ballRadius,
								   1)
				pygame.draw.circle(screen, 
								   colorList[status[x][y]],
								   (gameStartPos[0] + x * gridWidth + gridWidth/2, gameStartPos[1] + y * gridWidth + gridWidth/2),
								   ballRadius - 1)
				#draw small ball
				sx = x * gridWidth + gridWidth*2/3
				sy = y * gridWidth + gridWidth/3
				sc = insideBallColor
				if activeBall <> None and activeBall[0] == x and activeBall[1] == y:
					sc = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
					if abs(rx) < x * gridWidth + gridWidth / 3:
						rx = x * gridWidth + gridWidth / 3
					if rx > x * gridWidth + gridWidth * 2 / 3:
						rx = -(x * gridWidth + gridWidth * 2 / 3)
					if rx < 0:
						sx = abs(rx)
						sy = y * gridWidth + gridWidth / 2 + math.sqrt((gridWidth/6)**2 - (x * gridWidth + gridWidth / 2 - sx)**2)
					elif rx > 0:
						sx = rx
						sy = y * gridWidth + gridWidth / 2 - math.sqrt((gridWidth/6)**2 - (x * gridWidth + gridWidth / 2 - sx)**2)
					rx += 2
				pygame.draw.circle(screen, sc, (sx + gameStartPos[0], int(sy) + gameStartPos[1]), sBallRadius)
	if gameOver:
		text_gameOver = my_font_gameover.render("Game Over!", True, (130, 20, 80))
		text_gameOverContinue = score_font.render("Press Enter to continue...", True, (0, 0, 0))
		screen.blit(text_gameOver, gameOverPos)
		screen.blit(text_gameOverContinue, gameOverContinuePos)
	pygame.display.update()

def getThreeBalls():
	global ballCount
	global nextBallColors
	getBallCount = 0
	while getBallCount < 3:
		x = random.randint(0,lineCount - 1)
		y =random.randint(0,lineCount - 1)
		if status[x][y] == -1:
			status[x][y] = nextBallColors[getBallCount]
			ballCount += 1
			getBallCount += 1
			clearBalls((x, y, status[x][y]))
	
def getNextBallColor():
	global nextBallColors
	nextBallColors = []
	for i in range(3):
		color = random.randint(0, len(colorList) - 1)
		nextBallColors.append(color)
def getBallNum(ball, vector):
	count = 0
	x = ball[0]
	y = ball[1]
	while True:
		x += vector[0]
		y += vector[1]
		if x in range(lineCount) and y in range(lineCount) and status[x][y] == ball[2]:
			count += 1
		else:
			break
	return count
def clearBalls(ball):
	clearCount = 0
	global ballCount
	global score
	lcount = getBallNum(ball, (-1, 0))
	rcount = getBallNum(ball, (1, 0))
	
	ucount = getBallNum(ball, (0, -1))
	dcount = getBallNum(ball, (0, 1))
	
	lucount = getBallNum(ball, (-1, -1))
	rdcount = getBallNum(ball, (1, 1))
	
	rucount = getBallNum(ball, (1, -1))
	ldcount = getBallNum(ball, (-1, 1))
	
	if lcount + rcount >= 4:
		for x in range(ball[0] - lcount, ball[0] + rcount + 1):
			status[x][ball[1]] = -1
		clearCount += (lcount + rcount)
	if ucount + dcount >= 4:
		for y in range(ball[1] - ucount, ball[1] + dcount + 1):
			status[ball[0]][y] = -1
		clearCount += (ucount + dcount)
	if lucount + rdcount >= 4:
		for x in range(-lucount, rdcount + 1):
			status[ball[0] + x][ball[1] + x] = -1
		clearCount += (lucount + rdcount)
	if rucount + ldcount >= 4:
		for x in range(-ldcount, rucount + 1):
			status[ball[0] + x][ball[1] - x] = -1
		clearCount += (rucount + ldcount)
	if clearCount > 0:
		ballCount -= (clearCount + 1)
		score += 1 + clearCount + (clearCount - 4) * 2
		return True
	return False

def movecheck(curPos, nextPos, tarPos, pathStat):
	nextlen = len(pathStat[curPos[0]][curPos[1]]) + 1
	nextx = nextPos[0]
	nexty = nextPos[1]
	if nextx in range(lineCount) and nexty in range(lineCount) and status[nextx][nexty] == -1:
		tarlen = len(pathStat[nextx][nexty])
		if tarlen == 0 or (tarlen > 0 and nextlen < tarlen):
			pathStat[nextx][nexty] = copy.deepcopy(pathStat[curPos[0]][curPos[1]])
			pathStat[nextx][nexty].append((nextx, nexty))
			if nextPos <> tarPos:
				move((nextx, nexty), tarPos, pathStat)
def move(curPos, tarPos, pathStat):
	tarlen = len(pathStat[tarPos[0]][tarPos[1]])
	nextlen = len(pathStat[curPos[0]][curPos[1]]) + 1
	if tarlen > 0 and nextlen >= tarlen:
		return
	movecheck(curPos, (curPos[0] + 1, curPos[1]), tarPos, pathStat)#right
	movecheck(curPos, (curPos[0], curPos[1] + 1), tarPos, pathStat)#down
	movecheck(curPos, (curPos[0] - 1, curPos[1]), tarPos, pathStat)#left
	movecheck(curPos, (curPos[0], curPos[1] - 1), tarPos, pathStat)#up
def updatehighscore():
	if score > highscore:
		createscorefile(score)
def createscorefile(scoreNum):
	global highscore
	n = str(scoreNum * 62)
	mn = str(scoreNum * 91)
	f = open(scoreFile, 'wb')
	f.writelines(md5.new(mn).digest() + n)
	f.close()
	highscore = scoreNum
def readscorefile():
	global highscore
	f = open(scoreFile, 'rb')
	s = f.readline()
	try:
		n = int(s[16:]) / 62
		if s[:16] <> md5.new(str(n*91)).digest():
			createscorefile(0)
		else:
			highscore = n
	except:
		createscorefile(0)
def initgame():
	global status
	global score
	global highscore
	global gameOver
	global ballCount
	global activeBall
	
	status = [[-1 for x in range(lineCount)] for y in range(lineCount)]
	score = 0
	gameOver = False
	activeBall = None
	getNextBallColor()
	getThreeBalls()
	getNextBallColor()
	ballCount = 3
	if not os.path.exists(scoreFile):
		createscorefile(0)
	else:
		readscorefile()
if __name__ == '__main__':
	initgame()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == KEYDOWN:
				if event.key == K_RETURN:
					initgame()
		while not gameOver:
			for event in pygame.event.get():
				if event.type == QUIT:
					updatehighscore()
					exit()
				elif event.type == MOUSEBUTTONDOWN:
					mousePos = pygame.mouse.get_pos()		
					x = (mousePos[0] - gameStartPos[0]) / gridWidth
					y = (mousePos[1] - gameStartPos[1]) / gridWidth
					if x in range(lineCount) and y in range(lineCount):
						if status[x][y] <> -1:
							activeBall = (x, y, status[x][y])
							rx = x * gridWidth + gridWidth*2/3
						elif status[x][y] == -1 and activeBall <> None:
							pathStat = [[[] for nx in range(lineCount)] for ny in range(lineCount)]
							move((activeBall[0], activeBall[1]), (x, y), pathStat)
							ballPath = pathStat[x][y]
							if len(ballPath) > 0:
								preX, preY = activeBall[0], activeBall[1]
								for (nX, nY) in ballPath:
									status[preX][preY] = -1
									status[nX][nY] = activeBall[2]
									preX, preY = nX, nY
									display()
									time.sleep(0.05)
								if not clearBalls((x, y, activeBall[2])):
									if ballCount > lineCount**2 - 3:
										gameOver = True
										break
									getThreeBalls()
									getNextBallColor()
									if ballCount == lineCount**2:
										gameOver = True
										activeBall = None
										break
								activeBall = None
			display()
			time.sleep(0.02)
		updatehighscore()
		display()
		time.sleep(0.02)