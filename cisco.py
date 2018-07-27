import getpass,sys,telnetlib

ap = telnetlib.Telnet()
connected = False
HOST = "192.168.188.3" #Controller IP Address
PORT = 23 #Telnet Port
lowBandChannels = [3,6]
highBandChannels = [36,38,42,149,151,155]

def connect():
    global ap,connected
    ap = telnetlib.Telnet()
    ap.open(HOST,PORT)
    ap.read_until("Username: ")
    user = raw_input("Enter AP Username: ")
    ap.write(user + "\n")
    ap.read_until("Password: ")
    password = getpass.getpass()
    ap.write(password + "\n")
    connected = True

def elevatePrivileges():
    global ap
    ap.write("en\n") #Enable
    ap.read_until("Password: ")
    enablePassword = getpass.getpass()
    ap.write(enablePassword + "\n")
    print ap.read_until("#")

def setRadioBands(band):
    if band == 2.4:
        print("Enabling: 2.4GHz / Disabling: 5GHz")
        ap.write("ap dot11 5ghz shutdown\n")
        ap.read_until("#")
        ap.write("no ap dot11 24ghz shutdown\n")
        ap.read_until("#")
        ap.write("ap dot11 24ghz dot11g")
        ap.read_until("#")
    elif band == 5.0:
        print("Enabling: 5GHz / Disabling: 2.4GHz")
        ap.write("ap dot11 24ghz shutdown\n")
        ap.read_until("#")
        ap.write("no ap dot11 5ghz shutdown\n")
        ap.read_until("#")

    elif band == None:
        print("No Band Selected?")

    ap.write("end\n")

def setRadioChannel(channel):
    print("Setting AP to Broadcast on Channel: " + str(channel))
    ap.write("configure terminal\n")
    if channel in lowBandChannels:
        ap.write("interface dot11Radio 0\n") #2.4GHz Radio
        ap.read_until("#")
    else:
        ap.write("interface dot11Radio 1\n") #5GHz Radio
        ap.read_until("#")

    read_until("#") #Wait for Prompt
    ap.write("channel " + str(channel) + "\n")
    ap.read_until("#")
    ap.write("end\n")
    ap.read_until("#")

def setBandWidth(bandwidth):
    print("Setting Channel Bandwidth To: " + str(bandwidth))
    ap.write("config 802.11a chan_width " + APname + " " + bandwidth + "\n")
    ap.read_until("#")
    ap.write("end\n")
    ap.read_until("#")

def configAP(select):
    if select < 2:
        setRadioBands(2.4)
    else:
        setRadioBands(5.0)

    if select == 1:
        setRadioChannel(3)
    elif select == 2:
        setRadioChannel(6)
    elif select == 3 or select == 4 or select == 5:
        setRadioChannel(36)
    elif select == 6 or select == 7 or select == 8:
        setRadioChannel(149)

    if select == 3 or select == 6:
        setBandWidth(20)
    elif select == 4 or select == 7:
        setBandWidth(40)
    elif select == 5 or select == 8:
        setBandWidth(80)

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
                print("Elevating Privileges... ")
                elevatePrivileges()
            else:
                print("Already Connected.")
                continue
        elif select == 9:
            quit()
        else:
            configAP(select)

#Run
main()
