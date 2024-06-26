import re
import subprocess
from argparse import ArgumentParser
from ipwhois import IPWhois
from prettytable import PrettyTable

IP_REGEX = r'(?:\d{1,3}\.){3}\d{1,3}'


def get_ip(ip):
    ip = {}
    try:
        res = IPWhois(ip).lookup_rdap()
    except Exception as e:
        res = {}
    ip['asn'] = res.get('asn')
    ip['country'] = res.get('asn_country_code')
    ip['provider'] = res.get('network', {}).get('name')
    return ip

def tracert(host):
    return subprocess.run(f'tracert -d -w 50 {host}',
                          capture_output=True, text=True).stdout



def get_arg_parser():
    parser = ArgumentParser()
    parser.add_argument('host',
                        help='IP address or domain name')
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    host = args.host
    addresses = re.findall(IP_REGEX, tracert(host))[1:]
    table = PrettyTable(['#', 'ip', 'asn', 'country', 'provider'])
    res = [(get_ip(ip)) for ip in addresses]
    n = 1

    for row in res:
        table.add_row([n] + [(row.get(k) or '-') for k in row.keys()])
        n += 1

    print(f'\nTracing a route to "{host}":\n')
    print(table)
    print('\nTracing completed.')


if __name__ == '__main__':
    main()
