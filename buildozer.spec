[app]

# Application metadata
title = Scanner
package.name = scanner
package.domain = ru.scanner
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,ttf
version = 1.0.0

# Imports found in the repository:
#2
# Kivy UI/runtime plus openpyxl and its pure-Python XML dependency.
requirements = python3,kivy==2.3.0,openpyxl==3.1.5,et_xmlfile==2.0.0

orientation = portrait
fullscreen = 0

# The app writes Mark_fail.xlsx in its application-writable home directory.
# These permissions also support the existing Android file chooser behavior.
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android 12 is API 31. API 24 keeps the existing broad device compatibility.
android.api = 31
android.minapi = 24
android.ndk = 25b
android.archs = armeabi-v7a,arm64-v8a

# SDL2 is the Kivy bootstrap. Pin p4a to a known release rather than a
# moving develop/master branch.
p4a.bootstrap = sdl2
p4a.branch = v2024.01.21

android.accept_sdk_license = True
android.ccache = 0

[buildozer]
log_level = 2
warn_on_root = 0