import tkinter as tk
from tkinter import scrolledtext
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def url_to_normal(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    v = qs.get('v')
    if not v:
        return url
    new_query = urlencode({'v': v[0]})
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    return new_url

def convert_urls():
    input_text = input_box.get("1.0", tk.END).strip()
    urls = input_text.splitlines()
    output_box.delete("1.0", tk.END)
    
    for url in urls:
        if url.strip():
            normal_url = url_to_normal(url.strip())
            output_box.insert(tk.END, normal_url + "\n")

# Create main window
root = tk.Tk()
root.title("YouTube Playlist URL Converter")

# Input label and text box
tk.Label(root, text="Paste YouTube playlist URLs (one per line):").pack(padx=10, pady=5)
input_box = scrolledtext.ScrolledText(root, width=60, height=10)
input_box.pack(padx=10, pady=5)

# Convert button
convert_btn = tk.Button(root, text="Convert to normal URLs", command=convert_urls)
convert_btn.pack(pady=10)

# Output label and text box
tk.Label(root, text="Converted URLs:").pack(padx=10, pady=5)
output_box = scrolledtext.ScrolledText(root, width=60, height=10)
output_box.pack(padx=10, pady=5)

root.mainloop()
