# Eyecare- Optimise your Eye Health👀
Your solution to maintain optimal eye health while maximizing productivity📈 

Leading Medical Professionals recommend to look at an object 20 ft. away for 20 seconds, for every 20 minutes of work to prevent the effects of eye strain🧐. This App automates the process in the form of timely reminders⏱️
  
  Key Features:
*  Reminder to take breaks in the form of a System Notification🔔 
*  Users can also toggle light theme or dark theme using the 'theme' button⚫⚪
*  Users can adjust the time duration for work and break⌛ (will be added soon)

## Screenshots
App opened in Light Mode:  
<img src="/assets/Screenshot 2024-05-28 100102.png" alt="Image 1" width=40%>  
App opened in Dark Mode:  
<img src="/assets/Screenshot 2024-05-28 100045.png" alt="Image 2" width=40%>  
About Page:  
<img src="/assets/Screenshot 2024-05-28 100149.png" alt="Image 3" width=40%>  
Example of System Notification:  
<img src="assets/Screenshot 2024-05-28 100218.png" alt="Image 4" width=40%>  


## Download
Windows- [Download Now](https://github.com/Leetcodr/eyecare/releases/download/Second/eyecare.exe) (eyecare.exe)

Mac OS- will be available soon!
## Author
*  [Atharva Baradkar](https://www.linkedin.com/in/atharva-baradkar/) - Visit LinkedIn Profile
## Build Yourself
Pre-Requisites:
*  Python3
*  pip

Clone the Project:
```bash
git clone https://github.com/Leetcodr/eyecare
```
Install the Dependencies:
```bash
pip install -r requirements.txt
```
Build the App:
```bash
pyinstaller --noconfirm --onefile --windowed --icon "$ICON_PATH" --collect-data "sv_ttk" --hidden-import "pygame.mixer" --hidden-import "plyer.platforms.win.notification" --add-data "$SOUND_PATH;."  "$SCRIPT_PATH"
```
Replace:
*  Replace $ICON_PATH with Absoulte path of the 'glasses.ico' file
*  Replace $SOUND_PATH with Absoulte path of the 'sound.wav' file
*  Replace $SCRIPT_PATH with Absolute path of the 'eyecare.py' file
## Disclaimer
When installing our eye health app, it's important to note that while it is a tool for assistance, however currently it is not medically certified or recommended by health care professionals. This app serves as a general wellness tool and is not a replacement for professional eye care. Please use this app responsibly, understanding its limitations and intended purpose.
