[app]

# (str) Title of your application
title = Jarvis Assistente Residencial

# (str) Package name
package.name = jarvisassistente

# (str) Package domain (needed for android packaging)
package.domain = org.jarvis

# (str) Source directory where the main.py file is located
source.dir = .

# (list) Source files to include (let it blank to include all files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Source files to exclude (let it blank to exclude none)
source.exclude_exts = spec

# (list) List of directory to exclude (let it blank to exclude none)
source.exclude_dirs = tests, bin, venv, .git, .github

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,opencv-python,ffpyplayer

# (str) Supported orientations (portrait, landscape or all)
orientation = portrait

# (list) The Android specific permissions
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android build tools version to use (Forçado para evitar o erro da versão 37)
android.build_tools_version = 33.0.0

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
