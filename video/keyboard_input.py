import keyboard

while True:
    kin = keyboard.read_key()
    print(kin)
    if  kin == "space":
        print("Quit")
        break
