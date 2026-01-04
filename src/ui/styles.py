from tkinter import ttk

def apply_styles():
    style = ttk.Style()

    # Define colors
    black = "#000000"
    green = "#00FF00" # Neon Green

    # Configure styles
    style.configure("TFrame", background=black)
    style.configure("TLabel", background=black, foreground=green, font=("Courier New", 12))
    
    # General Button Style
    style.configure("TButton", 
                    background=black, 
                    foreground=green, 
                    font=("Courier New", 12, "bold"),
                    padding=(10, 5),
                    relief="flat",
                    highlightthickness=2,
                    highlightbackground=green
                    )
    style.map("TButton",
              background=[("active", green)],
              foreground=[("active", black)])

    # Accent Button Style for main menu (reversed)
    style.configure("Accent.TButton", 
                    font=("Courier New", 16, "bold"),
                    padding=(15, 10),
                    background=black,
                    foreground=green,
                    highlightthickness=2,
                    highlightbackground=green
                    )
    style.map("Accent.TButton",
              background=[("active", green)],
              foreground=[("active", black)])
    
    style.configure("TEntry", 
                    fieldbackground=black, 
                    foreground=green, 
                    insertbackground=green,
                    borderwidth=1,
                    relief="solid")
    
    style.configure("TProgressbar", troughcolor=black, background=green)
