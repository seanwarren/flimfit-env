import json
import subprocess
import platform
import os

# Get vcpkg directory
vcpkg_dir = os.path.dirname(os.path.realpath(__file__))
vcpkg_dir = os.path.join(vcpkg_dir, "vcpkg", "")

# Get system and setup extension
system = platform.system()
if system == "Windows":
   script_ext = ".bat"
else:
   script_ext = ".sh"

# Bootstrap vcpkg
subprocess.run([vcpkg_dir + "bootstrap-vcpkg" + script_ext])

# Read configuration
json_file = open('config.json')
config = json.load(json_file)

# Setup ports
triplet_ext = ":" + config["default_triplet"][system]
ports = [port + triplet_ext for port in config["ports"]]

# Build ports
subprocess.run([vcpkg_dir + "vcpkg", "install"] + ports, 
   cwd=vcpkg_dir)

# Export
subprocess.run([vcpkg_dir + "vcpkg", "export"] + ports + ["--zip"],
   cwd=vcpkg_dir)
