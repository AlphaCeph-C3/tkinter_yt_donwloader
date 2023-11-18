import tkinter as ttk
import customtkinter as ctk
from pytube import YouTube
from pytube.exceptions import RegexMatchError, AgeRestrictedError
import utils


def start_download():
    text = ttk.StringVar(value="")
    text_color = ttk.StringVar(value="#fff")
    try:
        yt_link = link_input.get()
        complete_label.configure(text="")
        progress_percentage.configure(text="0%", pady=10)
        progress_bar.configure(width=500, progress_color="#fff")
        app.update()
        yt_object = YouTube(
            yt_link, on_progress_callback=on_progress, on_complete_callback=on_complete
        )
        title.configure(
            text=yt_object.title, text_color="#fff", font=("FiraCode Nerd Font", 15)
        )
        video_file = yt_object.streams.filter(res="720p", progressive=True).first()
        if video_file is None:
            raise ValueError("No video found for the link")

        video_file.download()
    except (RegexMatchError, ValueError):
        text.set("Invalid Youtube Link")
        text_color.set("#ff0000")
    except AgeRestrictedError:
        text.set("Could not download the video. Age Restricted!")
        text_color.set("#ff0000")
    else:
        text.set("Download Completed!")
        text_color.set("#00ff00")
    finally:
        complete_label.configure(
            text=text.get(),
            text_color=text_color.get(),
            font=("FiraCode Nerd Font", 15),
            padx=20,
            pady=10,
        )


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_done = bytes_downloaded / total_size * 100
    percentage = int(percentage_done)
    progress_percentage.configure(text=f"{percentage}%")
    progress_percentage.update_idletasks()
    # making the bar move
    progress_bar.set(percentage_done / 100)
    progress_bar.update_idletasks()


def on_complete(stream, fpath):
    # utils.run_video_after_download(fpath)
    utils.run_the_video(fpath)


# System settings
# ctk.set_appearance_mode("system")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# App frame
app = ctk.CTk()
app.title("Youtube Video Downloader")
app.geometry("920x405")

# UI elements
title = ctk.CTkLabel(app, text="Insert a Youtube Link", font=("FiraCode Nerd Font", 25))
title.pack(padx=10, pady=30)

# link input
link_input = ctk.CTkEntry(app, width=460, height=40)
# link_input.focus()
link_input.pack()

# Progress bar
progress_percentage = ctk.CTkLabel(app, text="", font=("Aria", 20))
progress_percentage.pack()

progress_bar = ctk.CTkProgressBar(app, width=0)
progress_bar.set(0)
progress_bar.pack()

# Downloading complete
complete_label = ctk.CTkLabel(app, text="")
complete_label.pack()

# Download button for the app.
download_button = ctk.CTkButton(
    app,
    text="Download",
    width=300,
    height=40,
    command=start_download,
    font=("Times New Roman", 20),
)
download_button.pack(padx=20, pady=10)

# run it in loop
app.mainloop()
