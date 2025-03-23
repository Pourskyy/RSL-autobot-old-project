import pyautogui
import time
import win32api
import win32con
import tkinter as tk
import tkinter.ttk as ttk
import pygetwindow as gw
import threading
import random
import io
import sys
import json

pyautogui.FAILSAFE = False

class Image():
    def __init__(self, window):
        self.window = window
        
    def image_pos(self, img_to_check):
        elementx = self.window.x + self.window.width * img_to_check[0]
        elementy = self.window.y + self.window.height * img_to_check[1]
        #pyautogui.moveTo(elementx, elementy)
        return elementx, elementy

class ImageWindow():
    def __init__(self):
        # Trouver une fenêtre par son titre ou sa classe, ici
        #self.target_window = gw.getWindowsWithTitle("Raid: Shadow Legends")[0]
        self.target_window = gw.getWindowsWithTitle("Sans titre")[0]

        # Obtenir la taille de la fenêtre
        self.width = abs(self.target_window.width)
        self.height = abs(self.target_window.height)

        # Obtenir les coordonnées (x, y) du coin supérieur gauche de la fenêtre
        self.x = abs(self.target_window.left)
        self.y = abs(self.target_window.top)

class Farming():
    def __init__(self, image):
        # ... (other attributes and initialization)
        self.is_gemOn_var = False   
        self.image = image      
        self.img_positions = []  
        self.START_ALL = (0.95, 0.3)
        self.START_BTN = (0.95, 0.85)
        self.IN_BATTLE = (0.42, 0.91)
        
        self.text_to_insert = "" 
        self.previous_i = None  # Variable to store the previous value of i
        self.text_lock = threading.Lock()  # Initialize the lock   
    ################################-------------GLOBAL----------------################################

    def lvlup(self):
        occurences_list = [(0.55, 0.5), (0.7, 0.3), (0.9, 0.8)]  # Seules les positions de pixels sont nécessaires
    
        for img_occ in occurences_list:
            img_occx, img_occy = self.image.image_pos(img_occ)
            self.img_positions.append((img_occx, img_occy))
        
        target_color = (20, 25, 31)  # La couleur attendue
        
        all_colors_match = True  # Supposons initialement que toutes les couleurs correspondent
        
        for pos in self.img_positions:
            pixel_color = pyautogui.pixel(int(pos[0]), int(pos[1]))
            if pixel_color != target_color:#ici
                all_colors_match = False
                break  # Sortir de la boucle si une couleur ne correspond pas
        
        if all_colors_match:
            print("Toutes les couleurs correspondent à la couleur attendue !")
            # Faites ce que vous voulez lorsque toutes les couleurs correspondent
            return True
        else:
            return False

    def random_number(self):
        x = random.uniform(0.0, 20.0)
        y = random.uniform(0.0, 10.0)
        return x, y
    
    def random_spacing(self):
        # Premier niveau : déterminer si l'espacement sera court (1 à 3 secondes) ou long (10 secondes)
        if random.random() < 0.98:  # Probabilité de 90% pour un espacement court
            # Second niveau : générer un nombre aléatoire pour l'espacement court (1 à 3 secondes)
            delay = random.uniform(1.0, 3.0)
        else:
            # Espacement long : 10 secondes
            delay = 10.0
        return delay
        
    def scroll_down(self, lines):
        for _ in range(lines):
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -2, 0)
            
    def click_if_pixel_matches(self, x, y, target_color):
        pixel_color = pyautogui.pixel(x, y)
        if pixel_color in target_color:
            pyautogui.click(x, y)
            return True
        return False
    
    def fight_menu_check(self, i):
        
        startx, starty = self.image.image_pos(self.START_ALL)
        startbx, startby = self.image.image_pos(self.START_BTN)
        
        if pyautogui.pixel(int(startx), int(starty)) == (93, 25, 27):
            pyautogui.click(startbx, startby)
            i += 1
            self.text_to_insert = f"Nombre de runs {i}\n"
            return i
        else:
            print('Not in the correct instance')
            return i
                    
    ################################-------------CAMPAGNE----------------################################

    def campagne(self):
        print('campagne')
        i = 0   # The count of runs
        i = self.fight_menu_check(i)  # Check if we need to start the first fight
        print(f"Number of runs: {i}")
        
        img_replay = (0.55, 0.89, (22, 124, 156))  # send the % coords x, y and then the color value(r,g,b)
        replayx, replayy = self.image.image_pos(img_replay)
        
        img_restoreG = (0.48, 0.69, (188, 43 , 60))
        restoreGx, restoreGy = self.image.image_pos(img_restoreG)
        
        img_restoreF = (0.48, 0.69, (188, 43 , 60))
        restoreFx, restoreFy = self.image.image_pos(img_restoreF)
                
        while not self.stop_farm: # and i < 10: ici
            time.sleep(0.75)
            #check if the lvl are maxed
            if self.lvlup() is True:#True
                print('Level maxed')
                break
            
            pixel_color = pyautogui.pixel(int(replayx), int(replayy))
            
            min_rgb = (20, 110, 140)  # Minimum RGB values
            max_rgb = (25, 130, 160)  # Maximum RGB values
            
            
            if all(min_c <= c <= max_c for c, min_c, max_c in zip(pixel_color, min_rgb, max_rgb)):
                pyautogui.click(replayx, replayy)
                time.sleep(0.25)
                
                if self.is_gemOn_var is not False and pyautogui.pixel(int(restoreGx), int(restoreGy)) >= (188, 43, 60):
                    print('Refilling with gems')
                    pyautogui.click(restoreGx, restoreGy)
                    
                elif (179, 43, 60) < pyautogui.pixel(int(restoreFx), int(restoreFy)) < (188, 43, 60): 
                    print('Miam free energie')
                    pyautogui.click(restoreFx, restoreFy)
                    
                elif pyautogui.pixel(int(restoreGx), int(restoreGy)) >= (188, 43, 60) and self.is_gemOn_var is False:
                    print('No more energy')
                    break   
                else:    
                    i += 1
                    if i != self.previous_i:
                        with self.text_lock:  # Acquire the lock before updating the text
                            self.text_to_insert = f"Nombre de runs {i}\n"
                            self.previous_i = i
                    print('Number of runs: ', i)
            time.sleep(5)
        print('stopped')

    ################################-------------DONJON----------------################################

    def donjon(self):
        print('donjon')
        i = 0   # The count of runs
        i = self.fight_menu_check(i)  # Check if we need to start the first fight
        print(f"Number of runs: {i}")
        
        img_replay = (0.55, 0.89, (22, 124, 156))  # send the % coords x, y and then the color value(r,g,b)
        replayx, replayy = self.image.image_pos(img_replay)
        
        img_restoreG = (0.48, 0.69, (188, 43 , 60))
        restoreGx, restoreGy = self.image.image_pos(img_restoreG)
        
        img_restoreF = (0.48, 0.69, (188, 43 , 60))
        restoreFx, restoreFy = self.image.image_pos(img_restoreF)
                
        while not self.stop_farm:
            time.sleep(0.75)
            
            pixel_color = pyautogui.pixel(int(replayx), int(replayy))
            
            min_rgb = (20, 110, 140)  # Minimum RGB values
            max_rgb = (25, 130, 160)  # Maximum RGB values   
            
            
            if all(min_c <= c <= max_c for c, min_c, max_c in zip(pixel_color, min_rgb, max_rgb)):
                pyautogui.click(replayx, replayy)
                #print(pyautogui.pixel(int(replayx), int(replayy)))
                time.sleep(0.25)
                
                if self.is_gemOn_var is not False and pyautogui.pixel(int(restoreGx), int(restoreGy)) >= (188, 43, 60):
                    print('Refilling with gems')
                    pyautogui.click(restoreGx, restoreGy)
                    
                elif (179, 43, 60) < pyautogui.pixel(int(restoreFx), int(restoreFy)) < (188, 43, 60): 
                    print('Miam free energie')
                    pyautogui.click(restoreFx, restoreFy)
                    
                elif pyautogui.pixel(int(restoreGx), int(restoreGy)) >= (188, 43, 60) and self.is_gemOn_var is False:
                    print('No more energy')
                    break
                else:    
                    i += 1
                    if i != self.previous_i:
                        with self.text_lock:  # Acquire the lock before updating the text
                            self.text_to_insert = f"Nombre de runs {i}\n"
                            self.previous_i = i
                    print('Number of runs: ', i)
            else:
                print("Running")
                        
            time.sleep(15)
        print('stopped')
        
    ################################-------------ARENE----------------################################       

    def check_energy(self):    
        img_token = (0.90, 0.15)  # send the % coords x, y
        tokenx, tokeny = self.image.image_pos(img_token)
        target_color_token = [(236, 236, 222), (250, 233, 88), (255, 255, 220), (255, 190, 0), (174, 115, 0), (132, 126, 65), (233, 222, 82), (255, 253, 139), (243, 232, 114), (234, 223, 87), (156, 146, 45), (109, 101, 10), (184, 186, 165), (255, 251, 107), (111, 102, 3), (108, 102, 1), (252, 245, 95), (178, 167, 57), (147, 135, 22), (202, 189, 46), (212, 198, 49), (220, 204, 59), (211, 200, 60), (192, 194, 176), (220, 214, 107), (255, 254, 133), (175, 171, 110), (255, 251, 189), (255, 255, 107), (181, 175, 78), (180, 170, 52), (179, 166, 66), (255, 249, 174), (134, 128, 55), (253, 253, 249), (107, 72, 0), (127, 83, 1), (187, 130, 5), (178, 116, 0), (180, 125, 5), (171, 111, 0)]
  
        time.sleep(0.25)
        
        for y in range(int(tokeny), self.image.window.height - 10, 20):
            if y + 40 >= self.image.window.height: #si y à fini toutes la liste et n'a pas trouvé de combat
                return True
            pixel_color = pyautogui.pixel(int(tokenx), y)

            if pixel_color in target_color_token:
                pyautogui.click(tokenx, y)
                time.sleep(1)
                return True

    def start_combat(self):
        startx, starty = self.image.image_pos(self.START_ALL)
        startbx, startby = self.image.image_pos(self.START_BTN)
        
        if pyautogui.pixel(int(startx), int(starty)) == (93, 25, 27):
            pyautogui.click(startbx, startby)
        else:
            return False

    def combat_dans_arene(self):
        in_battlex, in_battley = self.image.image_pos(self.IN_BATTLE)
        continue_btn = [(255, 232, 125)]
        while True:
            time.sleep(5)
            print("en combat")
            for pixel_x in range(int(in_battlex), self.image.window.width, 15):
                if self.click_if_pixel_matches(pixel_x, int(in_battley), continue_btn):
                    pyautogui.click(pixel_x, int(in_battley))
                    time.sleep(0.5)
                    pyautogui.click(pixel_x, int(in_battley))# Effectue le clic une seconde fois
                    self.cbt += 1
                    with self.text_lock:  # Acquire the lock before updating the text
                            self.text_to_insert = f"Nombre de runs {self.cbt}\n"
                    
                    return  # Si la couleur du pixel correspond à continue_btn, la boucle s'arrête
            
    def arene(self):
        print('arene')
        iteration = 0
        self.cbt = 0
        startx, starty = self.image.image_pos(self.START_ALL)
        startbx, startby = self.image.image_pos(self.START_BTN)
        a = [(187, 130, 5), (180, 125, 5)]# yellowish color of the btn
        b = [(249, 13, 33)]#color red of the gem
        
        while not self.stop_farm and iteration < 8 and self.check_energy():      
            start_it = pyautogui.pixel(int(startx), int(starty))
            
            check = (0.49, 0.70)
            refillx, refilly = self.image.image_pos(check)
            
            if start_it == (93, 25, 27):
                print("combats found")
                pyautogui.click(startbx, startby)
                self.combat_dans_arene()
                
            elif self.is_gemOn_var and self.click_if_pixel_matches(int(refillx), int(refilly), b):
                print("hehehe")
                
            elif self.click_if_pixel_matches(int(refillx), int(refilly), a):
                print(pyautogui.pixel(int(refillx), int(refilly)))
                print("Miam free reroll")
            else:
                self.scroll_down(10)
                print('scroll, pas de combats trouvés')
                time.sleep(1.5)
                iteration += 1
        print('stopped')
        
    ################################-------------SHOP----------------################################<
            
    def acheter_produit(self, x, y, variete_image_path):
        numberx, numbery = self.random_number()
        # Clic sur les coordonnées du produit pour afficher les différentes variétés
        pyautogui.click(x + numberx, y + numbery)
        print(variete_image_path)
        time.sleep(1.25)  # Attendre un court instant pour que le menu des variétés s'affiche

        # Rechercher les différentes variétés du produit
        varietes = pyautogui.locateAllOnScreen(variete_image_path, grayscale=True, confidence=0.91)
        
        # Variable pour suivre si la confirmation d'achat a été trouvée
        confirmation_trouvee = False
        x2, y2 = None, None  # Initialiser les coordonnées x2 et y2 à None

        # Recherche de la confirmation d'achat
        for variete in varietes:
            if variete_image_path in ["images/get5000.png", "images/get44000.png", "images/get39000.png", "images/get49000.png"]:
                confirmation_trouvee = True
                x2, y2 = (variete.left + variete.width), variete.top  # Définir x2 et y2 si la variété est trouvée
                break

        if confirmation_trouvee and variete_image_path != "images/get5000.png":
            pyautogui.click(x2 - numberx, y2 + numbery)  # Effectuer le clic d'achat
            print("Achat du produit effectué.")
            time.sleep(0.25)  # A(ttendre un court instant pour revenir à l'écran principal
            pyautogui.press("esc")  # Appuyer sur la touche "Echap" pour revenir à l'écran principal
            
        elif confirmation_trouvee and variete_image_path == "images/get5000.png":
            pyautogui.click(x2 - numberx, y2 + numbery)  # Effectuer le clic d'achat
            time.sleep(1)  # Attendre un court instant pour revenir à l'écran principal
            print('shard hmm!')
        elif pyautogui.locateOnScreen('images/cancel.png', grayscale=True, confidence=0.8) is not None:
            cancel_btn = pyautogui.locateOnScreen('images/cancel.png', grayscale=True, confidence=0.8)
            pyautogui.click(cancel_btn.left + numberx, cancel_btn.top + numbery)
            print("mauvais item")
        else:
            print("shard bug")

    def acheter_produits_magasin(self, image_path, nom_produit, variete_image_path):
        produits_trouves = pyautogui.locateAllOnScreen(image_path, grayscale=True, confidence=0.92)
        time.sleep(1)

        for produit_trouve in produits_trouves:
            self.acheter_produit(produit_trouve.left, produit_trouve.top - 10, variete_image_path)
            time.sleep(1)

    def shop(self):
        print('shop')
        while not self.stop_farm:
            self.acheter_produits_magasin('images/5000.png', 'shard', 'images/get5000.png')
            self.acheter_produits_magasin('images/44000.png', 'C1', 'images/get44000.png')
            self.acheter_produits_magasin('images/39000.png', 'C2', 'images/get39000.png')
            self.acheter_produits_magasin('images/49000.png', 'C3', 'images/get49000.png')
            self.scroll_down(10)
            time.sleep(1.25)
            self.acheter_produits_magasin('images/5000.png', 'shard', 'images/get5000.png')
            self.acheter_produits_magasin('images/44000.png', 'C1', 'images/get44000.png')
            self.acheter_produits_magasin('images/39000.png', 'C2', 'images/get39000.png')
            self.acheter_produits_magasin('images/49000.png', 'C3', 'images/get49000.png')

    ################################-------------CLASSES----------------################################<
    
