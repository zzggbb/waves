from outputs import Outputs

outputs = Outputs()

outputs.format_index = 9
outputs.divisor_index = 3
# test get_width()
assert outputs.get_width() == 1920
# test get_divisor()
assert outputs.get_divisor() == 480

# test prev_width()
outputs.prev_width()
assert outputs.get_width() == 1600
assert outputs.get_divisor() == 400

# test next_widt()
outputs.next_width()
assert outputs.get_width() == 1920
assert outputs.get_divisor() == 480
