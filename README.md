# What does this do?
Alarming is an alarm clock that uses the Google Calendar API to see upcoming events on one's calendar. It views the next event on the calendar and sets an alarm based on the time of that event, ensuring that the user will always have plenty of time to wake up and get ready for the event. Like any other alarm clock, Alarming also displays the current time, with the added feature of displaying the name of the upcoming event when an alarm goes off.

### How we built it
The script to access the Google Calendar API is written in Python and is run on a Raspberry Pi. The Raspberry Pi communicates date, time, and alarm data over a serial port with an Arduino Uno, which uses the data to display the time on an LCD screen and set off the alarm.

### Video
https://youtu.be/VmHLxUnLlj8

### Devpost (Submitted to Boilermake IV)
https://devpost.com/software/alarming

Winner of Make School's Best Beginner Hack
