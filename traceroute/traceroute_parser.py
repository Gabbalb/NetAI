import re

def parse_traceroute_output(output):
    hops = []
    if not output:
        return hops

    lines = output.splitlines()
    for line in lines:
        # Cerca indirizzi IP in formato IPv4
        match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
        if match:
            ip = match.group()
            hops.append(ip)
    return hops
