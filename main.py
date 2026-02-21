
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button

from kivy.uix.label import Label
from kivy.clock import Clock
import yt_dlp
import threading
import os



from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivy.utils import get_color_from_hex
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager




def color(hex_code):
    return get_color_from_hex(hex_code)








DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
LAST_PATH_FILE = "last_path.txt"



class DownloaderUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.top_label = Label(
            text="Youtube/Insta Video Downloader", bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            font_size=22
            )

        self.link_input = MDTextField(
            hint_text="Paste YouTube / Instagram link here",
            helper_text="Youtube or Insta",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height=50,
            multiline=False,
            mode="rectangle"
        )

        self.fetch_btn = MDRaisedButton(
            text="Search for Quality Options",
            size_hint_y=None,
            height=45,
            md_bg_color= color("#C5FFFD"),
            text_color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5}
        )
        self.fetch_btn.bind(on_press=self.fetch_qualities)

        self.quality_btn = MDRaisedButton(
            text="Highest Quality",
            pos_hint={"center_x": 0.5}
        )
        self.quality_btn.bind(on_release=self.open_quality_menu)
        

        self.download_btn = MDRaisedButton(
            text="Download",
            size_hint_y=None,
            height=45,
            md_bg_color=(0.1, 0.6, 0.9, 1),
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5}
        )
        self.download_btn.bind(on_press=self.download_video)

        self.status_label = Label(text="")

        self.progress_bar = MDProgressBar(max=100, value=0)
        
        self.add_widget(self.top_label)
        self.add_widget(self.progress_bar)


        self.add_widget(self.link_input)
        
        self.add_widget(self.fetch_btn)
        self.add_widget(self.quality_btn)
        self.add_widget(self.download_btn)
        self.add_widget(self.status_label)

        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        self.download_path = os.getcwd()
        if os.path.exists(LAST_PATH_FILE):
            with open(LAST_PATH_FILE, "r") as f:
                self.download_path = f.read().strip()


        self.formats = {}

        self.file_manager = MDFileManager(
            select_path=self.on_folder_selected,
            exit_manager=self.close_file_manager,
            preview=False
        )

    def choose_download_folder(self):
        start_path = self.download_path if os.path.exists(self.download_path) else os.getcwd()
        self.file_manager.show(start_path)

    def on_folder_selected(self, path):
        self.download_path = path

        with open(LAST_PATH_FILE, "w") as f:
            f.write(path)

        self.close_file_manager()

        self.status_label.text = "Downloading..."
        threading.Thread(target=self._download_thread).start()

    def close_file_manager(self, *args):
        self.file_manager.close()


    def fetch_qualities(self, instance):
        self.status_label.text = "Fetching qualities..."
        threading.Thread(target=self._fetch_thread).start()

    def _fetch_thread(self):
        url = self.link_input.text.strip()
        self.formats.clear()

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'logger': None,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            quality_list = []

            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    label = f"{f.get('height', 'NA')}p - {f.get('ext')}"
                    self.formats[label] = f['format_id']
                    quality_list.append(label)

            quality_list = sorted(set(quality_list), reverse=True)

            Clock.schedule_once(
                lambda dt, q=quality_list: self.update_quality_options(q)
            )
    


        except Exception as e:
            err = str(e)
            Clock.schedule_once(lambda dt, msg=err: self.set_status(f"Error: {msg}"))

    def update_quality_options(self, quality_list):
        if not quality_list:
            self.status_label.text = "No qualities found"
            return

        self.quality_options = quality_list
        self.selected_quality = quality_list[0]

        self.quality_btn.text = self.selected_quality
        self.status_label.text = "Select quality"




    def download_video(self, instance):
        self.choose_download_folder()

    


    def _download_thread(self):
        url = self.link_input.text.strip()
        selected_quality = self.quality_btn.text
        download_dir = getattr(self, 'download_path', os.getcwd())

        ydl_opts = {
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'format': self.formats.get(selected_quality, 'best'),
            'quiet': True,
            'no_warnings': True,
            'logger': None,
            'progress_hooks': [self.progress_hook],
        }


        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.on_download_complete())

        except Exception as e:
            err = str(e)
            Clock.schedule_once(lambda dt, msg=err: self.set_status(f"Download failed ❌ {msg}"))

    def on_download_complete(self):
        self.set_status("Download completed ✅")
        self.progress_bar.value = 100
        self.show_download_complete_popup()



    def set_status(self, msg):
        self.status_label.text = msg

    

        # def on_submit(instance, selection, touch):
        #     if selection:
        #         self.download_path = selection[0]
        #         popup.dismiss()
        #         self.status_label.text = "Downloading..."
        #         threading.Thread(target=self._download_thread).start()

        #         with open(LAST_PATH_FILE, "w") as f:
        #             f.write(self.download_path)

        # chooser.bind(on_submit=on_submit)
        # popup.open()


    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded * 100 / total)
                Clock.schedule_once(lambda dt, p=percent: self.update_progress(p))

        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_progress(100))

    def update_progress(self, value):
        self.progress_bar.value = value


    def request_android_permissions(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

    def show_download_complete_popup(self):
        if hasattr(self, "success_dialog"):
            self.success_dialog.dismiss()

        self.success_dialog = MDDialog(
            title="Success",
            text="✅ Download completed successfully!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.success_dialog.dismiss()
                )
            ]
        )
        self.success_dialog.open()


    def open_quality_menu(self, button):
        menu_items = [
            {
                "text": q,
                "on_release": lambda x=q: self.set_quality(x),
            }
            for q in self.quality_options
        ]

        self.menu = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def set_quality(self, quality):
        self.selected_quality = quality
        self.quality_btn.text = quality
        self.menu.dismiss()

    
        






class VideoDownloaderApp(MDApp):
    def build(self):
        ui = DownloaderUI()
        ui.request_android_permissions()
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return ui


if __name__ == "__main__":
    VideoDownloaderApp().run()
