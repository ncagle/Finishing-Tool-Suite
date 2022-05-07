import arcpy
from arcpy import AddMessage as write
import webbrowser
import winsound
import subprocess
import time
import os
import signal
import sys


#----------------------------------------------------------------------


def get_pid(name):
	return int(subprocess.check_output(["pidof","-s",name]))

def kill_subprocess(name):
	pid_raw = subprocess.Popen("C:\Program Files (x86)\Windows Media Player\wmplayer.exe", shell=False).pid
	write(pid_raw)

def kill_process(name):
	#name = 'wmplayer'
	try:
		# iterating through each instance of the process
		for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
			fields = line.split()
			# extracting Process ID from the output
			pid = fields[0]
			# terminating process
			os.kill(int(pid), signal.SIGKILL)
		print("Process Successfully terminated")
	except:
		write("Error Encountered while running script")


### Works, but just opens it in a browser
#webbrowser.open("https://www.youtube.com/embed/Pz1a9MM-Vn4?autoplay=1&controls=0&showinfo=0&autohide=1", new=0, autoraise=True)


#----------------------------------------------------------------------


#winsound.MessageBeep(1)
# 'SystemAsterisk'  :  Asterisk
# 'SystemExclamation'  :  Exclamation
# 'SystemExit'  :  Exit Windows
# 'SystemHand'  :  Critical Stop
# 'SystemQuestion'  :  Question
# winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
# winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)


#----------------------------------------------------------------------


## Example of batch script creating temp vbs script to create custom desktop shortcut
# set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
#
# echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
# echo sLinkFile = "%USERPROFILE%\Desktop\GAIT 27 Archangel.lnk" >> %SCRIPT%
# echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
# echo oLink.TargetPath = "%appdata%\GAIT-WINDOWS-27\start_gait.bat" >> %SCRIPT%
# echo oLink.IconLocation = "%appdata%\GAIT-WINDOWS-27\GAIT_logo.ico" >> %SCRIPT%
# echo oLink.Save >> %SCRIPT%
#
# cscript /nologo %SCRIPT%
# del %SCRIPT%


#----------------------------------------------------------------------


# os.system('set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"')
# os.system('echo CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False >> %SCRIPT%')
# os.system('cscript /nologo %SCRIPT%')
# os.system('del %SCRIPT%')
#
# set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
# echo CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False >> %SCRIPT%
# cscript /nologo %SCRIPT%
# del %SCRIPT%


# vbs_cmd = '''
# set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
# echo CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False >> %SCRIPT%
# cscript /nologo %SCRIPT%
# del %SCRIPT%
# '''
# write(vbs_cmd)
#
#os.system(vbs_cmd)
#subprocess.check_output(vbs_cmd, shell=True)
#subprocess.call(vbs_cmd)


# subprocess.call((
#     'set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"',
#     'echo CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False >> %SCRIPT%',
#     'cscript /nologo %SCRIPT%',
# 	'del %SCRIPT%',
#     ), shell=True)


#----------------------------------------------------------------------


### VBS script
# CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\'WANGAN RUN' _ Best of Synthwave And Retro Electro Music Mix.mp3""", 0, False


### Technically works, but opens window and killing process abruptly changes window focus
# proc = subprocess.Popen([r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe", r"C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3"], shell=False)
# write(proc.pid)
# time.sleep(7)
# proc.kill()


### Works, but relies on external, existing vbs script  # Close with os.system("taskkill /im wmplayer.exe /t /f")
#subprocess.call(r"cscript C:\Projects\njcagle\R&D\7_Scripts\Projects\Finishing-Tool-Suite\finishing_tool_v9_8\background_music.vbs") # Or "cmd /c codename.vbs"


#----------------------------------------------------------------------


# import subprocess
# import time
# import os

write("\n\nConstructing background music VBS script")
with open('tmp.vbs', 'w') as vbs_script:
	vbs_script.write(r'CreateObject("Wscript.Shell").Run "wmplayer /play /close ""C:\Users\njcagle\Downloads\WANGAN_RUN_Synthwave_Mix.mp3""", 0, False')

write("Running script to call invisible WMP window")
subprocess.call('cscript tmp.vbs')
if os.path.exists('tmp.vbs'):
	os.remove('tmp.vbs')

write("\nWaiting 10 seconds...\n")
time.sleep(10)
write("Killing background music process\n\n")
os.system("taskkill /im wmplayer.exe /t /f")


#----------------------------------------------------------------------


#kill_process('wmplayer')


#winsound.PlaySound(None, winsound.SND_ASYNC)


# p = process.ProcessOpen("C:\Program Files (x86)\Windows Media Player\wmplayer")
# p.kill()
# "C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
