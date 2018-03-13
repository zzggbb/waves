# W A V E S
Visualize audio in the frequency and time domain

![waves.png](images/waves.png)

### Features
* simultaneous display of time, frequency, and time-frequency domains
* waveform smoothing to reduce flickering
* on the fly adjustments of all parameters:
  * sample rate
  * sample size
  * gain ratio
  * smooth ratio
  * width and height of output window
  * number of bars displayed
  * gradient start and stop colors

### Key Bindings
* b - decrease number of displayed bars
* B - increase number of displayed bars
* g - decrease gain ratio
* G - increase gain ratio
* n - halve sample size
* N - double sample size
* r - decrease sample rate
* R - increase sample rate
* s - decrease smoothing ratio
* S - increase smoothing ratio
* w - decrease output window width
* W - increase output window width

### Getting Started
You will need python3 installed.

Download the project and create a virtual environment:
```
$ git clone https://github.com/zzggbb/waves
$ cd waves
$ python3 -m virtualenv .
```

Enter the virtual environment and install required packages:
```
$ source bin/activate
$ pip install -r requirements.txt
```

Run the visualizer:
```
$ python3 waves.py
```

Leave the virtual env:
```
$ deactivate
```
