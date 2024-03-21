import tkinter
import tkinter.messagebox
import customtkinter
import math
#from smbus2 import SMBus
import time

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

author = "Alset"
name = "Motor Control"
version = "1.1"


#addr = 0x10 # bus address
#bus = SMBus.SMBus(1)
#time.sleep(1)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title(author + " - " + name + "V" + version)
        self.geometry(f"{800}x{480}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=name, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar buttons
        self.close_button = customtkinter.CTkButton(self.sidebar_frame, command=self.close_button_event, text="Close", text_color="red")
        self.close_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create logBox
        self.logBox = customtkinter.CTkTextbox(self, width=250, corner_radius=8)
        self.logBox.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # Create PWM label
        self.speed_label= customtkinter.CTkLabel(self, text="Speed = 0%", width=100, height=20, corner_radius=8, fg_color=("white", "gray75"))
        self.speed_label.grid(row=2, column=3, padx=(10,20), pady=(10,10), sticky="ns")
        
        def slider_pwm_event(value):
            print(str(int(value)) + "%")
            #self.logBox.insert("5.0", "\nPWM signal set to " + str(int(value)) + "%")
            self.speed_label.configure(text = "Speed = " + str(math.floor(value)) + "%")
            color = "gray" + str(math.floor(int(value)))
            self.speed_label.configure(fg_color = str(color))
            # Write a byte to address 80, offset 0
            data = int(value).to
            bus.write_byte_data(addr, 0, data)


        # create slider and progressbar frame for the Speed control
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=0, column=4, rowspan=4, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(2, weight=1)

        self.speed_slider = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical", from_=0, to=100, number_of_steps=100, width=40, command=slider_pwm_event)
        self.speed_slider.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        
        #self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        #self.progressbar_2.grid(row=0, column=4, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")
        

        self.sidebar_button_3.configure(state="disabled", text="Disabled Button")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.logBox.insert("0.0", "Starting up " + name + " V" + version + "\nLoading...\nLoaded")
        self.speed_slider.set(0)

        #self.seg_button_1.configure(values=["Eco", "Normal", "Power"])
        #self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def close_button_event(self):
        print("Closing " + author + " - " + name + " V" + version)
        App.destroy(self)
        
if __name__ == "__main__":
    app = App()
    #app.wm_attributes('-fullscreen', True)
    app.mainloop()
