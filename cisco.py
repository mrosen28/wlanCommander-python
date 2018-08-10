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
    global connected,ap,apName

    ap = telnetlib.Telnet()
    ap.open(HOST,PORT)
    ap.read_until("Username: ")
    user = raw_input("Enter AP Username: ")
    ap.write(user + "\n")
    ap.read_until("Password: ")
    password = getpass.getpass()
    ap.write(password + "\n")
    password = None

    ap.write("terminal length 0\n")
    ap.read_until(">")


    print("Elevating Privileges... ")
    ap.write("en\n") #Enable
    ap.read_until("Password: ")
    enablePassword = getpass.getpass()
    ap.write(enablePassword + "\n")
    ap.read_until("#")
    enablePassword = None
    print("Root Privileges Enabled!")

    if apName == None:
        print("Select AP:")
        print("1: AP881d.fc1d.d9e0")
        print("2: AP80e0.1dc8.6ecc")
        apChoice = raw_input("Enter #:")
        if apChoice == 1:
            apName = ap1
        else:
            apName = ap2
            
                apList = []
                
        #ap.write("show ap dot11 " + band + " summary\n")
        #for i in range(3): #Remove Extra String Data
            #ap.read_until("\n")
        #apList.append(ap.read_until(" "))
        #ap.read_until("\n")
        #apList.append(ap.read_until(" "))
        #ap.read_until("#")

        #print("Select AP:")
        #apNum = 0
        #for foundAP in apList:
            #print(apNum + ": " + foundAP)
            #apNum += 1
        #apChoice = raw_input("Enter #:")
        #apName = apList[apChoice]


    connected = True

def setRadio(band,bandwidth,channel):
    ap.write("config terminal\n")
    ap.read_until("#")
    print("Now Configuring...")

    #Disable Networks
    ap.write("ap dot11 5ghz shutdown\n")
    ap.read_until("#")
    ap.write("ap dot11 24ghz shutdown\n")
    ap.read_until("#")


    #Enable 802.11 Bands (bg/n/ac)
    #802.11n Support
    #nRadioSupport = raw_input("Enable 802.11n Support? (y/n):")
    # if nRadioSupport == "y":
    #     ap.write("ap dot11 24ghz dot11n\n")
    #     ap.read_until("#")
    #     ap.write("ap dot11 5ghz dot11n\n")
    # else:
    print("Enabling 802.11n!")
    ap.write("ap dot11 " + band + " dot11n\n")
    ap.read_until("#")

    #Set Data Rates
    print("Setting Data Rates...")
    aSupportedRates = ["RATE_18M","RATE_24M","RATE_36M","RATE_48M","RATE_54M"]
    bDisabledRates = ["RATE_1M","RATE_2M","RATE_5_5M","RATE_6M","RATE_9M"]
    bSupportedRates = ["RATE_12M","RATE_18M","RATE_24M","RATE_36M","RATE_48M","RATE_54M"]
    bMCSRates = ["RATE_1M","RATE_2M","RATE_3M","RATE_4M","RATE_5M","RATE_6M","RATE_7M"]
    aMCSRates = ["RATE_1M","RATE_2M","RATE_3M","RATE_4M","RATE_5M","RATE_6M","RATE_7M","RATE_8M","RATE_9M","RATE_10M","RATE_11M","RATE_12M","RATE_13M","RATE_14M","RATE_15M"]
    acMCSRates = ["RATE_8M","RATE_9M"]
    if band == "24ghz":
        if channel in [3,6]:
            ap.write("ap dot11 24ghz rate RATE_11M mandatory\n")
            ap.read_until("#")

        for x in bDisabledRates:
            ap.write("ap dot11 24ghz rate " + str(x) + " disable\n")
            ap.read_until("#")

        for x in bSupportedRates:
            ap.write("ap dot11 24ghz rate " + str(x) + " supported\n")
            ap.read_until("#")

        for x in bMCSRates:
            ap.write("ap dot11 24ghz dot11n mcs tx " + str(x) + "\n")
            ap.read_until("#")

    elif band == "5ghz":
        ap.write("ap dot11 5ghz rate RATE_6M disable\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz rate RATE_9M disable\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz rate RATE_12M mandatory\n")
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


    if band == "24ghz":
        print("Enabling: 802.11bg!")
        ap.write("ap dot11 24ghz dot11g\n")
        ap.read_until("[y]")
        ap.write("\n")
        ap.read_until("#")
        ap.write("no ap dot11 24ghz shutdown\n")
    elif band == "5ghz":
        print("Enabling: 802.11a/ac!")
        ap.write("no ap dot11 24ghz dot11g\n")
        ap.read_until("[y]")
        ap.write("\n")
        ap.read_until("#")
        ap.write("ap dot11 5ghz dot11ac\n")
        ap.read_until("#")
        ap.write("no ap dot11 5ghz shutdown\n")
    ap.read_until("#")

    #Exit Configure Terminal
    ap.write("end\n")
    ap.read_until("#")

    #Channel/Bandwidth Selection
    print("Setting AP to Broadcast on Channel: " + str(channel) + " (Bandwidth = " + str(bandwidth) + "MHz)")
    if band == "24ghz":
        ap.write("ap name " + apName + " dot11 24ghz channel " + str(channel) + "\n")#2.4GHz Channel Setting
    elif band == "5ghz":
        ap.write("ap name " + apName + " dot11 5ghz channel " + str(channel) + "\n")#5GHz Channel Setting
        ap.read_until("#")
        ap.write("ap name " + apName + " dot11 5ghz channel width " + str(bandwidth) + "\n")#5GHz Channel Width
    ap.read_until("#")

    #Enable Selected Radio
    ap.write("no ap dot11 " + band + " shutdown\n")
    ap.read_until("#")

    print("Enabling " + band + " Radio!")
    ap.write("ap name " + apName + " no dot11 " + band + "shutdown\n")
    ap.read_until("#")

    #Show Current Radio Config
    ap.write("show ap dot11 " + band + " summary\n")
    ap.read_until("summary")
    apSummary = ap.read_until("#")
    apSummary = apSummary[0:len(apSummary)-10]
    print (apSummary)
    if band == "5ghz":
        ap.write("show ap dot11 5ghz network\n")
    elif band == "24ghz":
        ap.write("show ap dot11 24ghz network\n")

    ap.read_until("Operational Rates")
    opRates = ap.read_until("802.11n MCS Settings:")
    opRates = opRates[0:len(opRates)-21]
    print ("Operational Rates:" + opRates)
    mcsRates = ap.read_until("802.11n Status:")
    mcsRates = mcsRates[0:len(mcsRates)-15]
    print("MCS Rates:" + mcsRates)
    ap.read_until("#")


