import pygame, sys , time

#----
# Prosty pong dla 2 graczy , spacja rozpoczyna gre .
#  Sterowanie graczy: 1p ArrowUP , ArrowDown ; 2p W , S 
#----
# klasy
class Ball:
	def __init__(self, screen , color , X , Y , radius):
		self.screen = screen
		self.color = color
		self.X = X
		self.Y = Y 
		self.radius = radius
		self.dx = 0 
		self.dy = 0 
		self.show()

	def show(self):
		pygame.draw.circle(self.screen , self.color , (self.X , self.Y), self.radius)
	
	def start_moving(self):
		self.dx = 15
		self.dy = 5

	def move(self):
		self.X = self.X + self.dx
		self.Y = self.Y + self.dy

	def paddle_cloison(self):
		self.dx = -self.dx
	def wall_colison(self):
		self.dy = -self.dy
	def restart_pos(self):
		self.X = WIDTH//2
		self.Y = HEIGHT//2
		self.dx = 0
		self.dy = 0
		self.show()

# gracze / lopatki
class Paddle:
	def __init__(self, screen, color, X , Y , width, height):
		self.screen = screen
		self.color = color
		self.X = X
		self.Y = Y 
		self.width = width
		self.height = height
		self.state = 'stopped'
		self.draw()

	def draw(self):
		pygame.draw.rect( self.screen, self.color, (self.X, self.Y , self.width, self.height) )
	# poruszanie sie
	def move(self):
		# poruszanie sie w gore
		if self.state == 'up':
			self.Y -= 10

		# poruszanie sie w dol
		elif self.state == 'down':
			self.Y += 10
	# fix wychodzenia poza ekran
	def screen_fix(self):
		if self.Y <= 0:
			self.Y = 0
		elif self.Y + self.height >= HEIGHT:
			self.Y = HEIGHT - self.height


# kolizja 
 
class kolizja:
	def between_ball_paddle_left(self, ball, paddle_left):
		if ball.Y + ball.radius > paddle_left.Y and ball.Y - ball.radius < paddle_left.Y + paddle_left.height:
			if ball.X - ball.radius <= paddle_left.X + paddle_left.width:
				return True
		return False

	def between_ball_paddle_right(self, ball, paddle_right):
		if ball.Y + ball.radius > paddle_right.Y and ball.Y - ball.radius < paddle_right.Y + paddle_right.height:
			if ball.X + ball.radius >= paddle_right.X:
				return True
		return False

	def between_ball_and_walls(self, ball):
		# gorna kolizja
		if ball.Y - ball.radius <= 0:
			return True
		# dolna kolizja
		if ball.Y + ball.radius >= HEIGHT:
			return True
		return False
	def spr_punkt_p1(self , ball ):
		return ball.X - ball.radius <= 0
	def spr_punkt_p2(self, ball):
		return ball.X + ball.radius >= WIDTH	

class punkty():
	def __init__(self , ekran , points , X , Y ):
		self.ekran = ekran
		self.points = points
		self.X = X
		self.Y = Y
		self.font = pygame.font.SysFont("monospace", 70, bold=True)
		self.label = self.font.render(self.points, 0, WHITE)
		self.show()

	def show(self):
		self.ekran.blit(self.label, (self.X - self.label.get_rect().width // 2, self.Y))
	
	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, WHITE)
pygame.init()

# deklaracje zmiennych
HEIGHT  = 600
WIDTH = 900
BgCOLOR = (0, 0, 0)
WHITE = (255,255,255)


EKRAN = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('pong')

# ustawienie tla + srodkowej linji
def paint_bgcolor():
	EKRAN.fill(BgCOLOR)
	pygame.draw.line( EKRAN , WHITE , (WIDTH//2,0), (WIDTH//2,HEIGHT), 5)

paint_bgcolor()

#obiekty
ball = Ball( EKRAN, WHITE , WIDTH//2 , HEIGHT//2 , 15)
paddle_left = Paddle(EKRAN , WHITE , 15 , HEIGHT//2 -60 , 20 , 120   )
paddle_right = Paddle(EKRAN , WHITE , WIDTH - 20 - 15 , HEIGHT//2 -60 , 20 , 120   )
collision = kolizja()
score1 = punkty( EKRAN , '0' , WIDTH//4 , 15 )
score2 = punkty( EKRAN , '0' , WIDTH - WIDTH//4 , 15 )


playing = False 
# zatrzymanie ekranu
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		# rozpoczecie gry i poruszanie sie
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				ball.start_moving()
				playing = True
			
			if event.key == pygame.K_w:
				paddle_left.state = 'up'

			if event.key == pygame.K_s:
				paddle_left.state = 'down'

			if event.key == pygame.K_UP:
				paddle_right.state = 'up'

			if event.key == pygame.K_DOWN:
				paddle_right.state = 'down'
		
		if event.type == pygame.KEYUP:
			paddle_left.state = 'stopped'
			paddle_right.state = 'stopped'
	if playing:
		#spowolnienie pilki
		clock = pygame.time.Clock()
		clock.tick(20)
		#poruszanie sie pilki
		paint_bgcolor()
		ball.move()
		ball.show()
		
		paddle_left.move()
		paddle_left.screen_fix()
		paddle_left.draw()

		paddle_right.move()
		paddle_right.screen_fix()
		paddle_right.draw()

		#sprawdzenie kolizjii
		if collision.between_ball_paddle_left(ball , paddle_left):
			ball.paddle_cloison()
		if collision.between_ball_paddle_right(ball , paddle_right):
			ball.paddle_cloison()
		if collision.between_ball_and_walls(ball):
			ball.wall_colison()
		if collision.spr_punkt_p2(ball):
			score1.increase()
			ball.restart_pos()
		if collision.spr_punkt_p1(ball):
			score2.increase()
			ball.restart_pos()
	score1.show()
	score2.show()

	pygame.display.update()
