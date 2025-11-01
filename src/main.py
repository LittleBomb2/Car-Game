import os
import math
import random
try:
    import pygame
except:
    os.system("pip install pygame")
    import pygame

try:
    import numpy as np
except:
    os.system("pip install numpy")
    import numpy as np

# Initializing Pygame
pygame.init()
pygame.display.set_caption("Car game 3D")

# Initializing Screen
screenWidth = input("Resolution Width: ") #640
screenHeight = input("Resolution Height: ") #640

playerName = "-1"

while playerName == "-1":
    playerName = input("Name: ")
    
    try:
        val = int(playerName)
        playerName = "-1"
    except ValueError:
        playerName = playerName

        
try:
    screenWidth = int(screenWidth)
except ValueError:
    screenWidth = 640
    
try:
    screenHeight = int(screenHeight)
except ValueError:
    screenHeight = 640

if screenWidth <= 0:
    screenWidth = 640
if screenHeight <= 0:
    screenHeight = 640
    
screen = pygame.display.set_mode((screenWidth, screenHeight))

def vectorNormalizing(vector):
    normal = np.linalg.norm(vector)

    normalized_vector = (vector / normal)

    return(normalized_vector)

def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

def ThreeD_Polygon(c, p1, p2, p3, angles, scales, color, camPos, camAngles, fov, aspect_ratio):
    # Rotation    
    az = (math.cos(angles[2]), -math.sin(angles[2]), 0, math.sin(angles[2]), math.cos(angles[2]), 0, 0, 0, 1)
    ay = (math.cos(angles[1]), 0, math.sin(angles[1]), 0, 1, 0, -math.sin(angles[1]), 0, math.cos(angles[1]))
    ax = (1, 0, 0, 0, math.cos(angles[0]), -math.sin(angles[0]), 0, math.sin(angles[0]), math.cos(angles[0]))

    ryz = (az[0] * ay[0] + az[1] * ay[3] + az[2] * ay[6], az[0] * ay[1] + az[1] * ay[4] + az[2] * ay[7], az[0] * ay[2] + az[1] * ay[5] + az[2] * ay[8], az[3] * ay[0] + az[4] * ay[3] + az[5] * ay[6], az[3] * ay[1] + az[4] * ay[4] + az[5] * ay[7], az[3] * ay[2] + az[4] * ay[5] + az[5] * ay[8], az[6] * ay[0] + az[7] * ay[3] + az[8] * ay[6], az[6] * ay[1] + az[7] * ay[4] + az[8] * ay[7], az[6] * ay[2] + az[7] * ay[5] + az[8] * ay[8])
    r = (ryz[0] * ax[0] + ryz[1] * ax[3] + ryz[2] * ax[6], ryz[0] * ax[1] + ryz[1] * ax[4] + ryz[2] * ax[7], ryz[0] * ax[2] + ryz[1] * ax[5] + ryz[2] * ax[8], ryz[3] * ax[0] + ryz[4] * ax[3] + ryz[5] * ax[6], ryz[3] * ax[1] + ryz[4] * ax[4] + ryz[5] * ax[7], ryz[3] * ax[2] + ryz[4] * ax[5] + ryz[5] * ax[8], ryz[6] * ax[0] + ryz[7] * ax[3] + ryz[8] * ax[6], ryz[6] * ax[1] + ryz[7] * ax[4] + ryz[8] * ax[7], ryz[6] * ax[2] + ryz[7] * ax[5] + ryz[8] * ax[8])

    r1 = (r[0] * p1[0] + r[1] * p1[1] + r[2] * p1[2], r[3] * p1[0] + r[4] * p1[1] + r[5] * p1[2], r[6] * p1[0] + r[7] * p1[1] + r[8] * p1[2])
    r2 = (r[0] * p2[0] + r[1] * p2[1] + r[2] * p2[2], r[3] * p2[0] + r[4] * p2[1] + r[5] * p2[2], r[6] * p2[0] + r[7] * p2[1] + r[8] * p2[2])
    r3 = (r[0] * p3[0] + r[1] * p3[1] + r[2] * p3[2], r[3] * p3[0] + r[4] * p3[1] + r[5] * p3[2], r[6] * p3[0] + r[7] * p3[1] + r[8] * p3[2])

    # Scaling
    sp1 = (r1[0] * scales[0], r1[1] * scales[1], r1[2] * scales[2])
    sp2 = (r2[0] * scales[0], r2[1] * scales[1], r2[2] * scales[2])
    sp3 = (r3[0] * scales[0], r3[1] * scales[1], r3[2] * scales[2])

    # Centering and camera
    cp1 = (sp1[0] + c[0] - camPos[0], sp1[1] + c[1] - camPos[1], sp1[2] + c[2] - camPos[2])
    cp2 = (sp2[0] + c[0] - camPos[0], sp2[1] + c[1] - camPos[1], sp2[2] + c[2] - camPos[2])
    cp3 = (sp3[0] + c[0] - camPos[0], sp3[1] + c[1] - camPos[1], sp3[2] + c[2] - camPos[2])

    point_x = [0, 0, 0]
    point_y = [0, 0, 0]

    fp1, fp2, fp3 = rotate_based_camera(cp1, cp2, cp3, [0, camAngles[1], camAngles[2]])
    fp1, fp2, fp3 = rotate_based_camera(fp1, fp2, fp3, [camAngles[0], 0, 0])
    vector1 = vectorNormalizing((fp1[0], fp1[1], clamp(fp1[2], 0, math.inf)))
    vector2 = vectorNormalizing((fp2[0], fp2[1], clamp(fp2[2], 0, math.inf)))
    vector3 = vectorNormalizing((fp3[0], fp3[1], clamp(fp3[2], 0, math.inf)))

    vector1 = vectorNormalizing((vector1[0], vector1[1], vector1[2]))
    #vector1 = vector1 + vector1 * (math.cos(vector1[0] * math.pi/2) + (math.cos(vector1[1] * math.pi/2))) / 2
    point_x[0] = (vector1[0] * (4 - math.cos(vector1[0] * math.pi/2) - math.cos(vector1[1] * math.pi/2)) * 90 / (fov * aspect_ratio / 2) * (screenWidth / 2) + (screenWidth / 2))
    point_y[0] = (vector1[1] * (4 - math.cos(vector1[0] * math.pi/2) - math.cos(vector1[1] * math.pi/2)) * 90 / (fov / 2) * (screenHeight / 2) + (screenHeight / 2))

    vector2 = vectorNormalizing((vector2[0], vector2[1], vector2[2]))
    #vector2 = vector2 * (math.cos(vector2[0] * math.pi/2) + (math.cos(vector2[1] * math.pi/2))) / 2
    point_x[1] = (vector2[0] * (4 - math.cos(vector2[0] * math.pi/2) - math.cos(vector2[1] * math.pi/2)) * 90 / (fov * aspect_ratio / 2) * (screenWidth / 2) + (screenWidth / 2))
    point_y[1] = (vector2[1] * (4 - math.cos(vector2[0] * math.pi/2) - math.cos(vector2[1] * math.pi/2)) * 90 / (fov / 2) * (screenHeight / 2) + (screenHeight / 2))
    
    vector3 = vectorNormalizing((vector3[0], vector3[1], vector3[2]))
    #vector3 = vector3 * (math.cos(vector3[0] * math.pi/2) + (math.cos(vector3[1] * math.pi/2))) / 2
    point_x[2] = (vector3[0] * (4 - math.cos(vector3[0] * math.pi/2) - math.cos(vector3[1] * math.pi/2)) * 90 / (fov * aspect_ratio  / 2) * (screenWidth / 2) + (screenWidth / 2))
    point_y[2] = (vector3[1] * (4 - math.cos(vector3[0] * math.pi/2) - math.cos(vector3[1] * math.pi/2)) * 90 / (fov / 2) * (screenHeight / 2) + (screenHeight / 2))

    if not(vector1[2] <= 0 and vector2[2] <= 0 and vector3[2] <= 0):
        pygame.draw.polygon(screen, (color[0], color[1], color[2]), ((point_x[0], point_y[0]), (point_x[1], point_y[1]), (point_x[2], point_y[2])))

