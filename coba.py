from pynput.mouse import Button, Controller

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (0, 0)
print('Now we have moved it to {0}'.format(
    mouse.position))