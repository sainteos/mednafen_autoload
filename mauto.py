import os
import sys
import random
import re
from datetime import datetime, timedelta
import time
import subprocess

rom_files = []
working_directory = subprocess.check_output("cd", shell=True).strip()

print "Working Directory: " + working_directory
# #move cfg to .mednafen
subprocess.check_output("type nul > psx.cfg", shell=True)
subprocess.check_output("echo autosave 1 >> psx.cfg", shell=True)
subprocess.check_output("echo filesys.path_state " + working_directory + "\\save_states >> psx.cfg", shell=True)
subprocess.check_output("move psx.cfg D:\\Roms\\Mednafen", shell=True)
#subprocess.check_output("move psx.cfg " + home_directory + "\\.mednafen\\", shell=True)

if len(sys.argv) == 2:
  rom_folder = sys.argv[1]

  rom_files = filter(lambda file: re.match(r'.*\.(cue|ccd)$', file), os.listdir(rom_folder))
  m3u_files = filter(lambda file: re.match(r'.*\.(m3u)$', file), os.listdir(rom_folder))
  m3u_names = map(lambda file: file.split('.')[0], m3u_files)

  #True if the cue or ccd file has a matching m3u file
  def has_m3u(file):
    for name in m3u_names:
      if name in file:
        return True
    return False

  #Filter out roms that are multi disc (have m3u file)
  rom_files = filter(lambda file: not has_m3u(file), rom_files)
  #Add the m3u's to the possible roms
  rom_files = rom_files + m3u_files

  rom_files = map(lambda file: '\\' + rom_folder + file, rom_files)
elif len(sys.argv) == 3 and sys.argv[1] == "-d":
  rom_files = open(sys.argv[2], "w")

while 1:
  mednafen_process = subprocess.Popen(["mednafen", working_directory + random.choice(rom_files).strip()])
  start = datetime.now()
  #delta of 20 minutes between changes
  delta = timedelta(minutes=20)

  while datetime.now() - start <= delta:
    if mednafen_process.poll() is not None:
      break

  if mednafen_process.returncode is None:
    mednafen_process.kill()
