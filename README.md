![kép](https://github.com/ThomAce/OnnxStreamGui/assets/34764511/c59dee8a-cfa5-4928-afd2-b0c343e7f1f5)

# OnnxStreamGui
An Efficient Graphical User Interface (GUI) for OnnxStream: Designed with simplicity and user-friendliness in mind, this interface ensures smooth and intuitive navigation. Tailored to cater to a wide range of computing platforms, it is especially optimized for performance on devices like the Raspberry Pi. The purpose behind this design is to harness the minimal memory consumption capabilities of OnnxStream, making it accessible and effective for users across different hardware and software environments.

# What is OnnxStream?
OnnxStream is an efficient project designed for stable diffusion with minimal memory consumption. It performs exceptionally well on a variety of computers, but is especially optimized for the Raspberry Pi.

# OnnxStream Github repo:
[https://github.com/vitoplantamura/OnnxStream](https://github.com/vitoplantamura/OnnxStream)

# OnnxStream+ Github repo: (fork of OnnxStream with capability of custom seed, fine tuning & re-generating your image, and logging.)
https://github.com/ThomAce/OnnxStream

# Current stage:
PRE-ALPHA

# Available packages:
- Webpage
- Desktop GUI

# Pre requisites:

- SD1.5 weights: https://github.com/vitoplantamura/OnnxStream/releases/tag/v0.1
- SDXL1.0 weights:
```
git lfs install
git clone --depth=1 https://huggingface.co/vitoplantamura/stable-diffusion-xl-base-1.0-onnxstream
```

# Web Requirements:
WARNING! - The web based version only tested on RaspberryPi 4!
- Apache2
- PHP5+ (PHP7 preferred)

# Desktop GUI Requirements:
- Python3+
  - Go to https://www.python.org/downloads/
  - Select, download and install Python according to your OS
- Guizero
  - Go to https://lawsie.github.io/guizero/#installation for details or:
  - Run the command in cmd: pip install guizero
- Guizero images
  - Run the command in cmd: pip3 install guizero[images]
- PIL (aka Pillow)
  - Run the command in cmd: pip install pillow

You are ready to start the application based on your system preferences. You can choose either sdgui.sh or sdgui.bat according to your OS type.

# How to use:

## First time use:
  
  - At the first start you should navigate to Settings by pressing the appropriate button on top of the application window.
  - Provide at least one of the Stable Diffusion executable path (including the executable!).
  - Save it and your application is ready to be used.

## Generate image:

- Provide a name of the project. It can be theoretically anything.
- Provide Positive Prompt.
- Provide Negative Prompt.
- Provide Image name. You can do it with the little save icon right side of the input field below the Image name field or copy&paste the direct path to the target image.
- Provide steps between 3 and 100
- Choose which type of diffusion you wanted to use
- Push the start button and wait.

When the diffusion ready the generated image will be visible and the status changed to "finished", the Actions buttons become available.

  


# Pre-Alpha photos (developer insight if you like...):

### OnnxStream GUI running on Windows 11:
![kép](https://github.com/ThomAce/OnnxStreamGui/assets/34764511/d6302eb3-0820-418d-8292-fbf1f86dedb7)

![kép](https://github.com/ThomAce/OnnxStreamGui/assets/34764511/3e8184c7-7b10-4ab9-bba9-19fa1804ccc8)


### OnnxStream GUI running on Raspbian:
![kép](https://github.com/ThomAce/OnnxStreamGui/assets/34764511/b3eca91d-3df7-461e-89a3-b43abfee693a)

![kép](https://github.com/ThomAce/OnnxStreamGui/assets/34764511/843be03d-cfb3-4d26-8028-3e598d25b10d)




