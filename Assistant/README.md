# IOT Assignment 2
### Assistant
This Folder contains the files you need to replace after installing the google assistant on your pi. You do not run the assistant from this directory.
Assuming installation complete.

CD ~/AIY-projects-python/
<br>
source env/bin/activate
<br>
python src/Assistant.py
<br>

You'll be promted for the ip address of the api. If you are running this service on the same pi as api, just press enter, otherwise enter the ip of the pi with the api running on it.
### -------------------------------------------------------------
## Instructions from tutorial sheet
### Working with Google Assistant Library (on Raspberry Pi)
Google Assistant Library is a convenient subset of the Google Assistant Service, which takes
care of the audio input. As a result, certain features are omitted from this library, such as the
ability to type to the service and retrieve text responses from the Google Assistant APIs.
<br>
To work with the Library, you will need these extra components to be used alongside your
Raspberry Pi:
<br>
USB sound card (for audio input)
<br>
a 3.5mm jack microphone
<br>
<br>
There is a convenient install script from t1m0thyj to install the Google Assistant Library unto
your Raspberry Pi:
<br>
git clone https://github.com/t1m0thyj/AssistantPi/
<br>
<br>
### Enabling Google Assistant API service
Before you begin, make sure that your Google Assistant API is enabled:
<br>
https://console.cloud.google.com/apis/library/embeddedassistant.googleapis.com?q=assistant
<br>
You will create additional credentials on the next few pages.
<br>
### REGISTERING NEW DEVICE
<br>
You will need to generate a credentials.json similar to the way you created one for your Google
Calendar API. The full instructions are on:
<br>
https://developers.google.com/assistant/sdk/guides/library/python/embed/setup
<br>
But here's the minimal set up steps to take:
<br>
Go to: https://console.actions.google.com/
<br>
Create a project: IoT-Demo-ASG2
<br>
And choose SKIP for the categories
<br>
On the left side of the screen:
<br>
click on Device registration and click: REGISTER MODEL
<br>
Use the following details for your new model
<br>
Product Name: RMIT-IoT-Pi-01
<br>
Manufacture Name: Raspberry
<br>
Device type: Auto
<br>
Device Model id: iot-demo-asg2-rmit-iot-pi-01
<br>
Click: REGISTER MODEL
<br>
On the next page, click: Download OAuth 2.0 credentials
<br>
save the file as assistant.json and click Next
<br>
On the next page, click SKIP
<br>
<br>
Now, move the assistant.json to your Raspberry Pi's /home/pi folder. (Note: If you did not
renamed it, just move that file over to Raspberry Pi and renamed it as assistant.json)
<br>
<br>
Back on your Raspberry Pi
<br>
cd ~/AssistantPi
<br>
bash install.sh
<br>
<br>
You will be asked to authenticate via the now familiar oauth process via browser. Once
authenticated, you will realise that the Library does not pick up your installed audio. Create a
file to inform Google Assistant Library to use the external mic through the USB sound card and
3.5mm jack for your audio output. This 3.5mm jack may be your smartphone's earphones or a
speaker that may be lying around.
<br>
<br>
CTRL+C
<br>
nano .asoundrc
<br>
pcm.!default {
type asym
capture.pcm "mic"
playback.pcm "speaker"
}
pcm.mic {
type plug
slave {
pcm "hw:1,0"
}
}
pcm.speaker {
type plug
slave {
pcm "hw:0,0"
}
}
<br>
<br>
You can now test your new Google Assistant on your Raspberry Pi with
<br>
cd /home/pi/AIY-projects-python
<br>
source env/bin/activate
<br>
python3 src/AssitantPi.py
<br>
<br>
### Add modified AssistantPi.py
Using an ftp client like FILEZILLA, connect to your pi.
<br>
In the /home/pi/AIY-projects-python/src replace the AssistantPi.py file with the one from this project.
<br>
Also add requirements.txt
<br>
pip install -r requirements.txt
<br>
source env/bin/activate
<br>
python3 src/AssitantPi.py