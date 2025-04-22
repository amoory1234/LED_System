# Hand and Voice Controlled Arduino LED System

This project integrates hand gesture recognition and voice commands to control 4 LEDs connected to an Arduino board.

## Features
- **Hand Gesture Control**: Detects number of raised fingers to control specific LEDs.
- **Voice Command Support**: Recognizes Arabic and English keywords like "on", "off", "شغل", "اطفي", and number commands.
- **Arduino Communication**: Sends serial commands to Arduino based on the detected input.

## Python Script
```bash
python hand_voice_control.py
```

## Requirements
Install dependencies using:

```bash
pip install -r requirements.txt
```


## Notes
- Make sure your Arduino is connected to the correct COM port.
- Python must have access to the microphone.
