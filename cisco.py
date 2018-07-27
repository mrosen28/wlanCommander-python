import getpass,sys,telnetlib

ap = telnetlib.Telnet()
connected = False
HOST = "192.168.188.3" #Controller IP Address
PORT = 23 #Telnet Port

def connect():
    ap = telnetlib.Telnet()
    ap.open(HOST,PORT)
    ap.read_until("Username: ")
    user = raw_input("Enter AP Username: ")
    ap.write(user + "\n")
    ap.read_until("Password: ")
    password = getpass.getpass()
    ap.write(password + "\n")

    print("Elevating Privileges... ")
    ap.write("en\n") #Enable
    ap.read_until("Password: ")
    enablePassword = getpass.getpass()
    ap.write(enablePassword + "\n")
    print ap.read_until("#")

    connected = True

def setRadio(band,bandwidth,channel):
    #Set 802.11 Band (bg/a)
    if band == "802.11b":
        print("Enabling: 802.11b/g / Disabling: 802.11a")
        ap.write("ap dot11 5ghz shutdown\n")
        ap.read_until("#")
        ap.write("no ap dot11 24ghz shutdown\n")
        ap.read_until("#")
        ap.write("config 802.11b 11gSupport enable\n")
    elif band == "802.11a":
        print("Enabling: 802.11a / Disabling: 802.11b/g")
        ap.write("ap dot11 24ghz shutdown\n")
        ap.read_until("#")
        ap.write("no ap dot11 5ghz shutdown\n")
    ap.read_until("#")

    #802.11n Support
    nRadioSupport = raw_input("Enable 802.11n Support? (y/n):")
    if nRadioSupport == "y":
        ap.write("config " + band + " 11nSupport enable\n")
        ap.read_until("#")
    else:
        ap.write("config " + band + " 11nSupport disable\n")
        ap.read_until("#")

    #Channel/Bandwidth Selection
    print("Setting AP to Broadcast on Channel: " + str(channel))
    print("Setting Channel Bandwidth To: " + str(bandwidth))

    if band == "802.11b":
        ap.write("interface dot11radio0\n") #2.4GHz Radio
    else:
        ap.write("interface dot11radio1\n") #5GHz Radio

    ap.read_until("#")
    ap.write("channel " + str(channel) + " " + str(bandwidth) + "\n")
    ap.read_until("#")

def configAP(select):
    channel,band,bandwidth = None
    ap.write("config terminal\n")
    print ap.read_until("#")
    print("Now Configuring...")
    if select < 2:
        band = "802.11b"
    else:
        band = "802.11a"

    if select == 1:
        channel = 2422
    elif select == 2:
        channel = 2437
    elif select == 3:
        channel = 5180
    elif select == 4:
        channel = 5190
    elif select == 5:
        channel = 5210
    elif select == 6:
        channel = 5745
    elif select == 7:
        channel = 5755
    elif select == 8:
        channel = 5775

    if select == 3 or select == 6:
        bandwidth = 20
    elif select == 4 or select == 7:
        bandwidth = 40
    elif select == 5 or select == 8:
        bandwidth = 80

    setRadio(band,bandwidth,channel)

    ap.write("end\n")
    ap.read_until("#")

def printMenu():
    print 30 * "-" , "MENU" , 30 * "-"
    if not connected:
        print ("0. Connect to Controller & Elevate Priveleges")
    else:
        print ("(0) Connected to Controller @ " + HOST)
        print ("1. Test Setup 1: 2.4GHz - Channel 3 - 20MHz")
        print ("2. Test Setup 2: 2.4GHz - Channel 6 - 20MHz")
        print ("3. Test Setup 3: 5GHz - Channel 36 - 20MHz")
        print ("4. Test Setup 4: 5GHz - Channel 38 - 40MHz")
        print ("5. Test Setup 5: 5GHz - Channel 42 - 80MHz")
        print ("6. Test Setup 6: 5GHz - Channel 149 - 20MHz")
        print ("7. Test Setup 7: 5GHz - Channel 151 - 40MHz")
        print ("8. Test Setup 8: 5GHz - Channel 155 - 80MHz")
        print ("9. Exit")
    print 23 * "-" , "Zebra Technologies", 23 * "-"

def main():
    while True:
        printMenu()
        select = int(input("Enter Choice Number: "))
        if select == 0:
            if not connected:
                print("Connecting...")
                connect()
            else:
                print("Already Connected.")
                continue
        elif select == 9:
            quit()
        else:
            configAP(select)

#Run
main()
