import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from yt_dlp import YoutubeDL

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MP3DownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MP3 Downloader - Modern Style")
        self.geometry("650x350")
        self.resizable(False, False)

        # Caminho padrão relativo à pasta do script
        self.base_folder = os.path.abspath(os.path.dirname(__file__))
        self.download_folder = os.path.join(self.base_folder, "downloads")
        os.makedirs(self.download_folder, exist_ok=True)

        self.urls = []
        self.url_source = tk.StringVar(value="paste")  # 'paste' or 'file'

        # Frame para escolher fonte dos URLs
        source_frame = ttk.LabelFrame(self, text="URL Source")
        source_frame.pack(padx=15, pady=10, fill=tk.X)

        ttk.Radiobutton(source_frame, text="Paste URLs", variable=self.url_source, value="paste", command=self.toggle_url_input).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Radiobutton(source_frame, text="Load from urls.txt", variable=self.url_source, value="file", command=self.toggle_url_input).pack(side=tk.LEFT, padx=10, pady=5)

        # Frame para URLs coladas
        self.paste_frame = ttk.Frame(self)
        self.paste_frame.pack(padx=15, fill=tk.BOTH, expand=True)

        ttk.Label(self.paste_frame, text="Paste YouTube URLs (one per line):").pack(anchor=tk.W, pady=5)
        self.url_text = tk.Text(self.paste_frame, height=8, font=("Segoe UI", 10))
        self.url_text.pack(fill=tk.BOTH, expand=True)

        # Frame para seleção de pasta
        folder_frame = ttk.Frame(self)
        folder_frame.pack(fill=tk.X, padx=15, pady=10)

        ttk.Label(folder_frame, text="Download Folder:").pack(side=tk.LEFT)
        self.folder_label = ttk.Label(folder_frame, text=self.download_folder, foreground="blue")
        self.folder_label.pack(side=tk.LEFT, padx=10)
        ttk.Button(folder_frame, text="Choose Folder", command=self.choose_folder).pack(side=tk.RIGHT)

        # Progress bar e status
        self.progress = ttk.Progressbar(self, length=580, mode='determinate')
        self.progress.pack(padx=15, pady=10)

        self.status_label = ttk.Label(self, text="", font=("Segoe UI", 9))
        self.status_label.pack(padx=15)

        # Download button
        self.download_button = ttk.Button(self, text="Start Download", command=self.start_download)
        self.download_button.pack(pady=10)

        self.toggle_url_input()

    def toggle_url_input(self):
        if self.url_source.get() == "paste":
            self.paste_frame.pack(padx=15, fill=tk.BOTH, expand=True)
        else:
            self.paste_frame.forget()

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=self.download_folder)

    def start_download(self):
        if self.url_source.get() == "paste":
            urls_raw = self.url_text.get("1.0", tk.END).strip()
            if not urls_raw:
                messagebox.showerror("Error", "Please paste at least one URL.")
                return
            self.urls = [line.strip() for line in urls_raw.splitlines() if line.strip()]
        else:
            txt_path = os.path.join(self.base_folder, "urls.txt")
            if not os.path.exists(txt_path):
                messagebox.showerror("Error", f"'urls.txt' not found in {self.base_folder}")
                return
            with open(txt_path, "r", encoding="utf-8") as f:
                self.urls = [line.strip() for line in f if line.strip()]
            if not self.urls:
                messagebox.showerror("Error", "'urls.txt' is empty.")
                return

        self.progress['maximum'] = len(self.urls)
        self.progress['value'] = 0
        self.status_label.config(text="Starting downloads...")

        self.download_button.config(state=tk.DISABLED)
        threading.Thread(target=self.download_all, daemon=True).start()

    def download_all(self):
        ffmpeg_path = resource_path("libs/ffmpeg/bin/ffmpeg.exe")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '256'},
                {'key': 'FFmpegMetadata'}
            ],
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            for idx, url in enumerate(self.urls, start=1):
                self.update_status(f"Downloading {idx} of {len(self.urls)}")
                try:
                    ydl.download([url])
                except Exception as e:
                    self.update_status(f"Error downloading: {url}\n{e}")
                self.progress['value'] = idx
        self.update_status("All downloads finished!")
        self.download_button.config(state=tk.NORMAL)

    def update_status(self, msg):
        def _update():
            self.status_label.config(text=msg)
        self.after(0, _update)

if __name__ == "__main__":
    app = MP3DownloaderApp()
    app.mainloop()
