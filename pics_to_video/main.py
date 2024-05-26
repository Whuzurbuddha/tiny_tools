import tkinter as tk
from tkinter import filedialog
from moviepy.editor import ImageSequenceClip

class VideoCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bild zu Video Konverter")

        self.image_paths = []

        # Drag & Drop Bereich
        self.drop_area = tk.Label(root, text="Bilder hinzufügen", relief="sunken", width=50, height=10)
        self.drop_area.pack(pady=10)
        self.drop_area.bind("<Button-1>", self.open_file_dialog)

        # Eingabefeld für die Zeit
        self.time_label = tk.Label(root, text="Gesamtdauer des Videos (Sekunden):")
        self.time_label.pack()
        self.time_entry = tk.Entry(root)
        self.time_entry.pack(pady=5)

        # Ausführungsbutton
        self.execute_button = tk.Button(root, text="Video erstellen", command=self.create_video)
        self.execute_button.pack(pady=10)

    def open_file_dialog(self, event):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self.image_paths.extend(file_paths)
        self.update_drop_area()

    def update_drop_area(self):
        display_text = "\n".join(self.image_paths)
        self.drop_area.config(text=display_text)

    def create_video(self):
        if not self.image_paths:
            tk.messagebox.showerror("Fehler", "Keine Bilder ausgewählt")
            return

        try:
            total_duration = float(self.time_entry.get())
        except ValueError:
            tk.messagebox.showerror("Fehler", "Ungültige Zeitangabe")
            return

        duration_per_image = total_duration / len(self.image_paths)

        clip = ImageSequenceClip(self.image_paths, durations=[duration_per_image] * len(self.image_paths))
        clip.write_videofile("output_video.mp4", fps=24)

        tk.messagebox.showinfo("Erfolg", "Video erfolgreich erstellt!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCreatorApp(root)
    root.mainloop()