def configAP(select):
    band="24ghz"if select<=2 else "5ghz"

    if select == 1:
        channel = 3
    elif select == 2:
        channel = 6
    elif select in [3,4,5]:
        channel = 36
    elif select in [6,7,8]:
        channel = 149

    if select in [1,2,3,6]:
        bandwidth = 20
    elif select in [4,7]:
        bandwidth = 40
    elif select in [5,8]:
        bandwidth = 80

    setRadio(band,bandwidth,channel)

def printMenu():
    print 30 * "-" , "MENU" , 30 * "-"
    if not connected:
        print ("0. Connect to Controller")
    else:
        print ("(0) Connected to Controller @ " + HOST + " (Selected AP: " + apName + ")")
        print ("1. Test Setup 1: 2.4GHz - Channel 3 - 20MHz")
        print ("2. Test Setup 2: 2.4GHz - Channel 6 - 20MHz")
        print ("3. Test Setup 3: 5GHz - Channel 36 - 20MHz")
        print ("4. Test Setup 4: 5GHz - Channel 36 - 40MHz")
        print ("5. Test Setup 5: 5GHz - Channel 36 - 80MHz")
        print ("6. Test Setup 6: 5GHz - Channel 149 - 20MHz")
        print ("7. Test Setup 7: 5GHz - Channel 149 - 40MHz")
        print ("8. Test Setup 8: 5GHz - Channel 149 - 80MHz")
        print ("9. Exit")
    print 23 * "-" , "Zebra Technologies", 23 * "-"

def main():
    while True:
        printMenu()
        select = int(input("Enter Choice Number: "))
        if select not in range(9):
            print("Incorrect Entry! Try Again!")
            continue
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
