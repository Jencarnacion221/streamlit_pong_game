import pygame, sys, random
import streamlit as st

#Functions done as to ensure code is more modular and looks cleaner
def ball_animation(): #This is done to make ball moved
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1

	# Player Score
	if ball.right >= screen_width:
		player_score += 1
		score_time = pygame.time.get_ticks()

	# Opponent Score
	if ball.left <= 0: 
		opponent_score += 1		
		score_time = pygame.time.get_ticks()


	if ball.colliderect(player) or ball.colliderect(opponent):
		ball_speed_x *= -1

#This ensures the player doesn't go beyond the screen by automatically teleporting them to the boundary if they attempt to get past it
def player_animation():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

#Makes enemy work
def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

#This randomizes the movement of the pong ball everytime it goes past the place
def ball_start():
	global ball_speed_x, ball_speed_y, score_time
	current_time = pygame.time.get_ticks()
	ball.center = (screen_width/2, screen_height/2)
	player.center = (10, screen_height / 2 - 70)
	opponent.center = (screen_width - 20, screen_height / 2 - 70)

	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))

	if 700 < current_time - score_time < 1400:
		number_three = basic_font.render("2",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))

	if 1400 < current_time - score_time < 2100:
		number_three = basic_font.render("1",False,light_grey)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))


	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0, 0
	else:
		ball_speed_y = 8 * random.choice((1,-1))
		ball_speed_x = 8 * random.choice((1,-1))
		score_time = None

# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1200
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
opponent = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10,140)
player = pygame.Rect(10, screen_height / 2 - 70, 10,140)

# Game Variables
ball_speed_x = 8 * random.choice((1,-1))
ball_speed_y = 8 * random.choice((1,-1))
player_speed = 0
opponent_speed = 10

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Score Timer
score_time = None



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 10
			if event.key == pygame.K_DOWN:
				player_speed += 10
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 10
			if event.key == pygame.K_DOWN:
				player_speed -= 10
	
	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()

	# Visuals 
	screen.fill(bg_color)
	pygame.draw.rect(screen, light_grey, player)
	pygame.draw.rect(screen, light_grey, opponent)
	pygame.draw.ellipse(screen, light_grey, ball)
	pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))

	if score_time:
		ball_start()

	opponent_text = basic_font.render(f"{opponent_score}",False,light_grey)
	screen.blit(opponent_text,(660,470))

	player_text = basic_font.render(f'{player_score}',False,light_grey)
	screen.blit(player_text,(500,470))

	pygame.display.flip()
	clock.tick(60)
