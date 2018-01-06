![picture alt](https://github.com/janyanti/TP_Anyanti/blob/master/assets/gamelogo.png?raw=true)

# 15-112 Term Project: Rhythm Rider
Rhythm Rider is an interactive music based game designed to produce an enjoyable experience while allowing a user to become more comfortable with musical notation and sight-reading. The project is designed to take MIDI Files as input and reproduce the music stored in the files with accurate musical representation. It is implemented with Python and makes use of the Pygame and Mido Python Libraries.

# Installation
Required Modules:
* Pygame
* Mido
* Rtmidi

Pygame can be installed by reading the instructions from the following [Link](https://www.pygame.org/wiki/GettingStarted#PygameInstallation "Link")

One can also install Pygame using Python's PIP install:
```
python3 -m pip install pygame --user
```

The mido and rtmidi libraries for python MIDI handeling can be installed using Pythons' PIP install:
```
pip install mido

pip install python-rtmidi
```
# Setup

After the successful installation of the required modules, all that is required to setup and run the game is to run the 'Main.py' file in the project folder. 
If one intends to use a MIDI input device for gameplay, it is required to have the device plugged in or active before running the program in order to assure that the program recognizes the device.
The Game is designed to work with a MIDI Keyboard or Virtual Input; However, the game will still run if a device is not present. This will only affect the piano mode of the game.

# Optimization

The game is designed to use MIDI Files as input to generate corresponding game levels, this means that experiences will vary depending on file selections. For optimal use, it is recommended to use MIDI files with one track. This will allow for a focus on musical content that a user can reasonably read and learn from the game with.

Resources such as [8notes](https://www.8notes.com/) and [MuseScore](https://musescore.com/dashboard) provide free access to MIDI files that can be used to play with the game.

For optimal performance in piano mode, it is advisable to use a MIDI input on a wired connection to reduce latency between key input and the game.







