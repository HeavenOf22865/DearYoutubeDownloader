import os
import threading
import webbrowser
from time import sleep
from typing import Any, cast

import dearpygui.dearpygui as dpg
import yt_dlp


def download(url, quality, download_path):

    quality_map = {
        "360p": "bestvideo[height<=360]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "Best": "bestvideo+bestaudio/best",
    }

    selected_format = quality_map.get(quality, "best")

    output_template = os.path.join(download_path, "%(title)s.%(ext)s")

    settings = {
        "format": selected_format,
        "outtmpl": output_template,
        "nocheckcertificate": True,
    }

    try:
        with yt_dlp.YoutubeDL(cast(Any, settings)) as ydl:
            ydl.download([url])

        dpg.set_value("status", "Succesfully downloaded")

        sleep(3)

        dpg.set_value("status", "Ready")

    except Exception as e:
        dpg.set_value("status", f"Error: {str(e)[27:]}")


def start_download():
    url = dpg.get_value("url_input")
    quality = dpg.get_value("quality_combo")
    download_path = dpg.get_value("download_path")

    if url:
        dpg.set_value("status", "Downloading...")

        thread = threading.Thread(
            target=download, args=(url, quality, download_path), daemon=True
        )
        thread.start()

    else:
        dpg.set_value("status", "Error: URL is empty")


def get_ffmpeg():
    webbrowser.open("https://www.gyan.dev/ffmpeg/builds/#release-builds")


def main():
    dpg.create_context()

    dpg.create_viewport(title="DearYoutubeDownloader", width=600, height=600)

    with dpg.window(
        label="Downloader",
        width=600,
        height=600,
        no_resize=True,
        no_close=True,
        no_move=True,
        no_collapse=True,
    ):
        dpg.add_input_text(hint="Paste URL here", tag="url_input")
        dpg.add_input_text(
            hint="Download path (App dir by default)", tag="download_path"
        )
        dpg.add_combo(
            items=["360p", "480p", "720p", "1080p", "Best"],
            label="Quality",
            default_value="720p",
            tag="quality_combo",
        )
        dpg.add_button(label="Download", callback=lambda: start_download())
        dpg.add_text(default_value="!!! App requires FFmpeg !!!")
        dpg.add_button(label="Get FFmpeg", callback=get_ffmpeg)
        dpg.add_text("Ready", tag="status")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
