#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

from time import sleep
import paramiko
import sys, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # ser_

sys.path.append(BASE_DIR)
sys.path.append("..\py_Tude")
print(BASE_DIR)
from configini_crw import *

from tkinter import *
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.messagebox 

# from pingable_console_ import *

class Application(tk.Frame):

    def __init__(self, master = None):

        # python2
        ## tk.Frame.__init__(self, master)
        ## self.master = master
        ## self.create_widgets()
        self.__root = ""
        self.__title = r" _ Turbo Easelay ZTP © 2021 - Inertia Register _ Powerby TSunx @ V.T.G.A "

    def create_widgets(self):

        window = tk.Tk()
        window.title(self.__title)

        root = tk.Frame(window)
        root.pack(side=tk.TOP, fill=tk.X)
        self.__root = root

        Button(root, text = ' Turbo Easelay ZTP - Inertia Register ', command = self.nodeferregistration).grid(row = 99, column = 1)

        self.ipmgmt = StringVar()
        Label(root, text = ' Mgmt over IP ').grid(row = 2, column = 0)
        # Entry(root, textvariable = self.ipmgmt).grid(row = 2, column = 1, sticky = EW)
        Label(root, text = ' 10.10.10.10/8 ').grid(row = 2, column = 1)

        self.portWanNumber = StringVar()
        Entry(root, textvariable = self.portWanNumber).grid(row = 3, column = 1, sticky = EW)
        # Button(root, text = ' Unknown Reachability ', command = self.unknownreachability).grid(row = 3, column = 1)
        Button(root, text = ' Wan Anchor ', command = self.interfaces_brief).grid(row = 3, column = 0)
        Label(root, text = ' 0..WAN / 100..LTE ').grid(row = 3, column = 2)
        self.portWanNumber.set("0")

        self.pushscriptname = StringVar()
        Button(root, text = ' Script Basing * ', command = self.selectPushScript).grid(row = 4, column = 0)
        Entry(root, textvariable = self.pushscriptname).grid(row = 4, column = 1, sticky = EW)

        Label(root, text = ' DHCP Default If Skip ').grid(row = 12, column = 1)

        self.code_addresskey = StringVar()
        Label(root, text = ' Prime key ').grid(row = 13, column = 0)
        Entry(root, textvariable = self.code_addresskey).grid(row = 13, column = 1, sticky = EW)
        Label(root, text = '    IPv4 / PPPoE_U ').grid(row = 13, column = 2)

        self.code_gatewaykey = StringVar()
        Label(root, text = ' Pass way ').grid(row = 14, column = 0)
        Entry(root, textvariable = self.code_gatewaykey).grid(row = 14, column = 1, sticky = EW)
        Label(root, text = ' Gateway / PPPoE_P ').grid(row = 14, column = 2)

        # Button(root, text = ' Push & Registration ', command = self.push).grid(row = 55, column = 1)
        Label(root, text = '').grid(row = 58, column = 1)
        Button(root, text = ' OFF ', command = root.quit, fg = "red").grid(row = 0, column = 2)
        Label(root, text = ' Refer to v21.2.x, v16.10.x, v16.8.x ').grid(row = 299, column = 1)

        window.mainloop()

    def interfaces_brief(self):
        if '' == self.ipmgmt.get():
            ipmgmt = "10.10.10.10"
        else:
            ipmgmt = self.ipmgmt.get()
        print(ipmgmt)
        if  '' == self.portWanNumber.get():
            portwannumber = "0"
        else:
            portwannumber = self.portWanNumber.get()
        print(portwannumber)
        self.interfaces_briefHandler(wport = portwannumber, mgr = ipmgmt)


    def interfaces_briefHandler(self, wport, mgr):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # connect to client
            client.connect(mgr, 22, 'admin', 'versa123')
            ## get shell
            ssh_shell = client.invoke_shell()
            ## send('cli\n')
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                #print (line)
                #if  '$' in line:
                if ('$' in line) or ('#' in line):
                    break;
            ssh_shell.sendall( 'cli' + '\n' )
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                #print (line)
                if '>' in line:
                    break;
            lines = []
            print(" interfaces brief handler to run")
            ssh_shell.sendall( '\n' + '\n' )
            #urscript = "request interfaces oper-down vni-0/" + wport.strip().encode() + ".0 seconds 100\n"
            urscript = "show interfaces brief vni-0/" + wport.strip().encode() + "\n"
            #print(urscript.encode())
            #print(wport.strip().encode())
            print(" the handler is to run \n ")
            ssh_shell.send(urscript.encode() + '\n')
            #
            #ssh_shell.sendall( 'request interfaces oper-down vni-0/0.0 seconds 100' + '\n' )
            #print("vni-0/0.0")
            #ssh_shell.sendall( 'request interfaces oper-down vni-0/100.0 seconds 100' + '\n' )
            #print("vni-0/100.0")
            print("... about, then to check reachability on VD ")
            #ssh_shell.sendall( '\n' + '\n' )
            #ssh_shell.sendall( '\n' + '\n' )
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                print(line)
                #print(" Please waiting...")
                if ("error" in line):
                    #dscript = "echo " + s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode() + " >> ztp_ezsd.sh\n"
                    #print(dscript)
                    #ssh_shell.send(dscript.encode())
                    #ssh_shell.send('\n')
                    print ("[error]")
                    break;
                if ("ok" in line):
                    #dscript = "echo " + s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode() + " >> ztp_ezsd.sh\n"
                    #print(dscript)
                    #ssh_shell.send(dscript.encode())
                    #ssh_shell.send('\n')
                    print ("[ok]")
                    break;
                #if ('$' in line) or ('#' in line):
                #    break;
                #
            print(" Next Step...")
            ssh_shell.close()
            client.close()
            return ("Interfaces Brief")
        except Exception as e:
            print("--abnormal--:", e)
            return ("WARNING: The script \" " + "escript" + " \" only print on screen, not to run directly on the cpe!")


    def unknownreachability(self):
        if '' == self.ipmgmt.get():
            ipmgmt = "10.10.10.10"
        else:
            ipmgmt = self.ipmgmt.get()
        print(ipmgmt)
        if  '' == self.portWanNumber.get():
            portwannumber = "0"
        else:
            portwannumber = self.portWanNumber.get()
        print(portwannumber)
        self.unknownreachabilityhandler(wport = portwannumber, mgr = ipmgmt)


    def unknownreachabilityhandler(self, wport, mgr):
      try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print(dir(ssh))
        #
        # ser.write("\n".encode())
        # ser.write("\n".encode())
        # iflogin = ser.readline().decode()
        # print(iflogin)
        # connect to client
        client.connect(mgr, 22, 'admin', 'versa123')
        # client.connect('10.10.10.10',22,'admin','versa123')
        ## get shell
        ssh_shell = client.invoke_shell()
        ## send('cli\n')
        # ready when line endswith '>' or other character
        while True:
            line = ssh_shell.recv(1024)
            #print (line)
            #if  '$' in line:
            if ('$' in line) or ('#' in line):
                break;
        ssh_shell.sendall( 'cli' + '\n' )
        # ready when line endswith '>' or other character
        while True:
            line = ssh_shell.recv(1024)
            #print (line)
            if '>' in line:
                break;
        lines = []
        print("unknown reachability handler to run")
        ssh_shell.sendall( '\n' + '\n' )
        urscript = "request interfaces oper-down vni-0/" + wport.strip().encode() + ".0 seconds 100\n"
        # print(urscript.encode())
        # print(wport.strip().encode())
        print(" the handler is to run \n ")
        ssh_shell.send(urscript.encode() + '\n')
        #
        # ssh_shell.sendall( 'request interfaces oper-down vni-0/0.0 seconds 100' + '\n' )
        # print("vni-0/0.0")
        # ssh_shell.sendall( 'request interfaces oper-down vni-0/100.0 seconds 100' + '\n' )
        # print("vni-0/100.0")
        print("... about, then to check reachability on VD ")
        ssh_shell.sendall( '\n' + '\n' )
        '''
        ssh_shell.sendall( 'show interfaces brief' + '\n' )
        # ready when line endswith '>' or other character
        while True:
            line = ssh_shell.recv(1024)
            print (line)
            l = line.split('\r\n')
            lines.append(l)
            #if '' in line:
            #if ('' in line) or ('>' in line):
            if ('[' in line) or ('>' in line):
                break;
        # print lines
        str = ""
        for li in lines[-1]:
            str = li
            if  ("Hardware ID number" in li):
                break;
            if  ("Serial" in li):
                break;
            else:
                pass
                #str = li
                #print(li)
        sn = str.split("number")
        # print(sn)
        # print(sn[1].strip())
        SN = sn[1].strip()
        print("Pull-in the Serial number: ", SN)
        '''
        ssh_shell.sendall( '\n' + '\n' )
        # ready when line endswith '>' or other character
        while True:
            line = ssh_shell.recv(1024)
            #print (line)
            if '>' in line:
                break;
        ssh_shell.send('exit' + '\n')
        while True:
            line = ssh_shell.recv(1024)
            #print(line)
            #if '$' in line:
            if ('$' in line) or ('#' in line) :
                break;
        print("")
        ssh_shell.close()
        client.close()
        return ("Unknown Reachability Handler")
      except Exception as e:
        print("--abnormal--:", e)
        return ("WARNING: The script \" " + "escript" + " \" only print on screen, not to run directly on the cpe!")


    def nodeferregistration(self):
      try:
        with open(self.pushscriptname.get(), 'r') as file:
            rdata = file.read()
        # print("push: ", rdata)
        if '' == self.ipmgmt.get():
            ipmgmt = "10.10.10.10"
        else:
            ipmgmt = self.ipmgmt.get()
        # print(ipmgmt)
        os.system('ping {}'.format(ipmgmt))
        if  '' == self.portWanNumber.get():
            portwannumber = "0"
        else:
            portwannumber = self.portWanNumber.get()
        print("- Ported Wan ", portwannumber)
        pushscriptname = self.pushscriptname.get()
        # print("- Script ", pushscriptname)
        code_addresskey = self.code_addresskey.get()
        print(code_addresskey)
        code_gatewaykey = self.code_gatewaykey.get()
        print(code_gatewaykey)
        self.sshlink(wport = portwannumber, ipnet = code_addresskey, ipgw = code_gatewaykey, defer = "False", mgr = ipmgmt, mainscript = pushscriptname)
      except IOError as e:
        print("file name is null (script-basing-on)")
        exit(1)


    def sshlink(self, wport, ipnet, ipgw, defer, mgr, mainscript):
        ROOT = 'config_appliance_driver_preassocation'
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Connectclient
            client.connect(mgr, 22, 'admin', 'versa123')
            # Getshell
            ssh_shell = client.invoke_shell()
            # Cli mode send('cli\n')
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                # print (line)
                if ('$' in line) or ('#' in line):
                    break;
            ssh_shell.sendall( 'cli' + '\n' )
            # Ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                # print (line)
                if '>' in line:
                    break;
            # Get lines
            lines = []
            ssh_shell.sendall( 'show system detail' + '\n' )
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                # print (line)
                l = line.split('\r\n')
                lines.append(l)
                if ('[' in line) or ('>' in line):
                    break;
            # Print lines
            str = ""
            for li in lines[-1]:
                str = li
                if  ("Hardware ID number" in li):
                    break;
                if  ("Serial" in li):
                    break;
                else:
                    pass
            sn = str.split("number")
            # print(sn)
            SN = sn[1].strip()
            print("The Serial Number of CPE: ", SN)
            #
            ssh_shell.send(chr(3))
            ssh_shell.sendall( '\n' + '\n' )
            #
            # ready when line endswith '>' or other character
            while True:
                line = ssh_shell.recv(1024)
                # print(line)
                if '>' in line:
                    break;
            ssh_shell.send('exit' + '\n')
            while True:
                line = ssh_shell.recv(1024)
                # print(line)
                if ('$' in line) or ('#' in line) :
                    break;
            # Push the script
            scriptf = open(mainscript, 'r')
            script = scriptf.readlines()
            # print(wport)
            # print(ipnet)
            # print(ipgw)
            swport = " -w " + wport
            print(swport)
            # When ipnet is not . split , ipnet be pu
            # When ipgw is not . split, ipgw be pp
            if ("." not in ipnet):
                sipnet = " -p -pu " + ipnet
            else:
                sipnet = " -s " + ipnet
            if ("." not in ipgw):
                sipgw = " -pp " + ipgw
            else:
                sipgw = " -g " + ipgw
            #
            print(sipnet)
            print(sipgw)
            if (ipnet == "" and ipgw == ""):
                sipnet = " -d "
                sipgw = ""
            sscript = []
            for s in script:
                # print(s)
                escript = "echo " + s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode() + " >> ztp_ezs.sh\n"
                # escript = "echo " + s.strip().encode() + " >> ztp_versa.sh\n"
                # print(escript.encode())
                # ser.write(escript.encode())
                ##ssh_shell.send(escript.encode() + '\n')
                if defer == "True":
                    print(" the script is defer to run \n ")
                    ssh_shell.send(escript.encode() + '\n')
                    # deferscript = s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode()
                else:
                    #
                    # Not Delay, Run it directly !
                    #
                    deferscript = s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode()
                    # print(deferscript)
                    print(" Start up running ")
                    #
                    ssh_shell.send(deferscript.encode())
                    ssh_shell.send('\n')
                    ssh_shell.sendall( 'versa123' + '\n' )
                while True:
                    line = ssh_shell.recv(1024)
                    # print(line)
                    print(" Please waiting...")
                    if ("generated" in line):
                        dscript = "echo " + s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode() + " >> ztp_ezsd.sh\n"
                        # print(dscript)
                        ssh_shell.send(dscript.encode())
                        ssh_shell.send('\n')
                        print ("[ok] Loading generated config into CDB")
                        break;
                    if ("erase" in line):
                        dscript = "echo " + s.strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode() + " >> ztp_ezsd.sh\n"
                        # print(dscript)
                        ssh_shell.send(dscript.encode())
                        ssh_shell.send('\n')
                        print ("[!] - Found existing config on system\n")
                        print ("[!] - Please issue \"request erase running-config\" from CLI and try staging after that")
                        break;
                    if ('$' in line) or ('#' in line):
                        break;
                sscript.append(s)
                sscript.append(swport)
                sscript.append(sipnet)
                sscript.append(sipgw)          
            print("")
            print(" ))) The template of main body for ztp : ", mainscript)
            print(", has been pushed! ((( ")
            #
            pathdssh = "." + os.sep + ROOT + os.sep + "CADP_ssh_" + SN + ".ini"
            cfg = CreateConfigIni(pathdssh)
            cfg.createConfigSection("Basic")
            cfg.parseConfig("Basic", "organization", "")
            cfg.parseConfig("Basic", "name", "")
            cfg.parseConfig("Basic", "serialnumber", SN)
            cfg.parseConfig("Basic", "devicegroup", "")
            cfg.createConfigSection("LocationInformation")
            cfg.parseConfig("LocationInformation", "Address", "*")
            cfg.createConfigSection("BindData")
            cfg.parseConfig("BindData", "linkfrom", "ssh")
            cfg.parseConfig("BindData", "wan_port", wport)
            cfg.parseConfig("BindData", "wan_ipmask", ipnet)
            cfg.parseConfig("BindData", "wan_gw", ipgw)
            cfg.parseConfig("BindData", "lan_ipmask", "")
            cfg.parseConfig("BindData", "lan_gw", "")
            sleep(2)
            #
            ssh_shell.close()
            client.close()
            sscript.append(SN)
            return (sscript)
        except Exception as e:
            # config_devices_draft_default.ini
            # w_0_ip_mask
            # w_0_gateway
            #
            pathd0 = "." + os.sep + ROOT + os.sep + "CADP_current_" + ".ini"
            cfg = CreateConfigIni(pathd0)
            cfg.createConfigSection("Basic")
            cfg.parseConfig("Basic", "organization", "")
            cfg.parseConfig("Basic", "name", "")
            cfg.parseConfig("Basic", "serialnumber", "*")
            cfg.parseConfig("Basic", "devicegroup", "")
            cfg.createConfigSection("LocationInformation")
            cfg.parseConfig("LocationInformation", "Address", "*")
            cfg.createConfigSection("BindData")
            cfg.parseConfig("BindData", "linkfrom", "ssh")
            cfg.parseConfig("BindData", "wan_port", wport)
            cfg.parseConfig("BindData", "wan_ipmask", ipnet)
            cfg.parseConfig("BindData", "wan_gw", ipgw)
            cfg.parseConfig("BindData", "lan_ipmask", "")
            cfg.parseConfig("BindData", "lan_gw", "")
            cfg.createConfigSection("Script")
            # cfg.parseConfig("Script", "default", "")
            scriptf = open(mainscript, 'r')
            script = scriptf.readlines()
            # script = "sudo /opt/versa/scripts/staging.py -l SDWAN-Branch@shct.com -r controller01-staging@shct.com -c 61.151.158.115 -w 0 -s IP/MASK -g GATEWAY"
            #
            # When ipnet is not . split , ipnet be pu
            # When ipgw is not .split, ipgw be pp
            if ("." not in ipnet):
                sipnet = " -p -pu " + ipnet
            else:
                sipnet = " -s " + ipnet
            if ("." not in ipgw):
                sipgw = " -pp " + ipgw
            else:
                sipgw = " -g " + ipgw
            swport = " -w " + wport
            # print(swport)
            ##sipnet = " -s " + ipnet
            # print(sipnet)
            ##sipgw = " -g " + ipgw
            # print(sipgw)
            if (ipnet == "" and ipgw == ""):
                sipnet = " -d "
                sipgw = ""
            #
            # print(script)
            # print(escript.encode())
            escript = script[0].strip().encode() + " " + swport.strip().encode() + " " + sipnet.strip().encode() + " " + sipgw.strip().encode()
            script_opt = ""
            script_option = "w_" + wport
            script_opt = script_option
            # print(script_opt)
            print(" Script ".center(40, '-'))
            print("cd /opt/versa/scripts")
            print(escript)
            print(" Based. ".center(40, '-'))
            # cfg.parseConfig("Script", script_opt, escript)
            print("")
            print("[!] - The template of main body for ztp : ", mainscript)
            print(" Show in current ! ".center(40, '-'))
            #
            print("--abnormal--:", e)
            return ("WARNING: The script \" " + escript + " \" only print on screen, not to run directly on the cpe!")


    def push(self):
        with open(self.pushscriptname.get(), 'r') as file:
            rdata = file.read()
        # print("push: ", rdata)
        if '' == self.ipmgmt.get():
            ipmgmt = "10.10.10.10"
        else:
            ipmgmt = self.ipmgmt.get()
        print(ipmgmt)
        if  '' == self.portWanNumber.get():
            portwannumber = "100"
        else:
            portwannumber = self.portWanNumber.get()
        print("- Anchored Wan ", portwannumber)
        pushscriptname = self.pushscriptname.get()
        # print("- Script ", pushscriptname)
        code_addresskey = self.code_addresskey.get()
        print(code_addresskey)
        code_gatewaykey = self.code_gatewaykey.get()
        print(code_gatewaykey)
        self.sshlink(wport = portwannumber, ipnet = code_addresskey, ipgw = code_gatewaykey, defer = "True", mgr = ipmgmt, mainscript = pushscriptname)


    def selectPushScript(self):
        filepath = askopenfilename()
        self.pushscriptname.set(filepath)


    def file_message(self, msg):
        result = tkinter.messagebox.askokcancel(title = 'message', message = msg)


if __name__ == "__main__":
    tbm = Application()
    tbm.create_widgets()


## root = tk.Tk()
# root.title('TSunx')
## root.title(' _ Turbo Easelay ZTP - Inertia Register _ Powerby TSunx @ V.T.G.A ')
## app = Application(master = root)
## app.mainloop()
#