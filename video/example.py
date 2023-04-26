from pynput import keyboard

def on_press(key):
    try:
        print('Key {} pressed.'.format(key.char))
    except AttributeError:
        print('Key {} pressed.'.format(key))

def on_release(key):
    print('Key {} released.'.format(key))
    if key == keyboard.Key.esc:
        return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()