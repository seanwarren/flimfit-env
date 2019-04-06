import json
import subprocess
import platform
import os
import re

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
json_file = open(os.path.join(env_dir, 'config.json'))
config = json.load(json_file)

# Setup ports
triplet_ext = ":" + config["default_triplet"][system]
ports = [port + triplet_ext for port in config["ports"]]

# Build ports
subprocess.run([vcpkg_dir + "vcpkg" + exec_ext, "install", "--clean-after-build"] + ports, 
   cwd=vcpkg_dir, check=True)

# Export ports
out = subprocess.run([vcpkg_dir + "vcpkg" + exec_ext, "export"] + ports + ["--zip"],
         cwd=vcpkg_dir, encoding="ascii", stdout=subprocess.PIPE)
print(out.stdout)

# Get name of exported file
m = re.search("Zip archive exported at: (.+)", out.stdout)
file = os.path.realpath(m.group(1))

# Create version name and rename file
git_ver = subprocess.check_output(["git", "describe", "--abbrev=7"], encoding="ascii").strip()
new_file = os.path.join(env_dir, "flimfit-env-" + git_ver + ".zip")
if os.path.exists(new_file):  
   os.remove(new_file)
os.rename(file, new_file)