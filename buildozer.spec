[app]

title = Scanner

package.name = scanner

package.domain = ru.scanner

source.dir = .

source.include_exts = py,kv,png,jpg,jpeg,json,ttf,txt,xlsx

source.exclude_dirs = .git,.buildozer,bin,venv,__pycache__,.idea

version = 1.0.0

requirements = python3,kivy,setuptools,openpyxl

orientation = portrait

fullscreen = 0


# Android

android.api = 33

android.minapi = 24

android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.ccache = 0


[buildozer]

log_level = 2

warn_on_root = 1

#