[app]

# (str) Title of your application
title = Casa Inteligente

# (str) Package name
package.name = casainteligente

# (str) Package domain (needed for android packaging)
package.domain = org.casa

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# pyjnius e adicionado para permitir a comunicacao com a API de voz nativa do Android
requirements = python3,kivy,pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Adicionada a permissao RECORD_AUDIO para o recurso de voz funcionar
android.permissions = INTERNET, RECORD_AUDIO

# ========================================================
# CONFIGURACOES DO SDK/NDK (EVITA ERROS NO GITHUB ACTIONS)
# ========================================================

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use (Evita o erro do sdkmanager/r28c)
android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_path =

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1