def rotate_based_camera(p1, p2, p3, angles):
     # Rotation    
    az = (math.cos(-angles[2]), -math.sin(-angles[2]), 0, math.sin(-angles[2]), math.cos(-angles[2]), 0, 0, 0, 1)
    ay = (math.cos(-angles[1]), 0, math.sin(-angles[1]), 0, 1, 0, -math.sin(-angles[1]), 0, math.cos(-angles[1]))
    ax = (1, 0, 0, 0, math.cos(-angles[0]), -math.sin(-angles[0]), 0, math.sin(-angles[0]), math.cos(-angles[0]))

    ryz = (az[0] * ay[0] + az[1] * ay[3] + az[2] * ay[6], az[0] * ay[1] + az[1] * ay[4] + az[2] * ay[7], az[0] * ay[2] + az[1] * ay[5] + az[2] * ay[8], az[3] * ay[0] + az[4] * ay[3] + az[5] * ay[6], az[3] * ay[1] + az[4] * ay[4] + az[5] * ay[7], az[3] * ay[2] + az[4] * ay[5] + az[5] * ay[8], az[6] * ay[0] + az[7] * ay[3] + az[8] * ay[6], az[6] * ay[1] + az[7] * ay[4] + az[8] * ay[7], az[6] * ay[2] + az[7] * ay[5] + az[8] * ay[8])
    r = (ryz[0] * ax[0] + ryz[1] * ax[3] + ryz[2] * ax[6], ryz[0] * ax[1] + ryz[1] * ax[4] + ryz[2] * ax[7], ryz[0] * ax[2] + ryz[1] * ax[5] + ryz[2] * ax[8], ryz[3] * ax[0] + ryz[4] * ax[3] + ryz[5] * ax[6], ryz[3] * ax[1] + ryz[4] * ax[4] + ryz[5] * ax[7], ryz[3] * ax[2] + ryz[4] * ax[5] + ryz[5] * ax[8], ryz[6] * ax[0] + ryz[7] * ax[3] + ryz[8] * ax[6], ryz[6] * ax[1] + ryz[7] * ax[4] + ryz[8] * ax[7], ryz[6] * ax[2] + ryz[7] * ax[5] + ryz[8] * ax[8])

    r1 = (r[0] * p1[0] + r[1] * p1[1] + r[2] * p1[2], r[3] * p1[0] + r[4] * p1[1] + r[5] * p1[2], r[6] * p1[0] + r[7] * p1[1] + r[8] * p1[2])
    r2 = (r[0] * p2[0] + r[1] * p2[1] + r[2] * p2[2], r[3] * p2[0] + r[4] * p2[1] + r[5] * p2[2], r[6] * p2[0] + r[7] * p2[1] + r[8] * p2[2])
    r3 = (r[0] * p3[0] + r[1] * p3[1] + r[2] * p3[2], r[3] * p3[0] + r[4] * p3[1] + r[5] * p3[2], r[6] * p3[0] + r[7] * p3[1] + r[8] * p3[2])

    return(r1, r2, r3)

