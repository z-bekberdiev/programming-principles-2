from json import load
from os import system


with open("practice-4/exercises/sample-data.json", "r") as file:
    system("clear")
    print("\n")
    system("clear")
    data = load(file)
    print("Interface Status")
    print("=" * 82)
    print("DN" + " " * 43 + "Description" + " " * 10 + "Speed" + " " * 5 + "MTU")
    print("-" * 44 + " " + "-" * 20 + " " + "-" * 9 + " " + "-" * 6)
    for item in data["imdata"]:
        print(item["l1PhysIf"]["attributes"]["dn"] + " " * (45 - len(item["l1PhysIf"]["attributes"]["dn"])) + item["l1PhysIf"]["attributes"]["descr"] + " " * (21 - len(item["l1PhysIf"]["attributes"]["descr"])) + item["l1PhysIf"]["attributes"]["speed"] + " " * (10 - len(item["l1PhysIf"]["attributes"]["speed"])) + item["l1PhysIf"]["attributes"]["mtu"])


"""
Interface Status
==================================================================================
DN                                           Description          Speed     MTU
-------------------------------------------- -------------------- --------- ------
topology/pod-1/node-201/sys/phys-[eth1/33]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/34]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/35]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/36]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/1]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/2]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/3]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/4]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/5]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/6]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/7]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/8]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/9]                         inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/10]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/11]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/12]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/13]                        inherit   9150
topology/pod-1/node-201/sys/phys-[eth1/14]                        inherit   9150
"""