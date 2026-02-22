[app]

# (str) Title of your application
title = Video Downloader

# (str) Package name
package.name = videodownloader

# (str) Package domain (reverse domain name style)
package.domain = org.fareed

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,kv,png,jpg,jpeg,ttf,mp4

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Version
version = 0.1

# (str) Application entry point
entrypoint = main.py

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (list) Android features
# android.features = android.hardware.touchscreen

# (list) Requirements
requirements = python3,kivy,kivymd,pillow,yt-dlp,requests

# (str) Orientation
orientation = portrait

# (str) Icon
icon.filename = %(source.dir)s/icon.png

# (str) Presplash
presplash.filename = %(source.dir)s/presplash.png


# -----------------------------
# ANDROID SPECIFIC
# -----------------------------

# (int) Android API to build against
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android SDK path
# android.sdk_path =

# (str) Android NDK path
# android.ndk_path =

# (str) NDK version
android.ndk = 25b

# (bool) Enable logcat
android.logcat = 1

# (bool) Use AndroidX
android.enable_androidx = True

# (bool) Enable gradle build
android.gradle_dependencies =

# (bool) Allow backup
android.allow_backup = True


# -----------------------------
# BUILD OPTIONS
# -----------------------------

# (bool) Copy libs instead of symlinking
copy_libs = 1

# (bool) Enable debug symbols
android.debug = 1

# (bool) Use color output
log_level = 2
