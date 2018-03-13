### Overall
* fix the lag when switching samples sizes by 'skipping' data frames
* test compatibility with macOS and windows
* add ability to change input device

### Frequency Output:
* more/better frequency bin scaling methods, currently just elliptical
* power scaling by maximum of each bin
* frequency domain smoothing

### Spectrogram
* control seconds per pixel: each pixel can represent between 1/(sample rate) and 1 second
* cache all samples, up to a maximum cache size
* each sample is 1024*16 bits = 2 KB.

### Controls
* keyboard+mouse input fields
* color parameters
* adjustable window height
