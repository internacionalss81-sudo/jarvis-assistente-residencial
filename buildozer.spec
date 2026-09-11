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

# (string) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions required by the app
android.permissions = INTERNET, RECORD_AUDIO

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (bool) Accept SDK licenses
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1