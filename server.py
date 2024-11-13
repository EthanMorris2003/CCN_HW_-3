import threading
import pygame
import socket
import sys
import random
import pynput

posx = 300
posy = 375 
score = 0  
falling_speed = 5  

def GameThread():
    global posx, posy, score, falling_speed, missed

    pygame.init()

    background = (204, 230, 255)
    bucketColor = (0, 51, 204)  
    fallingColor = (255, 0, 0)  

    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 600, 400

    falling_object = pygame.Rect(0, 0, 15, 15) 
    
    bucket = pygame.Rect(0, 0, 60, 15)  
    
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Bucket Catch Game')

    missed = 0
    font = pygame.font.SysFont('Arial', 24) 
    game_over_font = pygame.font.SysFont('Arial', 40)  
    button_font = pygame.font.SysFont('Arial', 30) 

    while True:
        screen.fill(background) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if missed >= 1:
                    if restart_button.collidepoint(event.pos):
                        RestartGame()
                        continue  

        if missed >= 1:
            game_over_text = game_over_font.render("Game Over!", True, (0, 0, 0))
            text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
            screen.blit(game_over_text, text_rect) 

            restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 200, 50)
            pygame.draw.rect(screen, (0, 255, 0), restart_button) 
            button_text = button_font.render("Restart", True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=restart_button.center)
            screen.blit(button_text, button_text_rect)  

        else:
            bucket.center = (posx, posy)

            falling_object.y += falling_speed

            collision = bucket.colliderect(falling_object)
            if collision:
                falling_object.y = 0  
                falling_object.x = random.randint(0, screen_width - falling_object.width)  
                score += 1 

                if score < 40: 
                    if score % 5 == 0:  
                        falling_speed += 1

            if falling_object.y > screen_height:
                falling_object.y = 0
                falling_object.x = random.randint(0, screen_width - falling_object.width) 
                missed += 1 

            pygame.draw.rect(screen, fallingColor, falling_object)

            pygame.draw.rect(screen, bucketColor, bucket)

            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (screen_width - 150, 20))

        pygame.display.update()  
        fps.tick(60) 

def ServerThread():
    global posy, posx
    host = "127.0.0.1"
    port = 5000  

    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
    except OSError as e:
        print(f"Error binding to port {port}: {e}")
        return
    
    print("Server enabled on", host)
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from:", address)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        
        print("from connected user:", data)
        if data == 'w':
            posy -= 10
        elif data == 's':
            posy += 10
        elif data == 'a':
            posx -= 10
        elif data == 'd':
            posx += 10
    conn.close()

def RestartGame():
    global posx, posy, score, falling_speed, missed
    posx = 300 
    posy = 375 
    score = 0  
    falling_speed = 5  
    missed = 0 

if __name__ == '__main__':
    server_thread = threading.Thread(target=ServerThread)
    server_thread.daemon = True  
    server_thread.start()
    
    GameThread()