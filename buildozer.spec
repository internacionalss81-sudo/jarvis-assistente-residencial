[app]

# (string) Title of your application
title = Casa Inteligente

# (string) Package name
package.name = casainteligente

# (string) Package domain (needed for android packaging)
package.domain = org.casa

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,*.png

# (string) Application versioning
version = 1.0.0

# (list) Application requirements (incluindo ffpyplayer para suporte a vídeo)
requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,ffpyplayer

# (str) Icon of the application
icon.filename = %(source.dir)s/icone.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions required by the app (incluindo rede e Wi-Fi para falar com o ESP32 e a câmera)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,RECORD_AUDIO

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK licenses
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enable Android logcat
android.logcat_filters = *:S python:D

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1