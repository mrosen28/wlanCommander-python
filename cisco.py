import getpass,sys,telnetlib

ap = telnetlib.Telnet()
#GET AP NAMES FROM "SHOW AP SUMMARY" LIST?
ap1 = "AP881d.fc1d.d9e0"
ap2 = "AP80e0.1dc8.6ecc"
apName = None
connected = False
HOST = "192.168.188.3" #Controller IP Address
PORT = 23 #Telnet Port

def connect():
    global connected,ap
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
    #Disable Radios
    ap.write("ap name " + apName + " ap dot11 5ghz shutdown\n")
    ap.read_until("#")
    ap.write("ap name " + apName + " ap dot11 24ghz shutdown\n")
    ap.read_until("#")

    #Enable 802.11 Bands (bg/n/ac)
    if band == "24ghz":
        print("Enabling: 802.11bg / Disabling: 802.11ac")
        ap.write("ap dot11 24ghz dot11g\n")
        ap.read_until("[y]")
        ap.write("\n")
        ap.read_until("#")
        ap.write("no ap dot11 24ghz shutdown\n")
    elif band == "5ghz":
        print("Enabling: 802.11ac / Disabling: 802.11bg")
        ap.write("no ap dot11 24ghz dot11g\n")
        ap.read_until("[y]")
        ap.write("\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz dot11ac\n")
        ap.read_until("#")
        ap.write("no ap dot11 5ghz shutdown\n")
    ap.read_until("#")
    #802.11n Support
    #nRadioSupport = raw_input("Enable 802.11n Support? (y/n):")
    # if nRadioSupport == "y":
    #     ap.write("ap dot11 24ghz dot11n\n")
    #     ap.read_until("#")
    #     ap.write("ap dot11 5ghz dot11n\n")
    # else:
    print("Enabling 802.11n")
    ap.write("no ap dot11 24ghz dot11n\n")
    ap.read_until("#")
    ap.write("no ap dot11 5ghz dot11n\n")
    ap.read_until("#")

    #Set Data Rates
    print("Setting Data Rates")
    aSupportedRates = [18,24,36,48,54]
    bDisabledRates = [1,2,5.5,6,9,11,12,18,24,36,48,54]
    bMCSRates = [1,2,3,4,5,6,7]
    aMCSRates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    acMCSRates = [8,9]
    if band == "24ghz"
        if channel == 3:
            ap.write("ap dot11 24ghz rate 11 mandatory")
            ap.read_until("#")
        elif channel == 6:
            ap.write("ap dot11 24ghz rate 11 disable")
            ap.read_until("#")

        for x in bDisabledRates:
            ap.write("ap dot11 24ghz rate " + str(x) + " disable\n")
            ap.read_until("#")

        for x in bMCSRates:
            ap.write("ap dot11 24ghz dot11n mcs tx " + str(x) + "\n")
            ap.read_until("#")

    else:
        ap.write("ap dot11 5ghz rate 6 disable\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz rate 9 disable\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz rate 12 mandatory\n")
        ap.read_until("#")
        for x in aSupportedRates:
            ap.write("ap dot11 5ghz rate " + str(x) + " supported\n")
            ap.read_until("#")

        for x in aMCSRates:
            ap.write("ap dot11 5ghz dot11n mcs tx " + str(x) + "\n")
            ap.read_until("#")

        for x in acMCSRates:
            ap.write("ap dot11 5ghz dot11ac mcs tx " + str(x) + "spatial-stream 1\n")
            ap.read_until("#")
            ap.write("ap dot11 5ghz dot11ac mcs tx " + str(x) + "spatial-stream 2\n")
            ap.read_until("#")

    #Channel/Bandwidth Selection
    print("Setting AP to Broadcast on Frequency: " + str(channel) + ". (Bandwidth = " + str(bandwidth) + "MHz)")
    if band == "802.11b":
        ap.write("ap name " + apName + " dot11 24ghz channel " + str(channel) + "\n")#2.4GHz Channel Setting
    else:
        ap.write("ap name " + apName + " dot11 5ghz channel " + str(channel) + "\n")#5GHz Channel Setting
        ap.write("ap name " + apName + " dot11 5ghz channel width " + str(bandwidth) + "\n")#5GHz Channel Width
    ap.read_until("#")

    #Enable Radios
    print("Enabling " + band + "  Radio")
    ap.write("ap name " + apName + " no dot11 " + band + "shutdown\n")
    ap.read_until("#")

def configAP(select):
    global apName
    ap.write("config terminal\n")
    ap.read_until("#")
    print("Now Configuring...")

    print("Select AP:")
    print("1: AP881d.fc1d.d9e0")
    print("2: AP80e0.1dc8.6ecc")
    apChoice = raw_input("Enter #:")
    if apChoice == 1:
        apName = ap1
    else:
        apName = ap2

    if select < 2:
        band = "24ghz"
    else:
        band = "5ghz"

    if select == 1:
        channel = 3
    elif select == 2:
        channel = 6
    elif select == 3:
        channel = 36
    elif select == 4:
        channel = 38
    elif select == 5:
        channel = 42
    elif select == 6:
        channel = 149
    elif select == 7:
        channel = 151
    elif select == 8:
        channel = 155

    if select in [1,2,3,6]:
        bandwidth = 20
    elif select in [4,7]:
        bandwidth = 40
    elif select in [5,8]:
        bandwidth = 80

    setRadio(band,bandwidth,channel)

    ap.write("end\n")
    ap.read_until("#")

def printMenu():
    print 30 * "-" , "MENU" , 30 * "-"
    if not connected:
        print ("0. Connect to Controller")
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
