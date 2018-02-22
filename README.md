# Smile Detector with Sense HAT
A simple face and smile detector for Raspberry Pi and Sense HAT.

## Requirements

- Raspberry Pi
- Sense HAT
- Raspbian Stretch
- Python 3
- OpenCV 3.4.0

## Installation

### Build OpenCV for Raspberry Pi

```sh
# Install prerequisites
sudo apt install cmake
sudo apt install gfortran
sudo apt install libgtk2.0-dev libgtk-3-dev
sudo apt install libtbb2 libtbb-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev
sudo apt install libjpeg-dev libpng-dev libtiff-dev libjasper-dev
# Extra packages from https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
sudo apt install libv4l-dev libavresample-dev libatlas-base-dev liblapacke-dev

# Download and extract OpenCV 3.4.0
wget https://github.com/opencv/opencv/archive/3.4.0.tar.gz -O opencv-3.4.0.tar.gz
wget https://github.com/opencv/opencv_contrib/archive/3.4.0.tar.gz -O opencv_contrib-3.4.0.tar.gz
tar zxvf opencv-3.4.0.tar.gz
tar zxvf opencv_contrib-3.4.0.tar.gz

# Building OpenCV
mkdir opencv-3.4.0/build
cd opencv-3.4.0/build
cmake -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.0/modules \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_TESTS=OFF
sudo make install

# Fix Python 3 module name
cd /usr/local/lib/python3.5/dist-packages
sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
```

You can test the OpenCV installation by running in Python:

```python
>>> import cv2
>>> cv2.__version__
'3.4.0'
```

## Testing Smile Detector

Clone the codes, connect the webcam and try running the smile detector in debug mode. I used a Logitech QuickCam Pro 9000. You may use the Raspberry Pi camera or any camera from [this list](https://elinux.org/RPi_USB_Webcams).

X is required to show the debug camera window. If the camera window does not open or freezes up, press Ctrl+C or the Sense HAT stick to terminate the program.

```sh
git clone https://github.com/mwyau/python-opencv-smile-detector.git smiledetector
cd smiledetector

# Get cascade data files
wget https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_alt.xml
wget https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_smile.xml

./smiledetector.py --debug
```

## Install as System Service (Optional)

If it runs okay, you can install it as a systemd service:

```sh
sudo cp smiledetector.service /lib/systemd/system/

# Test running as system service
sudo systemctl start smiledetector
sudo systemctl status smiledetector

# Enable at startup
sudo systemctl enable smiledetector
```

## Copyright

- [MIT License](LICENSE)
