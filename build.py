import json
import subprocess
import platform
import os
import re
import shutil

# Get vcpkg directory
env_dir = os.path.dirname(os.path.realpath(__file__))
vcpkg_dir = os.path.join(env_dir, "vcpkg", "")

# Get system and setup extension
system = platform.system()
if system == "Windows":
   script_ext = ".bat"
   exec_ext = ".exe"
else:
   script_ext = ".sh"
   exec_ext = ""

# Bootstrap vcpkg
subprocess.run([vcpkg_dir + "bootstrap-vcpkg" + script_ext], check=True)

# Read configuration
json_file = open(os.path.join(env_dir, "config.json"))
config = json.load(json_file)

# Setup ports
triplet_ext = ":" + config["default_triplet"][system]
ports = [port + triplet_ext for port in config["ports"]]

# Build ports
subprocess.run([vcpkg_dir + "vcpkg" + exec_ext, "install", "--clean-after-build"] + ports, 
   cwd=vcpkg_dir, check=True)

# Delete tools directory
shutil.rmtree(os.path.join(vcpkg_dir, "downloads"))