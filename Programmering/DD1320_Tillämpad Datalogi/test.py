import tkinter as tk

root = tk.Tk()
root.title("test")
root.geometry("300x150")

label = tk.Label(root, text="Hej världen!", font=("Arial", 16))
label.pack(pady=30)

root.update_idletasks()  # Viktigt på macOS
root.update()            # Tvingar fönstret att ritas

root.mainloop()