def rotate_based_camera_point(p1, angles):
     # Rotation    
    az = (math.cos(-angles[2]), -math.sin(-angles[2]), 0, math.sin(-angles[2]), math.cos(-angles[2]), 0, 0, 0, 1)
    ay = (math.cos(-angles[1]), 0, math.sin(-angles[1]), 0, 1, 0, -math.sin(-angles[1]), 0, math.cos(-angles[1]))
    ax = (1, 0, 0, 0, math.cos(-angles[0]), -math.sin(-angles[0]), 0, math.sin(-angles[0]), math.cos(-angles[0]))

    ryz = (az[0] * ay[0] + az[1] * ay[3] + az[2] * ay[6], az[0] * ay[1] + az[1] * ay[4] + az[2] * ay[7], az[0] * ay[2] + az[1] * ay[5] + az[2] * ay[8], az[3] * ay[0] + az[4] * ay[3] + az[5] * ay[6], az[3] * ay[1] + az[4] * ay[4] + az[5] * ay[7], az[3] * ay[2] + az[4] * ay[5] + az[5] * ay[8], az[6] * ay[0] + az[7] * ay[3] + az[8] * ay[6], az[6] * ay[1] + az[7] * ay[4] + az[8] * ay[7], az[6] * ay[2] + az[7] * ay[5] + az[8] * ay[8])
    r = (ryz[0] * ax[0] + ryz[1] * ax[3] + ryz[2] * ax[6], ryz[0] * ax[1] + ryz[1] * ax[4] + ryz[2] * ax[7], ryz[0] * ax[2] + ryz[1] * ax[5] + ryz[2] * ax[8], ryz[3] * ax[0] + ryz[4] * ax[3] + ryz[5] * ax[6], ryz[3] * ax[1] + ryz[4] * ax[4] + ryz[5] * ax[7], ryz[3] * ax[2] + ryz[4] * ax[5] + ryz[5] * ax[8], ryz[6] * ax[0] + ryz[7] * ax[3] + ryz[8] * ax[6], ryz[6] * ax[1] + ryz[7] * ax[4] + ryz[8] * ax[7], ryz[6] * ax[2] + ryz[7] * ax[5] + ryz[8] * ax[8])

    r1 = (r[0] * p1[0] + r[1] * p1[1] + r[2] * p1[2], r[3] * p1[0] + r[4] * p1[1] + r[5] * p1[2], r[6] * p1[0] + r[7] * p1[1] + r[8] * p1[2])

    return(r1)

