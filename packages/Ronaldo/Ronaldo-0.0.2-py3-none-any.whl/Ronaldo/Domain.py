from colorama import Fore

import Util


class Domain:
    def __init__(self,domain):
        self.domain = domain
    def gather(self):
        self.ip = Util.domaingetip(self.domain)
        self.address =self.ip+"\t"+ Util.getip(self.ip)
    def out(self):
        print(Fore.BLUE + "Search Domain's Ip info:\t"+self.domain+"\t" + self.address)

