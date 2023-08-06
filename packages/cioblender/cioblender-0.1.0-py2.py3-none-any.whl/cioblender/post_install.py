"""

"""
import os
import sys
import errno
from shutil import copy2

# /users/me/Conductor/cioblender
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = PKG_DIR
PKGNAME = os.path.basename(PKG_DIR)  # cioblender
MODULE_FILENAME = "conductor.mod"
PLATFORM = sys.platform
with open(os.path.join(PKG_DIR, "VERSION")) as version_file:
    VERSION = version_file.read().strip()
WIN_MY_DOCUMENTS = 5
WIN_TYPE_CURRENT = 0
SUPPORTED_BLENDER_VERSIONS = [2017, 2018, 2019, 2020, 2022]

def main():
    if not PLATFORM.startswith(("darwin", "win", "linux")):
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    # module_dir = get_blender_module_dir()
    # write_blender_mod_file(module_dir)
    sys.stdout.write("Completed Blender plugin setup!\n")


# def get_blender_module_dir():

#     app_dir = os.environ.get("BLENDER_APP_DIR")
#     if not app_dir:
#         if PLATFORM.startswith("darwin"):
#             app_dir = "~/Library/Preferences/Autodesk/blender"
#         elif PLATFORM.startswith("linux"):
#             app_dir = "~/blender"
#         else:  # windows
#             try:
#                 import ctypes.wintypes

#                 buff = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
#                 ctypes.windll.shell32.SHGetFolderPathW(
#                     None, WIN_MY_DOCUMENTS, None, WIN_TYPE_CURRENT, buff
#                 )
#                 documents = buff.value
#             except BaseException:
#                 sys.stderr.write(
#                     "Couldn't determine MyDocuments folder for the conductor.mod file.\n"
#                 )
#                 sys.stderr.write(
#                     "You may have to move it manually from the path below if that is not your where your Blender prefs and modules live.\n"
#                 )
#                 documents = "~\Documents"
#             app_dir = "{}\blender".format(documents)

#     return os.path.join(os.path.expanduser(app_dir), "modules")


# def write_blender_mod_file(module_dir):

#     ensure_directory(module_dir)
#     fn = os.path.join(module_dir, MODULE_FILENAME)
#     with open(fn, "w") as f:
#         for blender_version in SUPPORTED_BLENDER_VERSIONS:
#             f.write("+ BLENDERVERSION:{} conductor {} {}\n".format(blender_version, VERSION, MODULE_DIR))
#             f.write("PYTHONPATH+:=../\n\n")

#     sys.stdout.write("Wrote Blender module file: {}\n".format(fn))


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise


if __name__ == "__main__":
    main()
