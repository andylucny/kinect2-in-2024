# kinect2-in-2024
Using Kinect 2.0 XBox One in year 2024

Installation instructions:

Download KinectRuntime-v2.2_1811.zip from https://download.microsoft.com/download/5/0/3/503F0020-B1F0-4DA6-A575-EA5C5B9EBF95/KinectRuntime-v2.2_1811.zip

Unpack somewhere, go to drivers\K4W\ 

By the right mouse button on the file kinectsensor.inf run Install

Download KinectSDK-v2.0_1409-Setup.exe from https://download.microsoft.com/download/F/2/D/F2D1012E-3BC6-49C5-B8B3-5ACFF58AF7B8/KinectSDK-v2.0_1409-Setup.exe

Install it.

Connect sensor the "blue" USB port

In c:\Program Files\Microsoft SDKs\Kinect\v2.0_1409\bin\ try to run e.g. BodyBasics-WPF.exe, it should work

pip install comtypes

patch e.g. c:\Python39\Lib\site-packages\comtypes\__init__.py according to patches\comtypes,
i.e., to avoid throwing exception when there is unknown version ''

pip install pykinect2

copy patches from patches\pykinect2\*.py to e.g. c:\Python39\Lib\site-packages\pykinect2

run e.g. python PyKinectBody.py and play