def threeDPoint(c, p1, size, color, camPos, camAngles, fov, aspect_ratio):
    cp = (p1[0] + c[0] - camPos[0], p1[1] + c[1] - camPos[1], p1[2] + c[2] - camPos[2])
    
    p1 = rotate_based_camera_point(cp, [0, camAngles[1], camAngles[2]])
    p1 = rotate_based_camera_point(p1, [camAngles[0], 0, 0])
    
    vector1 = vectorNormalizing((p1[0], p1[1], clamp(p1[2], 0, math.inf)))
    
    point_x = (vector1[0] * (4 - math.cos(vector1[0] * math.pi/2) - math.cos(vector1[1] * math.pi/2)) * 90 / (fov / 2) * (screenWidth / 2) + (screenWidth / 2))
    point_y = (vector1[1] * (4 - math.cos(vector1[0] * math.pi/2) - math.cos(vector1[1] * math.pi/2)) * 90 / (fov / 2) * (screenHeight / 2) + (screenHeight / 2))

    distance = math.sqrt(((p1[0])**2 + (p1[1])**2 + (p1[2])**2))
    #print(distance)
    size = size / distance
    pygame.draw.circle(screen, color, (point_x, point_y), size)

def rectangle_noz(c, p1, p2, p3, p4, angles, scales, color, camPos, camAngles, fov, aspect_ratio):
  ThreeD_Polygon(c, p1, p2, p3, angles, scales, color, camPos, camAngles, fov, aspect_ratio)
  ThreeD_Polygon(c, p2, p4, p3, angles, scales, color, camPos, camAngles, fov, aspect_ratio)

def cube_noz(c, p1, p2, p3, p4, p5, p6, p7, p8, angles, scales, color, camPos, camAngles, fov, aspect_ratio):
    #rectangle_noz(c, p5, p6, p7, p8, angles, scales, (0,0,255), camPos, camAngles, fov, aspect_ratio)
    #rectangle_noz(c, p7, p8, p3, p4, angles, scales, (255,255,0), camPos, camAngles, fov, aspect_ratio)
    rectangle_noz(c, p2, p6, p4, p8, angles, scales, (255,0,255), camPos, camAngles, fov, aspect_ratio)
    rectangle_noz(c, p5, p1, p7, p3, angles, scales, (0,255,255), camPos, camAngles, fov, aspect_ratio)
    rectangle_noz(c, p1, p2, p5, p6, angles, scales, (0,255,0), camPos, camAngles, fov, aspect_ratio)
    rectangle_noz(c, p1, p2, p3, p4, angles, scales, (255,0,0), camPos, camAngles, fov, aspect_ratio)

def check_colision_square(s1, w1, h1, s2, w2, h2):
    if s1[0] + w1 > s2[0] and s1[0] < s2[0] + w2 and s1[1] - h1 < s2[1] and s1[1] > s2[1] - h2:
        return(True)
    else:
        return(False)

