### BPM detection
Assume the beat lies in BPM_RANGE, for example 20-250hz. For each sampling
frame of size SAMPLE_SIZE, calcuate the average power of the frequencies in
BPM_RANGE. Store the average power of each frame in BPM_POWERS.

### Overall
* fix the lag when switching samples sizes by 'skipping' data frames
* test compatibility with macOS and windows
* add ability to change input device

### Frequency Output:
* power scaling by maximum of each bin

### Spectrogram
* control seconds per pixel: each pixel can represent between 1/(sample rate) and 1 second
* cache all samples, up to a maximum cache size
* each sample is 1024*16 bits = 2 KB.

### Controls
* keyboard+mouse input fields
* color parameters
* adjustable window height
