# W A V E S
Visualize audio in the frequency and time domain

![double.png](images/double.png)

### Features
* simultaneous display of time and frequency domain
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

### Notes
Gain and Smoothing:

These are the more interesting parameters... Smoothing controls the preference
of the bars to be where the samples tell them to be to be and where they *used*
to be. If the smoothing is high (above 0.5), the waves will act *viscously*.
If it is low (below 0.5), the waves will move quickly and flicker. Gain
controls the *spread* of the bars. High gain will make high bars higher, and
low bars lower. Low gain will make high bars lower, and low bars higher.
Play around with these parameters for some interesting effects! For example,
a high gain and high smoothing combination will cause the wave to split into a
high and low half. The gain will control how far away these halves are, and
the smoothing will control how bars transition between the halves.

Pygame Surfaces:

`Waves.time_surface` and `Waves.freq_surface` hold time domain and
frequency domain output. `Waves.control_surface` holds the parameter
labels and their values. These three surfaces are then blitted to
the main `Waves.surface`.

The Stream:

`Waves.stream` represents the audio stream. It is an abstraction layer
above the PyAudio stream. It handles cumbersome things such as closing
and reopening the PyAudio stream whenever the sample rate or sample
size changes.

Outputs:

The width of each displayed bar is given by `output width / number of bars`.
Gaps between bars will arise if this result is not an integer.
`Waves.outputs` handles this problem by predefining display formats. Each
format defines an output width and a list of numbers which evenly divide
the output width.

Performance:

Performance is detrimentally affected by the number of displayed bars.
If the output and the music get out of sync, try reducing the number of bars.
Hopefully this can be fixed in the future...
