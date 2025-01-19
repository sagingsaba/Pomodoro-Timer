import tkinter as tk
import math
import winsound

class ModernPomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro")
        # Make the window resizable
        self.root.geometry("340x600")
        
        # Modern color palette
        self.colors = {
            'bg': "#1A1A2E",  # Dark blue background
            'primary': "#16213E",  # Darker blue for containers
            'accent': "#0F3460",   # Medium blue for buttons
            'highlight': "#E94560", # Vibrant red for highlights
            'text_primary': "#FFFFFF",  # White text
            'text_secondary': "#A9A9A9",  # Gray text
            'success': "#4CAF50",  # Green for success states
            'warning': "#FFA726",  # Orange for breaks
            'info': "#29B6F6",     # Light blue for long breaks
            'button_hover': "#FF6B8B"  # Hover color for buttons
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Initialize variables
        self.work_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.current_time = self.work_time
        self.max_time = self.work_time
        self.is_running = False
        self.session_count = 0
        self.sound_enabled = True
        self.current_mode = "FOCUS SESSION"
        
        self.create_title_bar()
        self.create_widgets()
        
        # Set the window to fullscreen
        self.center_window()
        self.root.mainloop()

    def center_window(self):
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to full screen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes('-fullscreen', False)  # Set window to fullscreen mode
        

    def create_title_bar(self):
        title_bar = tk.Frame(self.root, bg=self.colors['primary'], height=40)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        # App icon with enhanced padding
        icon_label = tk.Label(title_bar, text="🍅", bg=self.colors['primary'],
                            fg=self.colors['highlight'],
                            font=("Helvetica", 18))
        icon_label.pack(side=tk.LEFT, padx=12)
        
        # Title with modern font
        title_label = tk.Label(title_bar, text="POMODORO", bg=self.colors['primary'],
                             fg=self.colors['text_primary'],
                             font=("Helvetica", 12, "bold"))
        title_label.pack(side=tk.LEFT, padx=8)

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Progress circle
        self.canvas = tk.Canvas(main_frame, width=260, height=260,
                              bg=self.colors['bg'], highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Timer display
        timer_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        timer_frame.pack(pady=10)
        
        self.time_label = tk.Label(timer_frame,
                                 text=self.format_time(self.current_time),
                                 font=("Helvetica", 48, "bold"),
                                 bg=self.colors['bg'],
                                 fg=self.colors['highlight'])
        self.time_label.pack()
        
        self.session_label = tk.Label(timer_frame, text=self.current_mode,
                                    font=("Helvetica", 14),
                                    bg=self.colors['bg'],
                                    fg=self.colors['text_secondary'])
        self.session_label.pack()
        
        self.create_counter_section(main_frame)
        self.create_control_buttons(main_frame)
        self.create_mode_buttons(main_frame)
        self.draw_progress_circle()

    def create_control_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        # New modern button style
        def create_hover_button(frame, text, command, is_primary=True):
            btn = tk.Button(frame, text=text,
                          font=("Helvetica", 13, "bold"),
                          width=10,
                          height=1,
                          bd=0,
                          relief="flat",
                          cursor="hand2")
            
            if is_primary:
                btn.config(
                    bg=self.colors['highlight'],
                    fg=self.colors['text_primary'],
                    activebackground=self.colors['button_hover'],
                    activeforeground=self.colors['text_primary']
                )
            else:
                btn.config(
                    bg=self.colors['accent'],
                    fg=self.colors['text_primary'],
                    activebackground=self.colors['primary'],
                    activeforeground=self.colors['text_primary']
                )
            
            # Round corners effect
            btn.config(pady=8)
            
            # Hover effects
            btn.bind("<Enter>", 
                    lambda e, b=btn: b.config(bg=self.colors['button_hover'] if is_primary 
                                            else self.colors['primary']))
            btn.bind("<Leave>", 
                    lambda e, b=btn: b.config(bg=self.colors['highlight'] if is_primary 
                                            else self.colors['accent']))
            
            btn.config(command=command)
            return btn
        
        # Create main control buttons with new style
        self.start_button = create_hover_button(button_frame, "START", self.toggle_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = create_hover_button(button_frame, "PAUSE", self.toggle_timer, False)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = create_hover_button(button_frame, "RESET", self.reset_timer, False)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def create_mode_buttons(self, parent):
        mode_frame = tk.Frame(parent, bg=self.colors['bg'])
        mode_frame.pack(pady=10)
        
        modes = [
            ("Focus", self.work_time, self.colors['highlight']),
            ("Short", self.short_break, self.colors['warning']),
            ("Long", self.long_break, self.colors['info'])
        ]
        
        for text, time, color in modes:
            btn = tk.Button(mode_frame, text=text,
                          font=("Helvetica", 11),
                          bg=self.colors['primary'],
                          fg=color,
                          bd=0,
                          padx=12,
                          pady=6,
                          cursor="hand2",
                          command=lambda t=time, txt=text: self.change_mode(t, txt))
            
            # Hover effects for mode buttons
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['accent']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['primary']))
            
            btn.pack(side=tk.LEFT, padx=6)

    def create_counter_section(self, parent):
        counter_frame = tk.Frame(parent, bg=self.colors['bg'])
        counter_frame.pack(pady=15)
        
        counters = [
            ("FOCUS", "🎯", self.colors['highlight']),
            ("SHORT", "☕", self.colors['warning']),
            ("LONG", "🌟", self.colors['info'])
        ]
        
        self.counter_labels = {}
        for name, icon, color in counters:
            frame = tk.Frame(counter_frame, bg=self.colors['bg'])
            frame.pack(side=tk.LEFT, padx=15)
            
            count_label = tk.Label(frame, text="0",
                                 font=("Helvetica", 22, "bold"),
                                 bg=self.colors['bg'], fg=color)
            count_label.pack()
            
            tk.Label(frame, text=f"{icon} {name}",
                    font=("Helvetica", 9),
                    bg=self.colors['bg'],
                    fg=self.colors['text_secondary']).pack()
            
            self.counter_labels[name] = count_label

    def draw_progress_circle(self):
        self.canvas.delete("all")
        # Draw background circle
        self.canvas.create_oval(10, 10, 250, 250,
                              width=8,
                              outline=self.colors['primary'])
        
        if self.current_time > 0:
            progress = self.current_time / self.max_time
            angle = 360 * progress
            
            rad = math.radians(angle - 90)
            x = 130 + 120 * math.cos(rad)
            y = 130 + 120 * math.sin(rad)
            
            if angle > 0:
                self.canvas.create_arc(10, 10, 250, 250,
                                     start=-90,
                                     extent=angle,
                                     width=8,
                                     outline=self.colors['highlight'])

    def update_timer(self):
        if self.is_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.time_label.config(text=self.format_time(self.current_time))
                self.draw_progress_circle()
                
                if self.current_time == 0:
                    self.play_sound()
                    self.session_completed()
                
                self.root.after(1000, self.update_timer)
            else:
                self.session_completed()

    def session_completed(self):
        self.session_count += 1
        current_mode = self.session_label.cget("text")
        
        if current_mode == "FOCUS SESSION":
            self.counter_labels["FOCUS"].config(
                text=str(int(self.counter_labels["FOCUS"].cget("text")) + 1))
            if self.session_count % 4 == 0:
                self.change_mode(self.long_break, "Long Break")
            else:
                self.change_mode(self.short_break, "Short Break")
        elif current_mode == "SHORT BREAK":
            self.counter_labels["SHORT"].config(
                text=str(int(self.counter_labels["SHORT"].cget("text")) + 1))
            self.change_mode(self.work_time, "Focus")
        else:
            self.counter_labels["LONG"].config(
                text=str(int(self.counter_labels["LONG"].cget("text")) + 1))
            self.change_mode(self.work_time, "Focus")
        
        if self.is_running:
            self.update_timer()

    def play_sound(self):
        if self.sound_enabled:
            try:
                winsound.Beep(1000, 500)
            except:
                pass

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.config(text="🔊" if self.sound_enabled else "🔇")

    def minimize_window(self):
        self.root.iconify()

    def change_mode(self, time_value, mode_name):
        self.current_time = time_value
        self.max_time = time_value
        self.session_label.config(text=f"{mode_name.upper()} SESSION")
        self.time_label.config(text=self.format_time(self.current_time))
        self.draw_progress_circle()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"

    def toggle_timer(self):
        self.is_running = not self.is_running
        self.start_button.config(text="PAUSE" if self.is_running else "START")
        if self.is_running:
            self.update_timer()

    def reset_timer(self):
        self.current_time = self.max_time
        self.time_label.config(text=self.format_time(self.current_time))
        self.draw_progress_circle()
        self.is_running = False
        self.start_button.config(text="START")

if __name__ == "__main__":
    ModernPomodoroTimer()
