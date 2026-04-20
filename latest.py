import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class WeddingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Planner")
        self.root.state('zoomed')
        self.selected_theme = None
        self.selected_event = None  # For corporate/birthday events
        self.selected_food = None
        self.theme_cost = 0
        self.event_cost = 0  # For corporate/birthday events
        self.food_cost = 0
        self.total_cost = 0
        self.food_prices = {"Basic": 500, "Elite": 1000, "Premium": 2000}
        
        self.setup_main_window()
    
    def setup_main_window(self):
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Load background image
        bg_image = Image.open("background2.png")
        bg_image = bg_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Theme colors
        self.TEXT_COLOR = "#FFD700"  # Gold
        self.HIGHLIGHT_COLOR = "#FFECB3"  # Lighter gold for highlights
        
        # Load icon images
        self.wedding_normal, self.wedding_zoom = self.load_image_pair("wedding2.png", (150, 150))
        self.birthday_normal, self.birthday_zoom = self.load_image_pair("birthday.png", (150, 150))
        self.corporate_normal, self.corporate_zoom = self.load_image_pair("corporate.png", (150, 150))
        
        # Create icon blocks
        self.create_icon_block(self.wedding_normal, self.wedding_zoom, "Wedding", self.wedding_clicked, 0.2)
        self.create_icon_block(self.birthday_normal, self.birthday_zoom, "Birthday", self.birthday_clicked, 0.5)
        self.create_icon_block(self.corporate_normal, self.corporate_zoom, "Corporate Events", self.corporate_clicked, 0.8)
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def load_image_pair(self, path, size, zoom_factor=1.1):  # Increased zoom factor
        try:
            img = Image.open(path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Process image to remove white background
            data = img.getdata()
            new_data = []
            for item in data:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            
            normal = ImageTk.PhotoImage(img.resize(size))
            zoomed = ImageTk.PhotoImage(img.resize((int(size[0]*zoom_factor), int(size[1]*zoom_factor))))
            return normal, zoomed
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            blank_img = Image.new('RGBA', size, (0, 0, 0, 0))
            blank = ImageTk.PhotoImage(blank_img)
            return blank, blank
    
    def create_icon_block(self, normal_img, zoom_img, text, command, relx):
        x = self.screen_width * relx
        y = self.screen_height * 0.5
        
        img_item = self.canvas.create_image(x, y-50, image=normal_img, tags=("clickable",))
        text_item = self.canvas.create_text(x, y+50, text=text, 
                                          font=("Helvetica", 14, "bold"),
                                          fill=self.TEXT_COLOR,
                                          tags=("clickable",))
        
        # Bind events to both image and text
        for item in [img_item, text_item]:
            self.canvas.tag_bind(item, "<Enter>", lambda e, img=img_item, z=zoom_img: 
                               self.canvas.itemconfig(img, image=z))
            self.canvas.tag_bind(item, "<Leave>", lambda e, img=img_item, n=normal_img: 
                               self.canvas.itemconfig(img, image=n))
            self.canvas.tag_bind(item, "<Button-1>", lambda e, cmd=command: cmd())
    
    def wedding_clicked(self):
        self.create_theme_window()
    
    def birthday_clicked(self):
        self.create_birthday_window()
    
    def corporate_clicked(self):
        self.create_corporate_window()
    
    def create_birthday_window(self):
        self.birthday_window = tk.Toplevel(self.root)
        self.birthday_window.title("Birthday Events")
        self.birthday_window.state('zoomed')
        
        # Create canvas for the birthday window
        birthday_canvas = tk.Canvas(self.birthday_window, highlightthickness=0)
        birthday_canvas.pack(fill="both", expand=True)
        
        # Set background
        bg_birthday_image = Image.open("birthdayback.jpeg")
        bg_birthday_image = bg_birthday_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_birthday_photo = ImageTk.PhotoImage(bg_birthday_image)
        birthday_canvas.create_image(0, 0, image=self.bg_birthday_photo, anchor="nw")
        birthday_canvas.bg_image = self.bg_birthday_photo
        
        # Birthday event image sizes
        self.event_width = 350
        self.event_height = 250
        
        # Load birthday event images
        self.theme_img = self.load_theme_image("theme.jpeg", (self.event_width, self.event_height))
        self.theme_img_zoom = self.load_zoomed_image("theme.jpeg", (self.event_width, self.event_height))
        
        self.elegant_img = self.load_theme_image("elegant.jpeg", (self.event_width, self.event_height))
        self.elegant_img_zoom = self.load_zoomed_image("elegant.jpeg", (self.event_width, self.event_height))
        
        # Create birthday event display items
        y_position = self.screen_height * 0.35
        
        # Birthday event data
        self.birthday_events = [
            {"x": 0.3, "image": self.theme_img, "zoomed": self.theme_img_zoom, 
             "name": "Theme Party", "price": 200000, "frame": None, "label": None},
            {"x": 0.7, "image": self.elegant_img, "zoomed": self.elegant_img_zoom,
             "name": "Glamourous Theme", "price": 300000, "frame": None, "label": None}
        ]
        
        # Create clickable birthday event elements
        for event in self.birthday_events:
            # Create frame with gold border
            event["frame"] = tk.Frame(birthday_canvas, bg=self.TEXT_COLOR, bd=3, relief="solid")
            event["frame"].place(x=self.screen_width*event["x"]-self.event_width//2-5, 
                               y=y_position-self.event_height//2-5,
                               width=self.event_width+10, 
                               height=self.event_height+10)
            
            # Create image label inside frame
            event["label"] = tk.Label(event["frame"], image=event["image"], bd=0)
            event["label"].pack(padx=3, pady=3)
            
            # Bind hover events
            event["label"].bind("<Enter>", lambda e, ev=event: self.on_event_enter(ev))
            event["label"].bind("<Leave>", lambda e, ev=event: self.on_event_leave(ev))
            event["label"].bind("<Button-1>", lambda e, ev=event: self.event_selected(ev))
            
            # Event name and price
            birthday_canvas.create_text(self.screen_width*event["x"], y_position + self.event_height//2 + 40, 
                                   text=f"{event['name']}\n₹{event['price']:,}", 
                                   font=("Helvetica", 14, "bold"), 
                                   fill=self.TEXT_COLOR)
        
        # Back button
        back_btn = tk.Button(self.birthday_window, text="Back", command=self.birthday_window.destroy,
                           bg="#4a4a4a", fg=self.TEXT_COLOR, font=("Helvetica", 12, "bold"))
        back_btn.place(relx=0.5, rely=0.85, anchor="center", width=200, height=40)
    
    def create_corporate_window(self):
        self.corporate_window = tk.Toplevel(self.root)
        self.corporate_window.title("Corporate Events")
        self.corporate_window.state('zoomed')
        
        # Create canvas for the corporate window
        corporate_canvas = tk.Canvas(self.corporate_window, highlightthickness=0)
        corporate_canvas.pack(fill="both", expand=True)
        
        # Set background
        bg_corporate_image = Image.open("corpfood.jpeg")
        bg_corporate_image = bg_corporate_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_corporate_photo = ImageTk.PhotoImage(bg_corporate_image)
        corporate_canvas.create_image(0, 0, image=self.bg_corporate_photo, anchor="nw")
        corporate_canvas.bg_image = self.bg_corporate_photo
        
        # Corporate event image sizes
        self.event_width = 350
        self.event_height = 250
        
        # Load corporate event images
        self.agm_img = self.load_theme_image("agm.jpeg", (self.event_width, self.event_height))
        self.agm_img_zoom = self.load_zoomed_image("agm.jpeg", (self.event_width, self.event_height))
        
        self.award_img = self.load_theme_image("award.jpeg", (self.event_width, self.event_height))
        self.award_img_zoom = self.load_zoomed_image("award.jpeg", (self.event_width, self.event_height))
        
        self.freshers_img = self.load_theme_image("freshers.jpeg", (self.event_width, self.event_height))
        self.freshers_img_zoom = self.load_zoomed_image("freshers.jpeg", (self.event_width, self.event_height))
        
        # Create corporate event display items
        y_position = self.screen_height * 0.35
        
        # Corporate event data
        self.corporate_events = [
            {"x": 0.2, "image": self.agm_img, "zoomed": self.agm_img_zoom, 
             "name": "AGM", "price": 300000, "frame": None, "label": None},
            {"x": 0.5, "image": self.award_img, "zoomed": self.award_img_zoom,
             "name": "Award Function", "price": 500000, "frame": None, "label": None},
            {"x": 0.8, "image": self.freshers_img, "zoomed": self.freshers_img_zoom,
             "name": "Fresher's Party", "price": 400000, "frame": None, "label": None}
        ]
        
        # Create clickable corporate event elements
        for event in self.corporate_events:
            # Create frame with gold border
            event["frame"] = tk.Frame(corporate_canvas, bg=self.TEXT_COLOR, bd=3, relief="solid")
            event["frame"].place(x=self.screen_width*event["x"]-self.event_width//2-5, 
                               y=y_position-self.event_height//2-5,
                               width=self.event_width+10, 
                               height=self.event_height+10)
            
            # Create image label inside frame
            event["label"] = tk.Label(event["frame"], image=event["image"], bd=0)
            event["label"].pack(padx=3, pady=3)
            
            # Bind hover events
            event["label"].bind("<Enter>", lambda e, ev=event: self.on_event_enter(ev))
            event["label"].bind("<Leave>", lambda e, ev=event: self.on_event_leave(ev))
            event["label"].bind("<Button-1>", lambda e, ev=event: self.event_selected(ev))
            
            # Event name and price
            corporate_canvas.create_text(self.screen_width*event["x"], y_position + self.event_height//2 + 40, 
                                   text=f"{event['name']}\n₹{event['price']:,}", 
                                   font=("Helvetica", 14, "bold"), 
                                   fill=self.TEXT_COLOR)
        
        # Back button
        back_btn = tk.Button(self.corporate_window, text="Back", command=self.corporate_window.destroy,
                           bg="#4a4a4a", fg=self.TEXT_COLOR, font=("Helvetica", 12, "bold"))
        back_btn.place(relx=0.5, rely=0.85, anchor="center", width=200, height=40)
    
    def on_event_enter(self, event):
        event["label"].config(image=event["zoomed"])
        event["frame"].config(bg=self.HIGHLIGHT_COLOR)
    
    def on_event_leave(self, event):
        event["label"].config(image=event["image"])
        event["frame"].config(bg=self.TEXT_COLOR)
    
    def event_selected(self, event):
        self.selected_event = event
        self.event_cost = event["price"]
        if hasattr(self, 'corporate_window'):
            self.corporate_window.destroy()
        elif hasattr(self, 'birthday_window'):
            self.birthday_window.destroy()
        self.show_food_catalog(event["name"], event["price"])
    
    def create_theme_window(self):
        self.theme_window = tk.Toplevel(self.root)
        self.theme_window.title("Wedding Themes")
        self.theme_window.state('zoomed')
        
        # Create canvas for the theme window
        theme_canvas = tk.Canvas(self.theme_window, highlightthickness=0)
        theme_canvas.pack(fill="both", expand=True)
        
        # Set background
        bg_theme_image = Image.open("background6.jpeg")
        bg_theme_image = bg_theme_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_theme_photo = ImageTk.PhotoImage(bg_theme_image)
        theme_canvas.create_image(0, 0, image=self.bg_theme_photo, anchor="nw")
        theme_canvas.bg_image = self.bg_theme_photo
        
        # Theme image sizes
        self.theme_width = 350
        self.theme_height = 250
        
        # Load theme images
        self.posh_img = self.load_theme_image("posh2.jpeg", (self.theme_width, self.theme_height))
        self.posh_img_zoom = self.load_zoomed_image("posh2.jpeg", (self.theme_width, self.theme_height))
        
        self.traditional_img = self.load_theme_image("traditional2.jpeg", (self.theme_width, self.theme_height))
        self.traditional_img_zoom = self.load_zoomed_image("traditional2.jpeg", (self.theme_width, self.theme_height))
        
        self.hybrid_img = self.load_theme_image("hybrid.jpeg", (self.theme_width, self.theme_height))
        self.hybrid_img_zoom = self.load_zoomed_image("hybrid.jpeg", (self.theme_width, self.theme_height))
        
        # Create theme display items
        y_position = self.screen_height * 0.35
        
        # Theme data
        self.themes = [
            {"x": 0.2, "image": self.posh_img, "zoomed": self.posh_img_zoom, 
             "name": "Lavish", "price": 300000, "frame": None, "label": None},
            {"x": 0.5, "image": self.traditional_img, "zoomed": self.traditional_img_zoom,
             "name": "Traditional", "price": 200000, "frame": None, "label": None},
            {"x": 0.8, "image": self.hybrid_img, "zoomed": self.hybrid_img_zoom,
             "name": "Hybrid", "price": 250000, "frame": None, "label": None}
        ]
        
        # Create clickable theme elements with enhanced hover effects
        for theme in self.themes:
            # Create frame with gold border
            theme["frame"] = tk.Frame(theme_canvas, bg=self.TEXT_COLOR, bd=3, relief="solid")
            theme["frame"].place(x=self.screen_width*theme["x"]-self.theme_width//2-5, 
                               y=y_position-self.theme_height//2-5,
                               width=self.theme_width+10, 
                               height=self.theme_height+10)
            
            # Create image label inside frame
            theme["label"] = tk.Label(theme["frame"], image=theme["image"], bd=0)
            theme["label"].pack(padx=3, pady=3)  # Small padding to show border
            
            # Bind hover events
            theme["label"].bind("<Enter>", lambda e, t=theme: self.on_theme_enter(t))
            theme["label"].bind("<Leave>", lambda e, t=theme: self.on_theme_leave(t))
            theme["label"].bind("<Button-1>", lambda e, t=theme: self.theme_selected(t))
            
            # Theme name and price
            theme_canvas.create_text(self.screen_width*theme["x"], y_position + self.theme_height//2 + 40, 
                                   text=f"{theme['name']} Theme\n₹{theme['price']:,}", 
                                   font=("Helvetica", 14, "bold"), 
                                   fill=self.TEXT_COLOR)
        
        # Back button
        back_btn = tk.Button(self.theme_window, text="Back", command=self.theme_window.destroy,
                           bg="#4a4a4a", fg=self.TEXT_COLOR, font=("Helvetica", 12, "bold"))
        back_btn.place(relx=0.5, rely=0.85, anchor="center", width=200, height=40)
    
    def on_theme_enter(self, theme):
        theme["label"].config(image=theme["zoomed"])
        theme["frame"].config(bg=self.HIGHLIGHT_COLOR)
    
    def on_theme_leave(self, theme):
        theme["label"].config(image=theme["image"])
        theme["frame"].config(bg=self.TEXT_COLOR)
    
    def load_theme_image(self, path, size):
        try:
            img = Image.open(path)
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            blank_img = Image.new('RGB', size, (200, 200, 200))
            return ImageTk.PhotoImage(blank_img)
    
    def load_zoomed_image(self, path, size, zoom_factor=1.1):
        try:
            img = Image.open(path)
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            new_size = (int(size[0]*zoom_factor), int(size[1]*zoom_factor))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading zoomed image {path}: {e}")
            blank_img = Image.new('RGB', (int(size[0]*zoom_factor), int(size[1]*zoom_factor)), (200, 200, 200))
            return ImageTk.PhotoImage(blank_img)
    
    def theme_selected(self, theme):
        self.selected_theme = theme
        self.theme_cost = theme["price"]
        self.theme_window.destroy()
        self.show_food_catalog(f"{theme['name']} Wedding", theme["price"])
    
    def show_food_catalog(self, event_name, event_price):
        self.food_window = tk.Toplevel(self.root)
        self.food_window.title(f"Food Catalog Selection - {event_name}")
        self.food_window.state('zoomed')
        
        # Create canvas
        food_canvas = tk.Canvas(self.food_window, highlightthickness=0)
        food_canvas.pack(fill="both", expand=True)
        bg_food_image = Image.open("background4.jpeg")
        bg_food_image = bg_food_image.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
        self.bg_food_photo = ImageTk.PhotoImage(bg_food_image)
        food_canvas.create_image(0, 0, image=self.bg_food_photo, anchor="nw")
        food_canvas.bg_image = self.bg_food_photo
        
        # Display event info at the top
        tk.Label(food_canvas, text=f"{event_name} - ₹{event_price:,}", 
                font=("Helvetica", 16, "bold"), 
                bg="#4a4a4a", fg=self.TEXT_COLOR).place(
                relx=0.5, rely=0.08, anchor="center")  # Moved slightly up
        
        # Food selection variable
        self.food_var = tk.StringVar(value="Elite")  # Default selection
        
        # Food options with enhanced styling and better description display
        food_options = [
            {"name": "Basic", "price": 500, "desc": """BASIC VEGETARIAN PACKAGE
    • Buffet-style traditional Indian meal
    • 2 Sabzis (Seasonal vegetable dishes)
    • 1 Dal (Lentil curry)
    • Steamed rice & 2 Roti varieties
    • Raita & Papad
    • Basic salad
    • 1 Sweet dish (e.g., Gulab Jamun or Kheer)
    • Buttermilk & Soft drinks"""},
            
            {"name": "Elite", "price": 1000, "desc": """ELITE VEGETARIAN PACKAGE
    • Premium buffet with live counters
    • 3 Gourmet sabzis (including Paneer specialty)
    • 2 Dal varieties (including Dal Makhani)
    • Jeera rice, Biryani, and 3 Roti varieties
    • 2 Raita varieties & Assorted papads
    • Fresh salad bar
    • 2 Sweet dishes (e.g., Rasmalai + Jalebi)
    • Fresh juices & Lassi
    • Chaats counter (Pani Puri/Bhel)"""},
            
            {"name": "Premium", "price": 2000, "desc": """PREMIUM VEGETARIAN PACKAGE
    • Royal thali dining experience
    • 5 Signature dishes (including Shahi Paneer & Malai Kofta)
    • 3 Dal varieties (including Dal Tadka & Dal Bukhara)
    • Speciality rice (Kashmiri Pulao + Lemon rice)
    • Tandoori roti, Naan, Paratha varieties
    • International salad bar with Indian dressings
    • Live dosa/chole bhature counter
    • 3 Premium desserts (e.g., Gajar ka Halwa + Rabri + Moong Dal Halwa)
    • Mocktails & Fresh coconut water
    • Paan service at end"""}
        ]
        
        # Create scrollable frame for food options - smaller and higher
        scroll_frame = tk.Frame(food_canvas, bg="#4a4a4a")
        scroll_frame.place(relx=0.5, rely=0.16, anchor="n", width=850, height=400)  # Adjusted size and position
        
        # Create a canvas inside the frame for scrolling
        inner_canvas = tk.Canvas(scroll_frame, bg="#4a4a4a", highlightthickness=0)
        inner_canvas.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=inner_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        inner_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create another frame inside the canvas for the food options
        options_frame = tk.Frame(inner_canvas, bg="#4a4a4a")
        inner_canvas.create_window((0, 0), window=options_frame, anchor="nw")
        
        # Function to update scroll region
        def _on_frame_configure(event=None):
            inner_canvas.configure(scrollregion=inner_canvas.bbox("all"))
        
        options_frame.bind("<Configure>", _on_frame_configure)
        
        # Create food option buttons with better styling and description layout
        for i, option in enumerate(food_options):
            frame = tk.Frame(options_frame, bg="#4a4a4a", bd=2, relief="ridge",
                            highlightbackground=self.TEXT_COLOR, highlightthickness=2)
            frame.pack(fill="x", padx=20, pady=10, ipady=10)
            
            # Left side - Radio button and price
            left_frame = tk.Frame(frame, bg="#4a4a4a")
            left_frame.pack(side="left", fill="y", padx=10)
            
            rb = tk.Radiobutton(
                left_frame,
                text=f"{option['name']}\n₹{option['price']}/person",
                font=("Helvetica", 14, "bold"),
                fg=self.TEXT_COLOR,
                bg="#4a4a4a",
                selectcolor="#333333",
                variable=self.food_var,
                value=option["name"],
                indicatoron=0,
                width=15,
                height=3,
                command=lambda o=option: self.food_selected(o)
            )
            rb.pack(pady=10)
            
            # Right side - Description
            right_frame = tk.Frame(frame, bg="#4a4a4a")
            right_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            desc_label = tk.Label(right_frame, 
                                text=option["desc"],
                                font=("Helvetica", 12),
                                fg="white",
                                bg="#4a4a4a",
                                justify="left",
                                anchor="w",
                                wraplength=500)  # Reduced wraplength to fit better
            desc_label.pack(fill="both", expand=True)
            
            # Hover effects
            frame.bind("<Enter>", lambda e, f=frame: f.config(bg="#5a5a5a"))
            frame.bind("<Leave>", lambda e, f=frame: f.config(bg="#4a4a4a"))
            rb.bind("<Enter>", lambda e, f=frame: f.config(bg="#5a5a5a"))
            rb.bind("<Leave>", lambda e, f=frame: f.config(bg="#4a4a4a"))
        
        # Number of people entry - moved further down
        tk.Label(food_canvas, text="Number of Guests:", font=("Helvetica", 14), 
                bg="#4a4a4a", fg=self.TEXT_COLOR).place(
                relx=0.5, rely=0.76, anchor="center")  # Moved down
        
        self.guest_var = tk.StringVar()
        guest_entry = tk.Entry(food_canvas, textvariable=self.guest_var, 
                            font=("Helvetica", 14), bd=2, relief="sunken")
        guest_entry.place(relx=0.5, rely=0.8, anchor="center", width=200, height=30)  # Moved down
        
        # Next button - moved further down
        next_btn = tk.Button(food_canvas, text="Calculate Total", command=lambda: self.calculate_total(event_price),
                        bg="#4a4a4a", fg=self.TEXT_COLOR, font=("Helvetica", 14, "bold"),
                        bd=2, relief="raised", activebackground="#5a5a5a")
        next_btn.place(relx=0.5, rely=0.9, anchor="center", width=250, height=50)  # Moved down
        
        # Hover effect for button
        next_btn.bind("<Enter>", lambda e: next_btn.config(bg="#5a5a5a"))
        next_btn.bind("<Leave>", lambda e: next_btn.config(bg="#4a4a4a"))
    def food_selected(self, option):
        self.selected_food = option["name"]
        self.food_cost = self.food_prices[option["name"]]
    
    def calculate_total(self, event_price):
        try:
            num_guests = int(self.guest_var.get())
            if num_guests <= 0:
                raise ValueError("Number of guests must be positive.")

        # Check selected food option
            food_name = self.food_var.get()
            if food_name not in self.food_prices:
                raise KeyError("Invalid food option selected.")

            self.food_cost = self.food_prices[food_name] * num_guests
            self.total_cost = event_price + self.food_cost
            self.selected_food = food_name
            self.num_guests = num_guests

            self.food_window.destroy()
            self.show_summary(event_price)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of guests")
        except KeyError:
            messagebox.showerror("Error", "Please select a valid food package")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred:\n{e}")

    
    def show_summary(self, event_price):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Booking Summary")
        summary_window.state('zoomed')

    # Create canvas
        summary_canvas = tk.Canvas(summary_window, highlightthickness=0)
        summary_canvas.pack(fill="both", expand=True)
        summary_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        summary_canvas.bg_image = self.bg_photo

    # Determine event type for display
        if hasattr(self, 'selected_theme') and self.selected_theme:
            event_type = f"{self.selected_theme.get('name', 'Custom')} Wedding"
        elif hasattr(self, 'selected_event') and self.selected_event:
            event_type = self.selected_event.get('name', 'Custom Event')
        else:
            event_type = "Unknown Event"

    # Protect against missing values
        food_name = getattr(self, 'selected_food', 'Unknown')
        guests = getattr(self, 'num_guests', 0)
        food_cost = getattr(self, 'food_cost', 0)
        total_cost = getattr(self, 'total_cost', 0)

    # Summary text
        summary_text = f"""
    Event Type: {event_type}
    Event Cost: ₹{event_price:,}

    Food Package: {food_name}
    Price per Person: ₹{self.food_prices[food_name]:,}
    Number of Guests: {guests}
    Food Cost: ₹{food_cost:,}

    TOTAL COST: ₹{total_cost:,}
    """

    # Create a summary frame
        summary_frame = tk.Frame(summary_canvas, bg="#4a4a4a", bd=3, relief="solid",
                             highlightbackground=self.TEXT_COLOR, highlightthickness=2)
        summary_frame.place(relx=0.5, rely=0.4, anchor="center", width=600, height=300)

        tk.Label(summary_frame, text="Booking Summary", font=("Helvetica", 18, "bold"),
             bg="#4a4a4a", fg=self.TEXT_COLOR).pack(pady=10)

        tk.Label(summary_frame, text=summary_text, font=("Helvetica", 14),
             bg="#4a4a4a", fg="white", justify="left").pack(pady=20, padx=20)

    # Book Now button
        book_btn = tk.Button(summary_window, text="Confirm Booking", 
                         bg="#4a4a4a", fg=self.TEXT_COLOR, 
                         font=("Helvetica", 16, "bold"),
                         bd=3, relief="raised", activebackground="#5a5a5a",
                         command=lambda: self.finalize_booking(event_type))
        book_btn.place(relx=0.5, rely=0.7, anchor="center", width=300, height=60)

    # Hover effect
        book_btn.bind("<Enter>", lambda e: book_btn.config(bg="#5a5a5a"))
        book_btn.bind("<Leave>", lambda e: book_btn.config(bg="#4a4a4a"))

    # Back button
        back_btn = tk.Button(summary_window, text="Back", 
                         command=summary_window.destroy,
                         bg="#4a4a4a", fg=self.TEXT_COLOR, 
                         font=("Helvetica", 14))
        back_btn.place(relx=0.5, rely=0.8, anchor="center", width=200, height=50)

    
    def finalize_booking(self, event_type):
        # Create a new window for the booking confirmation
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Booking Confirmation")
        confirm_window.geometry("600x400")
        confirm_window.resizable(False, False)
        
        # Set background color
        confirm_window.configure(bg="#f8f8f8")
        
        # Add a decorative header
        header_frame = tk.Frame(confirm_window, bg="#4a4a4a", height=80)
        header_frame.pack(fill="x")
        
        # Add a checkmark icon (using a label with text as a simple alternative)
        check_icon = tk.Label(header_frame, text="✓", font=("Helvetica", 40, "bold"), 
                            fg="#4CAF50", bg="#4a4a4a")
        check_icon.pack(pady=10)
        
        # Main content frame
        content_frame = tk.Frame(confirm_window, bg="#f8f8f8", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Confirmation message
        tk.Label(content_frame, 
                text="Your Booking is Confirmed!",
                font=("Helvetica", 18, "bold"),
                bg="#f8f8f8").pack(pady=(0, 10))
        
        # Booking details
        details_frame = tk.Frame(content_frame, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        details_frame.pack(fill="x", pady=10)
        
        tk.Label(details_frame, 
                text=f"Event Type: {event_type}",
                font=("Helvetica", 12),
                bg="#ffffff",
                anchor="w").pack(fill="x", pady=2)
        
        tk.Label(details_frame, 
                text=f"Food Package: {self.food_var.get()}",
                font=("Helvetica", 12),
                bg="#ffffff",
                anchor="w").pack(fill="x", pady=2)
        
        tk.Label(details_frame, 
                text=f"Total Cost: ₹{self.total_cost:,}",
                font=("Helvetica", 12, "bold"),
                bg="#ffffff",
                anchor="w").pack(fill="x", pady=2)
        
        # Thank you message
        tk.Label(content_frame, 
                text="Thank you for choosing our services!",
                font=("Helvetica", 12),
                bg="#f8f8f8").pack(pady=10)
        
        # Contact information
        tk.Label(content_frame, 
                text="Our team will contact you shortly for further details.",
                font=("Helvetica", 10),
                bg="#f8f8f8",
                fg="#555555").pack(pady=5)
        
        # Close button
        close_btn = tk.Button(content_frame, 
                            text="Close", 
                            command=lambda: [confirm_window.destroy(), self.root.destroy()],
                            bg="#4a4a4a", 
                            fg="white",
                            font=("Helvetica", 12),
                            width=15,
                            bd=0,
                            activebackground="#5a5a5a")
        close_btn.pack(pady=20)
        
        # Center the window
        confirm_window.update_idletasks()
        width = confirm_window.winfo_width()
        height = confirm_window.winfo_height()
        x = (confirm_window.winfo_screenwidth() // 2) - (width // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (height // 2)
        confirm_window.geometry(f"{width}x{height}+{x}+{y}")
# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeddingPlanner(root)
    root.mainloop()