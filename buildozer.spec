[app]

title = Scanner

package.name = scanner

package.domain = ru.scanner

source.dir = .

source.include_exts = py,png,jpg,kv,json,ttf

version = 1.0.0

requirements = python3,kivy,setuptools,openpyxl

orientation = portrait

fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 33

android.minapi = 24

android.ndk = 25b

android.accept_sdk_license = True

android.archs = armeabi-v7a, arm64-v8a

android.ccache = 0

[buildozer]

log_level = 2

warn_on_root = 0