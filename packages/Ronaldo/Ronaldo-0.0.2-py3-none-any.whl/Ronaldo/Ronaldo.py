
import argparse
import sys

from Ip import *
from Domain import *
def myparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', dest='User', type=str, default='root', help='target User')
    parser.add_argument('-s', '--sex', dest='Sex', type=str, choices=['男', '女'], default='男', help='target Sex')
    parser.add_argument('-n', '--number', dest='Num', nargs=2, required=True, type=int, help='target Two Numbers')
    print(parser.parse_args())

# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    Util.getmyip()
    banner = '''
            __________                         .__       .___       
            \______   \  ____    ____  _____   |  |    __| _/ ____  
             |       _/ /  _ \  /    \ \__  \  |  |   / __ | /  _ \ 
             |    |   \(  <_> )|   |  \ / __ \_|  |__/ /_/ |(  <_> )
             |____|_  / \____/ |___|  /(____  /|____/\____ | \____/ 
                    \/              \/      \/            \/        
    '''
    print(Fore.GREEN+banner)
    if len(sys.argv) >= 2:
        if Util.isip(sys.argv[1]):
            ip = Ip(sys.argv[1])
            ip.gather()
            ip.out()
        else:
            domain = Domain(sys.argv[1])
            domain.gather()
            domain.out()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