def main():
    # Starting clock
    clock = pygame.time.Clock()

    running = True

    aspect_ratio = screenWidth / screenHeight

    FOV_real = 180
    FOV = FOV_real
    
    currentCam = 0
    camPositions = [[0, -2, -5], [0, -5, -10], [0, -2, -0], [0, -30, 0]]
    camGroundPos = [screenHeight / 10, screenHeight / 7.5, screenHeight / 3.2, 0]
    camPos = camPositions[currentCam]

    camRotations = [[-math.pi / 8, 0, 0], [-math.pi / 8, 0, 0], [-math.pi / 16, 0, 0], [-math.pi / 2, 0, 0]]
    camRot = camRotations[currentCam]

    road_line_seperation = 4
    road_lenght = 100
    road_width = 4
    line_width = 0.2

    game = True

    #Sounds:
    point_sound = pygame.mixer.Sound("sounds/coin.wav")
    try:
        pygame.mixer.music.load('sounds/music.wav')
        pygame.mixer.music.play(-1)
    except:
        print("No music found")

    highscore = 0
    
    while game:
        lose_points_timer = 0
            
        carPos = [0, 0.6, 5]
            
        road_pos = 0
        road_speed = 1

        carPos1 = [random.uniform(-road_width, road_width), 0.6, random.uniform(60, 100)]
        carPos2 = [random.uniform(-road_width, road_width), 0.6, random.uniform(60, 100)]
        carPos3 = [random.uniform(-road_width, road_width), 0.6, random.uniform(60, 100)]
        car_speed1 = random.uniform(0.8, 1.5)
        car_speed2 = random.uniform(0.8, 1.5)
        car_speed3 = random.uniform(0.8, 1.5)

        fov_timer = 0

        points = 0

        cameraShake = 0
        
        font = pygame.font.Font('freesansbold.ttf', 32)

        replay_list = []

        score_txt = open("scores/scores.txt", "r+")
        data = score_txt.readlines()

        if playerName != "":
            for i in range(len(data)):
                if ''.join([char for char in data[i] if char.isalpha()]) == playerName:
                    highscore = int((data[i].replace(playerName + ": ", "")).replace("/n", ""))
                
        while running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game = False

            # Input
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_ESCAPE]:
                running = False
                game = False
                
            # Camera Change
            if keys_pressed[pygame.K_1]:
                currentCam = 0
            if keys_pressed[pygame.K_2]:
                currentCam = 1
            if keys_pressed[pygame.K_3]:
                currentCam = 2
            if keys_pressed[pygame.K_4]:
                currentCam = 3
                
            camRot = camRotations[currentCam]
            camPos = camPositions[currentCam]
                
            cameraShake = road_speed - 1.3

            if cameraShake < 0:
                cameraShake = 0
                
            if keys_pressed[pygame.K_w] and road_speed < 2:
                road_speed += 0.005
                if fov_timer < math.pi / 2:
                    fov_timer += 0.02
            elif keys_pressed[pygame.K_s] and road_speed > 0:
                road_speed -= 0.01
                if fov_timer > -math.pi / 2:
                    fov_timer -= 0.08
            else:
                if fov_timer >= 0.05:
                    fov_timer -= 0.05
                elif fov_timer <= -0.05:
                    fov_timer += 0.05
                else:
                    fov_timer = 0

            if keys_pressed[pygame.K_a]:
                carPos[0] -= 0.1
            elif keys_pressed[pygame.K_d]:
                carPos[0] += 0.1
                
            cameraShake += fov_timer / 4

            road_speed = clamp(road_speed, 0, 2)

            camPos = (carPos[0] + camPositions[currentCam][0], carPos[1] + camPositions[currentCam][1], carPos[2] + camPositions[currentCam][2])
            
            camPos = (camPos[0] + random.uniform(-(cameraShake / 10), (cameraShake / 10)), camPos[1] + random.uniform(-(cameraShake / 10), (cameraShake / 10)), camPos[2] + random.uniform(-(cameraShake / 10), (cameraShake / 10)))

            road_pos += road_speed

            # ROAD

            # Ground
            pygame.draw.rect(screen, (0, 0, 180), pygame.Rect(0, 0, screenWidth, camGroundPos[currentCam]))
            pygame.draw.rect(screen, (0, 153, 0), pygame.Rect(0, camGroundPos[currentCam], screenWidth, screenHeight - camGroundPos[currentCam]))
            
            if road_pos >= road_line_seperation:
                road_pos = 0
            for i in range(int(road_lenght / road_line_seperation)):
                rectangle_noz((0, 0, i * road_line_seperation - road_pos + road_line_seperation / 2 - 10), (-1, 0, 1), (1, 0, 1), (-1, 0, -1), (1, 0, -1), (0, 0, 0), (road_width, 1, road_line_seperation - line_width), (180, 180, 180), camPos, camRot, FOV, aspect_ratio)
                rectangle_noz((0, 0, i * road_line_seperation - road_pos - 10), (-1, 0, 1), (1, 0, 1), (-1, 0, -1), (1, 0, -1), (0, 0, 0), (road_width, 1, line_width), (100, 100, 100), camPos, camRot, FOV, aspect_ratio)

            # AI CAR SHIT
            carPos1[2] += car_speed1 - road_speed
            carPos2[2] += car_speed2 - road_speed
            carPos3[2] += car_speed3 - road_speed
                
            cube_noz(carPos1, (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            cube_noz(carPos2, (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            cube_noz(carPos3, (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)
      
            cube_noz(carPos, (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            replay_list.append([road_pos, [carPos[0], carPos[1], carPos[2]], [carPos1[0], carPos1[1], carPos1[2]], [carPos2[0], carPos2[1], carPos2[2]], [carPos3[0], carPos3[1], carPos3[2]], camPos])
                        
            if check_colision_square((carPos[0] - 0.8, carPos[2] + 1.8), 1.6, 3.6, (carPos1[0] - 0.8, carPos1[2] + 1.8), 1.6, 3.6):
                running = False  
            elif check_colision_square((carPos[0] - 0.8, carPos[2] + 1.8), 1.6, 3.6, (carPos2[0] - 0.8, carPos2[2] + 1.8), 1.6, 3.6):
                running = False
            elif check_colision_square((carPos[0] - 0.8, carPos[2] + 1.8), 1.6, 3.6, (carPos3[0] - 0.8, carPos3[2] + 1.8), 1.6, 3.6):
                running = False
                
            if carPos1[2] <= -20:
                carPos1[0] = random.uniform(-road_width, road_width)
                car_speed1 = random.uniform(0.8, 1.5)
                carPos1[2] = random.randint(60, 100)
                if carPos[0] > -road_width and carPos[0] < road_width:
                    points += 1
                    pygame.mixer.Sound.play(point_sound)

            if carPos2[2] <= -20:
                carPos2[0] = random.uniform(-road_width, road_width)
                car_speed2 = random.uniform(0.8, 1.5)
                carPos2[2] = random.randint(60, 100)
                if carPos[0] > -road_width and carPos[0] < road_width:
                    points += 1
                    pygame.mixer.Sound.play(point_sound)

            if carPos3[2] <= -20:
                carPos3[0] = random.uniform(-road_width, road_width)
                car_speed3 = random.uniform(0.8, 1.5)
                carPos3[2] = random.randint(60, 100)
                if carPos[0] > -road_width and carPos[0] < road_width:
                    points += 1
                    pygame.mixer.Sound.play(point_sound)

            if carPos1[2] >= 100:
                carPos1[0] = random.uniform(-road_width, road_width)
                car_speed1 = random.uniform(0.8, 1.5)
                carPos1[2] = random.randint(-20, -5)
                points -= 1
            if carPos2[2] >= 100:
                carPos2[0] = random.uniform(-road_width, road_width)
                car_speed2 = random.uniform(0.8, 1.5)
                carPos2[2] = random.randint(-20, -5)
                points -= 1
            if carPos3[2] >= 100:
                carPos3[0] = random.uniform(-road_width, road_width)
                car_speed3 = random.uniform(0.8, 1.5)
                carPos3[2] = random.randint(-20, -5)
                points -= 1

            if carPos[0] < -road_width or carPos[0] > road_width:
                lose_points_timer += 0.08
                road_speed -= 0.003
            else:
                lose_points_timer = 0
                
            if lose_points_timer >= 1:
                points -= 1
                lose_points_timer = 0
            if points < 0:
                points = 0
 
            scoreText = font.render('Points: ' + str(points), True, (255, 255, 255))
            scoreTextRect = scoreText.get_rect()
            scoreTextRect = (0, 0)
            screen.blit(scoreText, scoreTextRect)

            speedText = font.render('Speed: ' + str(int(road_speed * 432 / 2)) + 'Km/h', True, (255, 255, 255))
            speedTextRect = speedText.get_rect()
            speedTextRect.bottomleft = (0, screenHeight)
            screen.blit(speedText, speedTextRect)

            highscoreText = font.render('Highscore: ' + str(highscore), True, (255, 255, 255))
            highscoreTextRect = highscoreText.get_rect()
            highscoreTextRect.topright = (screenWidth, 0)
            screen.blit(highscoreText, highscoreTextRect)
            
            pygame.display.flip()

            pygame.display.update()

            clock.tick(60)

            #print("FPS: ", clock.get_fps())

        if playerName != "":
            isName = False

            for i in range(len(data)):
                # Find if name matches
                if ''.join([char for char in data[i] if char.isalpha()]) == playerName:
                    if points > highscore:
                        highscore = points
                        data[i] = playerName + ": " + str(points) + "\n"
                    isName = True
            if isName == False:
                score_txt.write(playerName + ": " +  str(points) + '\n')
                data.append(playerName + ": " + str(points) + "\n")
            else:
                # Clear text
                score_txt.seek(0)
                score_txt.truncate()

                # Write new data
                score_txt.writelines(data)

            score_txt.close()
        else:
            if points > highscore:
                highscore = points
        
        # Draw top10
        
        # Sort list

        if playerName != "":
            highscores = []
            names = []
            for i in range(len(data)):
                names.append(data[i].split(":", 1)[0])
                highscores.append(int((data[i].replace(names[i] + ": ", "")).replace("/n", "")))
                
            zipped_list = zip(highscores, names)
            sorted_list = sorted(zipped_list)

            print(sorted_list)
            highscoreList = []
            for i in range(len(sorted_list)):
                if i < 10:
                    highscoreList.append(str(sorted_list[len(sorted_list) - i - 1][1]) + ": " + str(sorted_list[len(sorted_list) - i - 1][0]))
            
            highscoreText = font.render('Top 10:', True, (255, 255, 255))
            
            for i in range(12):
                if i == 0:
                    highscoreTextRect = highscoreText.get_rect()
                    highscoreTextRect.midtop = (screenWidth / 2, 0)
                    
                    screen.blit(highscoreText, highscoreTextRect)
                elif i < 11:
                    highscoreSHIT = font.render(str(i) + ": " + highscoreList[i - 1], True, (255,255,255))
                    
                    highscoreTextRect = highscoreSHIT.get_rect()
                    highscoreTextRect.midtop = (screenWidth / 2, i * 35)
                    screen.blit(highscoreSHIT, highscoreTextRect)
                else:
                    for s in range(len(sorted_list)):
                        if sorted_list[len(sorted_list) - s - 1][1] == playerName:
                            highscoreSHIT = font.render(str(s + 1) + ": " + playerName + ": " + str(highscore), True, (255,255,255))
                    
                            highscoreTextRect = highscoreSHIT.get_rect()
                            highscoreTextRect.midtop = (screenWidth / 2, i * 35 + 35)
                            screen.blit(highscoreSHIT, highscoreTextRect)
        else:
            highscoreSHIT = font.render("HIGHSCORE: " + str(highscore), True, (255,255,255))
                    
            highscoreTextRect = highscoreSHIT.get_rect()
            highscoreTextRect.center = (screenWidth / 2, screenHeight / 2)
            screen.blit(highscoreSHIT, highscoreTextRect)

        text = font.render('Restart: R, Escape: ESC, Replay: M', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.midbottom = (screenWidth / 2, screenHeight - 35)
        screen.blit(text, textRect)   
        pygame.display.update()
        

        replay = False
        
        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = True
                    game = False
            
            if game == False:
                running = True
            keys_pressed = pygame.key.get_pressed()
            
            if keys_pressed[pygame.K_r]:
                running = True
            if keys_pressed[pygame.K_ESCAPE]:
                running = True
                game = False

            if keys_pressed[pygame.K_m]:
                running = True
                replay = True
                
            clock.tick(60)

        replay_pos = 0

        replay_play = True
        space_held = False

        camRot = camRotations[currentCam]
        camPos = camPositions[currentCam]
            
        while replay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    replay = False
                    running = True
                    game = False

            keys_pressed = pygame.key.get_pressed()
                        
            if keys_pressed[pygame.K_1]:
                currentCam = 0
            if keys_pressed[pygame.K_2]:
                currentCam = 1
            if keys_pressed[pygame.K_3]:
                currentCam = 2
            if keys_pressed[pygame.K_4]:
                currentCam = 3
                
            if keys_pressed[pygame.K_ESCAPE]:
                replay = False

            if keys_pressed[pygame.K_m]:
                replay_pos = 0

            if keys_pressed[pygame.K_SPACE] and not space_held:
                replay_play = not replay_play
                space_held = True
            elif not keys_pressed[pygame.K_SPACE] and space_held:
                space_held = False
                
            if keys_pressed[pygame.K_RIGHT]:
                replay_pos += 1
                replay_play = False

            if keys_pressed[pygame.K_LEFT]:
                replay_pos -= 1
                replay_play = False
                
            replay_pos = clamp(replay_pos, 0, len(replay_list) - 1)

                    
            camPos = [replay_list[replay_pos][1][0] + camPositions[currentCam][0], replay_list[replay_pos][1][1] + camPositions[currentCam][1], replay_list[replay_pos][1][2] + camPositions[currentCam][2]]
            camRot = camRotations[currentCam]
            
        
            pygame.draw.rect(screen, (0, 0, 180), pygame.Rect(0, 0, screenWidth, camGroundPos[currentCam]))
            pygame.draw.rect(screen, (0, 153, 0), pygame.Rect(0, camGroundPos[currentCam], screenWidth, screenHeight - camGroundPos[currentCam]))
            
            for i in range(int(road_lenght / road_line_seperation)):
                rectangle_noz((0, 0, i * road_line_seperation - replay_list[replay_pos][0] + road_line_seperation / 2 - 10), (-1, 0, 1), (1, 0, 1), (-1, 0, -1), (1, 0, -1), (0, 0, 0), (road_width, 1, road_line_seperation - line_width), (180, 180, 180), camPos, camRot, FOV, aspect_ratio)
                rectangle_noz((0, 0, i * road_line_seperation - replay_list[replay_pos][0] - 10), (-1, 0, 1), (1, 0, 1), (-1, 0, -1), (1, 0, -1), (0, 0, 0), (road_width, 1, line_width), (100, 100, 100), camPos, camRot, FOV, aspect_ratio)
            
            cube_noz(replay_list[replay_pos][2], (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            cube_noz(replay_list[replay_pos][3], (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            cube_noz(replay_list[replay_pos][4], (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)
      
            cube_noz(replay_list[replay_pos][1], (-1, -1, -1), (1, -1, -1), (-1, 1, -1), (1, 1, -1), (-1, -1, 1), (1, -1, 1), (-1, 1, 1), (1, 1, 1), (0, 0, 0), (1, 0.6, 2), (0, 0, 0), camPos, camRot, FOV, aspect_ratio)

            if replay_play:
                replay_pos += 1
                
            replay_pos = clamp(replay_pos, 0, len(replay_list) - 1)
            
            if replay_pos == len(replay_list) and replay_play:
                text = font.render('Restart replay: M, Race again: ESC', True, (255, 255, 255))

                textRect = text.get_rect()

                textRect.center = (screenWidth / 2, screenHeight / 2)
            
                screen.blit(text, textRect)
            
            
            pygame.display.flip()

            pygame.display.update()
                
            clock.tick(60)
            
    pygame.quit()

if __name__ == "__main__":
    main()
