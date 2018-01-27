class Outputs(object):
    def __init__(self):
        self.formats = [
            (320, [320, 160, 80, 64, 40, 32, 20, 16, 10, 8, 5, 4, 2, 1]),
            (480, [480, 240, 160, 120, 96, 80, 60, 48, 40, 32, 30, 24, 20, 16,
                   15, 12, 10, 8, 6, 5, 4, 3, 2, 1]),
            (640, [640, 320, 160, 128, 80, 64, 40, 32, 20, 16, 10, 8, 5, 4, 2,
                   1]),
            (768, [768, 384, 256, 192, 128, 96, 64, 48, 32, 24, 16, 12, 8, 6,
                   4, 3, 2, 1]),
            (800, [800, 400, 200, 160, 100, 80, 50, 40, 32, 25, 20, 16, 10, 8,
                   5, 4, 2, 1]),
            (1024, [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]),
            (1280, [1280, 640, 320, 256, 160, 128, 80, 64, 40, 32, 20, 16, 10,
                    8, 5, 4, 2, 1]),
            (1440, [1440, 720, 480, 360, 288, 240, 180, 160, 144, 120, 96, 90,
                    80, 72, 60, 48, 45, 40, 36, 32, 30, 24, 20, 18, 16, 15, 12,
                    10, 9, 8, 6, 5, 4, 3, 2, 1]),
            (1600, [1600, 800, 400, 320, 200, 160, 100, 80, 64, 50, 40, 32,
                    25, 20, 16, 10, 8, 5, 4, 2, 1]),
            (1920, [1920, 960, 640, 480, 384, 320, 240, 192, 160, 128, 120, 96,
                    80, 64, 60, 48, 40, 32, 30, 24, 20, 16, 15, 12, 10, 8, 6,
                    5, 4, 3, 2, 1]),
            (2560, [2560, 1280, 640, 512, 320, 256, 160, 128, 80, 64, 40, 32,
                    20, 16, 10, 8, 5, 4, 2, 1]),
            (3440, [3440, 1720, 860, 688, 430, 344, 215, 172, 86, 80, 43, 40,
                    20, 16, 10, 8, 5, 4, 2, 1]),
            (3840, [3840, 1920, 1280, 960, 768, 640, 480, 384, 320, 256, 240,
                    192, 160, 128, 120, 96, 80, 64, 60, 48, 40, 32, 30, 24,
                    20, 16, 15, 12, 10, 8, 6, 5, 4, 3, 2, 1])
        ]
        self.num_formats = len(self.formats)

        self.format_index = 9
        self.divisor_index = 1

    def _set_best_divisor(self, target_ratio):
        best_diff = float('inf')
        last_diff = best_diff
        best_index = 0
        width = self.get_width()
        for index, divisor in enumerate(self._get_divisors()):
            ratio = width / divisor
            diff = abs(ratio - target_ratio)

            # we've found a new best diff
            if diff < best_diff:
                best_index = index
                best_diff = diff

            last_diff = diff

        self.divisor_index = best_index

    def _get_divisors(self):
        return self.formats[self.format_index][1]

    def get_width(self):
        return self.formats[self.format_index][0]

    def get_divisor(self):
        return self._get_divisors()[self.divisor_index]

    def next_width(self):
        if self.format_index == self.num_formats - 1:
            return
        old_ratio = self.get_width() / self.get_divisor()
        self.format_index += 1
        self._set_best_divisor(old_ratio)

    def prev_width(self):
        if self.format_index == 0:
            return
        old_ratio = self.get_width() / self.get_divisor()
        self.format_index -= 1
        self._set_best_divisor(old_ratio)

    def next_divisor(self):
        if self.divisor_index > 0:
            self.divisor_index -= 1

    def prev_divisor(self):
        divisors = self.formats[self.format_index][1]
        if self.divisor_index < len(divisors) - 1:
            self.divisor_index += 1