class rslBotGUI():
    def __init__(self, root, farming_instance, on_close_callback = None):
        self.root = root
        self.root.title("BotEngine")
        self.on_close_callback = on_close_callback
        self.root.geometry("300x320")
        self.root.config(bg="#202123")
        self.root.resizable(False, False)
        
        icon_path = "icon/favicon.ico"
        root.iconbitmap(icon_path)
        
        self.farming = farming_instance  

        # Create a Notebook widget to hold different tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Create a Frame to hold the Text widget
        frame_farms = tk.Frame(self.notebook, bg="#202123")
        self.notebook.add(frame_farms, text="Farming")  # Add the frame as a tab with the text "Text Area"

        # Create a StringVar to track the selected farm
        self.selected_farm = tk.StringVar()

        self.radio_frame = tk.Label(frame_farms, bg="#202123")
        self.radio_frame.place(relx=0, rely=0)
        # Create and pack the Radiobutton widgets for each farm
        farms = ["Campagne", "Donjon", "Arene", "Shop"]  # Add new farms here if needed
        for index, farm in enumerate(farms):
            ttk.Radiobutton(self.radio_frame, text=farm, style="Custom.TRadiobutton",
                            variable=self.selected_farm, value=farm).grid(row=index, column=0, sticky="w")
        
        self.custom_style = ttk.Style()
        self.custom_style.configure("Custom.TCheckbutton",
                                    font=("Arial", 14),
                                    foreground="white",
                                    background="#202123",
                                    focuscolor="#202123",
                                    bordercolor="#202123",
                                    indicatorsize=18,
                                    indicatormargin=5,
                                    highlightthickness=0,
                                    selectcolor="#202123"
                                    )
        self.custom_style.configure("Custom.TRadiobutton",
                                    font=("Arial", 14),
                                    foreground="white",
                                    background="#202123",
                                    focuscolor="#202123",
                                    bordercolor="#202123",
                                    indicatorsize=18,
                                    indicatormargin=5,
                                    highlightthickness=0,
                                    selectcolor="#202123"
                                    )
        self.is_gemOn_var = tk.BooleanVar()
        self.is_gemOn_button = ttk.Checkbutton(frame_farms, text="Use gems", style="Custom.TCheckbutton", variable=self.is_gemOn_var)
        self.is_gemOn_button.place(relx=0.04, rely=0.46)
        self.is_gemOn_var.trace("w", self.on_checkbox_toggle)
        
        self.start_button = tk.Button(frame_farms, text="Start", font=("Arial", 16), bg="#444654", fg="white", command=self.start_farm)
        self.start_button.place(relx=0.04, rely=0.85)

        self.stop_button = tk.Button(frame_farms, text="Stop", font=("Arial", 16), bg="#444654", fg="white", command=self.stop_farm)
        self.stop_button.place(relx=0.258, rely=0.85)

        self.quitter_button = tk.Button(frame_farms, text="Refresh", font=("Arial", 16), bg="#444654", fg="white", command=self.refresh)
        self.quitter_button.place(relx=0.465, rely=0.85)
        
        self.quitter_button = tk.Button(frame_farms, text="Quit", font=("Arial", 16), bg="#444654", fg="white", command=self.quitter)
        self.quitter_button.place(relx=0.78, rely=0.85)

        self.input_label = tk.Label(frame_farms, text="Nothing is running", font=("Arial", 10), bg="#202123", fg="#FFFFFF")
        self.input_label.place(relx=0.6, rely=0.475)

    # Create a Frame to hold the Text widget
        frame = tk.Frame(frame_farms)
        frame.place(relx= 0.04, rely=0.55) # Expand the frame to fill available space    
        
        # Create the Text widget inside the frame and use place to position it
        self.text_area = tk.Text(frame, height=4, width=30, wrap="none", font=("Arial", 12), bg="#404040", fg="white")  # Set wrap to "none"
        self.text_area.pack(fill="both", expand=True)  # Expand the Text widget to fill available space
        
        self.running = False
        self.update_thread = None
        #self.farm_run_dict = {}  # Initialize an empty farm_run_dict
        

    # Create a Frame for the second tab "Datas"
        frame_text = tk.Frame(self.notebook)
        self.notebook.add(frame_text, text="Data")  # Add the frame_text as a tab with the text "Datas"

        # Add some content to the "Datas" tab (you can customize this frame as needed)
        self.data_area_info = tk.Label(frame_text, text="Total numbers of run in :", font=("Arial", 18))
        self.data_area_info.pack()
        self.data_area = tk.Label(frame_text, text="Content for Datas Tab", font=("Arial", 12), justify="left")
        self.data_area.pack(pady=20, padx=0)  # Expand the Text widget to fill available space
        self.update_data_area()# Set the Data frame at the beginning of the app
    
    # Create a Frame for the third tab "Advanced"
        self.frame_adv = tk.Frame(self.notebook)
        self.notebook.add(self.frame_adv, text="Advanced")  # Add the frame_text as a tab with the text "Datas"
        
        
        
    #ADVANCED FRAME
        self.button_function1 = self.create_button("Fonction 1", self.add_function1)
        self.button_function2 = self.create_button("Fonction 2", self.add_function2)
        self.run_button = self.create_button("Lancer la séquence", self.run_sequence)
        self.undo_button = self.create_button("Annuler", self.undo_last_action)
        self.sequence_label = self.create_label("Séquence actuelle : ")
        self.pack_elements()
    
    def create_label(self, text):
        return tk.Label(self.frame_adv, text=text)
        
    def create_button(self, text, command):
        return tk.Button(self.frame_adv, text=text, command=command)
    
    def add_function1(self):
        self.gestion_actions.add_function(self.gestion_actions.big_functions.fonction1)
        self.update_sequence_label()

    def add_function2(self):
        self.gestion_actions.add_function(self.gestion_actions.big_functions.fonction2)
        self.update_sequence_label()

    def undo_last_action(self):
        self.gestion_actions.undo_last_action()
        self.update_sequence_label()

    def run_sequence(self):
        self.gestion_actions.run_sequence()
    
    def pack_elements(self):
        self.button_function1.pack()
        self.button_function2.pack()
        self.run_button.pack()
        self.undo_button.pack()
        self.sequence_label.pack()
    
    def on_checkbox_toggle(self, *args):
        # This function is called when the Checkbutton is toggled.
        # It will set the current state of the Checkbutton in the farming class.
        self.farming.is_gemOn_var = self.is_gemOn_var.get()
        print("Checkbutton state:", self.is_gemOn_var.get()) 
        
    def start_farm(self):
        farms = {
            "Campagne": self.farming.campagne,
            "Donjon": self.farming.donjon,
            "Arene": self.farming.arene,
            "Shop": self.farming.shop,
            # Add new farms here if needed
        }

        selected_farm = self.selected_farm.get()

        # Check if the selected farm exists in the farms dictionary
        if selected_farm in farms:
            # Call the farm function using the dictionary
            farm_function = farms[selected_farm]
            self.farming.stop_farm = False  # Reset the stop_farm flag before starting a new farm
            self.input_label.configure(text=f"{selected_farm} running")
            farm_thread = threading.Thread(target=farm_function)  # Run the farm function in a separate thread
            farm_thread.start()
            
            if not self.running:
                self.running = True
                self.update_thread = threading.Thread(target=self.update_text_area, args=(self.text_area,))
                self.update_thread.start()
                #self.update_thread_2 = threading.Thread(target=self.update_data_area)
                #self.update_thread_2.start()
                
        else:
            print("Invalid farm selection")
            
    def update_data_area(self):
        with open("./config/config.json", "r") as json_file:
            farm_run_dict = json.load(json_file)
        
        data_text = ""  # Initialize an empty string to build the text content
        
        for key, run in farm_run_dict.items():
            data_text += f"{key}: {run}\n"  # Build the text
        
        # Set the text of the data_area widget to the built data_text
        self.data_area.config(text=data_text)
            
    def update_text_area(self, text_area):
        # Redirect the standard output to update the given text area
        output_buffer = io.StringIO()

        # Load the existing farm run data from the JSON file
        try:
            with open("./config/config.json", "r") as json_file:
                self.farm_run_dict = json.load(json_file)
        except FileNotFoundError:
            self.farm_run_dict = {}  # Create an empty dictionary if the file doesn't exist

        while self.running:
            new_text = None
            with self.farming.text_lock:  # Acquire the lock
                if self.farming.text_to_insert:
                    new_text = self.farming.text_to_insert
                    self.farming.text_to_insert = ""
            if new_text:
                text_area.insert("end", new_text)
                text_area.see("end")  # Scroll to the end of the Text widget to show the new text

                # Update the JSON dictionary with the new value
                selected_farm = self.selected_farm.get()
                if selected_farm in self.farm_run_dict:
                    self.farm_run_dict[selected_farm] += 1
                else:
                    self.farm_run_dict[selected_farm] = 1

                # Save the updated farm run data to the JSON file
                with open("./config/config.json", "w") as json_file:
                    json.dump(self.farm_run_dict, json_file, indent=4)

            time.sleep(0.5)
            sys.stdout.write = output_buffer.write

    def stop_farm(self):
        self.farming.stop_farm = True  # Set stop_farm to True to stop the currently running farm
        self.input_label.configure(text="Stop running")
        self.running = False
        
    # Point d'entrée du programme
    
    def quitter(self):
        self.stop_farm()
        self.root.destroy()
    
    def refresh(self):
        self.stop_farm()  # Stop the running farm if any
        self.running = False  # Reset the running flag
        self.input_label.configure(text="Nothing is running")  # Clear the input label text
        self.selected_farm.set("")  # Reset the selected farm option
        self.text_area.delete("1.0", tk.END)  # Clear the text area content
        self.update_data_area()  # Update the data area with refreshed values
        image_window.__init__()
                
    ################################-------------GLOBAL----------------################################

if __name__ == "__main__":
    root = tk.Tk()

    # Create instances of ImageWindow and Image
    image_window = ImageWindow()
    image = Image(image_window)

    # Create an instance of Farming and pass the Image instance
    farming_instance = Farming(image)

    # Créez une instance de la classe rslBotGUI en passant l'instance de Farming
    gui_instance = rslBotGUI(root, farming_instance)
    
    # Start the Tkinter main loop
    root.mainloop()