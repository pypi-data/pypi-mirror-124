import Util
from colorama import Fore

class Ip:
    def __init__(self,ip):
        self.ip = ip
        self.address = ""
        self.domain = []
    def gather(self):
        self.address =self.ip+"\t"+ Util.getip(self.ip)
        self.domain = Util.getdomain(self.ip)
    def out(self):
        print(Fore.BLUE +"Search Ip info:\t"+self.address)
        for i in range(0,len(self.domain)):
            print(Fore.BLUE +"Search Ip's domain:\t"+self.domain[i]+"\n")