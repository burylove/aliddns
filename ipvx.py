#coding=utf-8
import socket
import subprocess
import config

def get_host_ip(host,address_family=socket.AF_INET6):
    """
    获取host对应的ipv4/ipv6地址
    :params host: 域名
    :params address_family:
        socket.AF_INET6: ipv6
        socket.AF_INET:  ipv4
    :return ip: 对应的ip
    """
    ip = None
    try:
        sock = socket.socket(address_family, socket.SOCK_DGRAM)
        sock.connect((host,80))
        ip = sock.getsockname()[0]
    except Exception as e:
        print(e)
        pass
    finally:
        sock.close()
    return ip


def get_host_ips_by_cmd(interface=None):
    """
    获取interface网口下的ip列表
    :params interface: 网卡名称
    :return ip_list: ip列表
    """
    if not interface:
        interface = config.INTERFACE
    cmd = f"ip addr show {interface} | grep 'inet6 [0-9].*scope global'"
    res = subprocess.check_output(cmd, shell=True).decode('utf-8').split('\n')
    ip_list = [info.strip().split(' ')[1].split('/')[0] for info in res if info.strip() != '']
    return ip_list

def get_host_ip_by_cmd(ip_list=None):
    """
    获取外网可用的ipv6
    :params ip_list:
    :return ip
    """
    if not ip_list:
        ip_list = get_host_ips_by_cmd()
    ip = ip_list[0]
    for ele in ip_list:
        if len(ip) > len(ele):
            ip = ele
    return ip


if __name__ == "__main__":
    # ip = get_host_ip(config.TEST_IPV6_HOST)
    # print(ip)

    ip_list = get_host_ips_by_cmd()
    print(ip_list)

    ip = get_host_ip_by_cmd(ip_list)
    print(ip)
