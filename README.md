# Platform-Fighter

Instructions on how to export this game into an EXE file:

Download Python and the cx_Freeze module if you haven't

Open the setup.py file (be sure to place it outside the PlatformFighter folder when doing this)

Place a copy of the main file (Fighter.py) in the same folder as the setup.py file and rename it to whatever version it is

In the setup.py file, change the file name within the cx_Freeze.Executable function

Change the name and version inside the cx_Freeze.setup function

Open the Command Prompt within that folder

Run, in Command Prompt, python setup.py build, as commented in the setup.py file

The Build folder will be created, and inside is the exe file

Copy and place the rest of the files and folders (Stickman Character, MUSIC and STAGES folders; Character_Select, Controls, PlayerStickman and Start_Screen files)

Don't rename any of the folders or files except for the build folder, or you can move the PlatformFighter folder out of the build folder entierly
