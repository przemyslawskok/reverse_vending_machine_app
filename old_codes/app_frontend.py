
import socket            
import functions.usb_config as config
import functions.frontend_functions as ff
from functions.syntax import colors as c
import _thread
import time
import pygame


pygame.init()
pygame.font.init()


class frontend():
    def __init__(self):
        print("Frontend class: Initializing...")

        # self.SCREEN = pygame.display.set_mode((1280,800))
        self.SCREEN = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.INFO_FONT = pygame.font.SysFont('arial', 30 , bold = True)

        self.BACKGROUND_COLOR = (80,80,80)
        self.BORDER_COLOR = (0,0,0)

  
        self.BOTTLE_SIZE = "Brak informacji"
        self.BOTTLE_MATERIAL = "Brak informacji"
        self.BOTTLE_WEIGHT = "1"
        self.BOTTLE_LENGTH = "1"

        self.MACHINE_STATE = "Brak informacji"
        self.MACHINE_RING_SENSOR = "Brak informacji"
        self.MACHINE_END_SENSOR = "Brak informacji"

        self.MACHINE_INFO_STATE = "Stan maszyny"
        self.MACHINE_INFO_RING_SENSOR = "Stan czujnika wejściowego"
        self.MACHINE_INFO_END_SENSOR = "Stan czujnika końcowego"


        self.BOTTLE_INFO_TITLE = "Informacje live o butelce"
        self.BOTTLE_INFO_SIZE = "Rozmiar butelki:"
        self.BOTTLE_INFO_MATERIAL = "Materiał butelki:"
        self.BOTTLE_INFO_WEIGHT= "Waga butelki[g]:"
        self.BOTTLE_INFO_LENGTH = "Długość butelki[cm]:"
        
        self.DB_INFO_TITLE = "Informacje z bazy danych"
        self.DB_INFO_SIZE = "Rozmiar butelki:"
        self.DB_INFO_MATERIAL = "Materiał butelki:"
        self.DB_INFO_WEIGHT= "Waga butelki[g]:"
        self.DB_INFO_LENGTH = "Długość butelki[cm]:"
        self.DB_INFO_NAME = "Nazwa:"


        self.DB_SIZE = "2"
        self.DB_MATERIAL = "Brak informacji"
        self.DB_WEIGHT = "2"
        self.DB_LENGTH = "2"
        self.DB_NAME = "Brak informacji"

        self.BOTTLE_PROBABILITIES_TITLE = "Ostatnie wyniki modelu"
        self.BOTTLE_PROBABILITIES_HEADERS = "PL  |  MT  |  GL  |  ST  |  EM  "
        self.BOTTLE_PROBABILITIES = "Brak informacji"

        self.BOTTLE_BARCODE_TITLE = "Ostatni kod kreskowy"
        self.BOTTLE_BARCODE = "Brak informacji"


        self.COMPARE_WEIGTH = "OK"


        self.WEIGHT_DIFFRENCE = False 



        #create button as black rectangle

        self.BUTTON = pygame.Rect(50, 500, 200, 50)
  

        self.BUTTON_START_TEXT = self.INFO_FONT.render("Rozpocznij", True, (255, 255, 255))
        self.BUTTON_STOP_TEXT = self.INFO_FONT.render("Zatrzymaj", True, (255, 255, 255))


        _thread.start_new_thread(ff.receive_buffor,(self,))
        
        print(c.OK_GREEN+"Frontend class: Initialized!"+c.ENDC)
        self.gui()



    def update_screen(self): 
        self.SCREEN.fill(self.BACKGROUND_COLOR)



        pygame.draw.rect(self.SCREEN,self.BORDER_COLOR, pygame.Rect(0, 0, 1280, 150), 5)  
        pygame.draw.rect(self.SCREEN,self.BORDER_COLOR, pygame.Rect(0, 146, 550, 220), 5)          
        pygame.draw.rect(self.SCREEN,self.BORDER_COLOR, pygame.Rect(546, 146, 550, 220), 5)  
        pygame.draw.rect(self.SCREEN,self.BORDER_COLOR, pygame.Rect(1092, 146, 188, 220), 5)  
        pygame.draw.rect(self.SCREEN,self.BORDER_COLOR, pygame.Rect(0, 361, 550, 120), 5)  



        MACHINE_INFO_STATE = self.INFO_FONT.render(self.MACHINE_INFO_STATE, True, (255, 255, 255))
        self.SCREEN.blit(MACHINE_INFO_STATE, (50,30))
        MACHINE_STATE_TEXT = self.INFO_FONT.render(self.MACHINE_STATE, True, (90, 130, 255))
        self.SCREEN.blit(MACHINE_STATE_TEXT , (40,70))

        MACHINE_INFO_RING_SENSOR = self.INFO_FONT.render(self.MACHINE_INFO_RING_SENSOR, True, (255, 255, 255))
        self.SCREEN.blit(MACHINE_INFO_RING_SENSOR, (360,30))
        MACHINE_RING_SENSOR_TEXT = self.INFO_FONT.render(self.MACHINE_RING_SENSOR, True, (90, 130, 255))
        self.SCREEN.blit(MACHINE_RING_SENSOR_TEXT , (410,70))

        
        MACHINE_INFO_END_SENSOR = self.INFO_FONT.render(self.MACHINE_INFO_END_SENSOR, True, (255, 255, 255))
        self.SCREEN.blit(MACHINE_INFO_END_SENSOR, (810,30))
        MACHINE_INFO_END_SENSOR_TEXT = self.INFO_FONT.render(self.MACHINE_END_SENSOR, True, (90, 130, 255))
        self.SCREEN.blit(MACHINE_INFO_END_SENSOR_TEXT , (870,70))






        BOTTLE_INFO_TITLE = self.INFO_FONT.render(self.BOTTLE_INFO_TITLE, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_INFO_TITLE, (10,160))

        BOTTLE_INFO_SIZE = self.INFO_FONT.render(self.BOTTLE_INFO_SIZE, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_INFO_SIZE, (10,200))
        BOTTLE_SIZE_TEXT = self.INFO_FONT.render(self.BOTTLE_SIZE, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_SIZE_TEXT, (320,200))

        
        BOTTLE_INFO_MATERIAL = self.INFO_FONT.render(self.BOTTLE_INFO_MATERIAL, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_INFO_MATERIAL, (10,240))
        BOTTLE_MATERIAL_TEXT = self.INFO_FONT.render(self.BOTTLE_MATERIAL, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_MATERIAL_TEXT, (320,240))


        BOTTLE_INFO_WEIGHT = self.INFO_FONT.render(self.BOTTLE_INFO_WEIGHT, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_INFO_WEIGHT, (10,280))
        BOTTLE_WEIGHT_TEXT = self.INFO_FONT.render(self.BOTTLE_WEIGHT, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_WEIGHT_TEXT, (320,280))


        BOTTLE_INFO_LENGTH = self.INFO_FONT.render(self.BOTTLE_INFO_LENGTH, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_INFO_LENGTH, (10,320))
        BOTTLE_LENGTH_TEXT = self.INFO_FONT.render(self.BOTTLE_LENGTH, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_LENGTH_TEXT, (320,320))



        BOTTLE_PROBABILITIES_TITLE = self.INFO_FONT.render(self.BOTTLE_PROBABILITIES_TITLE, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_PROBABILITIES_TITLE, (10,370))   
        BOTTLE_PROBABILITIES_HEADERS = self.INFO_FONT.render(self.BOTTLE_PROBABILITIES_HEADERS, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_PROBABILITIES_HEADERS, (10,400))
        BOTTLE_PROBABILITIES = self.INFO_FONT.render(self.BOTTLE_PROBABILITIES, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_PROBABILITIES, (10,430))




        BOTTLE_BARCODE_TITLE = self.INFO_FONT.render(self.BOTTLE_BARCODE_TITLE, True, (255, 255, 255))
        self.SCREEN.blit(BOTTLE_BARCODE_TITLE, (10,490))
        BOTTLE_BARCODE = self.INFO_FONT.render(self.BOTTLE_BARCODE, True, (90, 130, 255))
        self.SCREEN.blit(BOTTLE_BARCODE, (10,520))

        

        DB_INFO_TITLE = self.INFO_FONT.render(self.DB_INFO_TITLE, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_TITLE, (560,160))
        DB_INFO_SIZE = self.INFO_FONT.render(self.DB_INFO_SIZE, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_SIZE, (560,200))
        DB_INFO_MATERIAL = self.INFO_FONT.render(self.DB_INFO_MATERIAL, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_MATERIAL, (560,240))
        DB_INFO_WEIGHT = self.INFO_FONT.render(self.DB_INFO_WEIGHT, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_WEIGHT, (560,280))
        DB_INFO_LENGTH = self.INFO_FONT.render(self.DB_INFO_LENGTH, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_LENGTH, (560,320))
        DB_INFO_NAME = self.INFO_FONT.render(self.DB_INFO_NAME, True, (255, 255, 255))
        self.SCREEN.blit(DB_INFO_NAME, (560,360))


        DB_SIZE_TEXT = self.INFO_FONT.render(self.DB_SIZE, True, (90, 130, 255))
        self.SCREEN.blit(DB_SIZE_TEXT, (870,200))
        DB_MATERIAL_TEXT = self.INFO_FONT.render(self.DB_MATERIAL, True, (90, 130, 255))
        self.SCREEN.blit(DB_MATERIAL_TEXT, (870,240))
        DB_WEIGHT_TEXT = self.INFO_FONT.render(self.DB_WEIGHT, True, (90, 130, 255))
        self.SCREEN.blit(DB_WEIGHT_TEXT, (870,280))
        DB_LENGTH_TEXT = self.INFO_FONT.render(self.DB_LENGTH, True, (90, 130, 255))
        self.SCREEN.blit(DB_LENGTH_TEXT, (870,320))
        DB_NAME_TEXT = self.INFO_FONT.render(self.DB_NAME, True, (90, 130, 255))
        self.SCREEN.blit(DB_NAME_TEXT, (870,360))

        #calculate diffrence as percentage

        if self.WEIGHT_DIFFRENCE == "OK":
            self.COMPARE_WEIGTH = "OK"
            COMPARE_WEIGHT= self.INFO_FONT.render(self.COMPARE_WEIGTH, True, (0, 255, 0))
            self.SCREEN.blit(COMPARE_WEIGHT, (1150,280))
        else:
            self.COMPARE_WEIGTH = "NIE OK"
            COMPARE_WEIGHT= self.INFO_FONT.render(self.COMPARE_WEIGTH, True, (255, 0, 0))
            self.SCREEN.blit(COMPARE_WEIGHT, (1150,280))


        #render button as rect
        self.BUTTON = pygame.draw.rect(self.SCREEN, (0, 255, 0), (1000, 500, 200, 80))
        self.SCREEN.blit(self.BUTTON_START_TEXT, (1020, 520))

        self.BUTTON = pygame.draw.rect(self.SCREEN, (255, 0, 0), (1000, 600, 200, 80))
        self.SCREEN.blit(self.BUTTON_STOP_TEXT, (1020, 620))

 






        pygame.display.update()
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN:
                ff.check_button_coordinates(event.x, event.y)
                print(event.x, event.y)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()





    def gui(self):
        while True:
            self.check_events()
            self.update_screen()







gui = frontend()





while True:
    continue


