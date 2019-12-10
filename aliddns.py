#coding=utf-8
import config
from alidns import DnsRecord
from ipvx import get_host_ips_by_cmd, get_host_ip_by_cmd



def ddns():
    """
    run
    """
    dns_record = DnsRecord(config.ACCESS_KEY, config.ACCSEE_ID, config.TEST_HOST)

    # 获取可用的ip
    ip6_list = get_host_ips_by_cmd(interface=config.INTERFACE)
    ip6 = get_host_ip_by_cmd(ip6_list)
    print(ip6)
    # 设置/更新
    for rr in config.RR:
        info = dns_record.get(record=rr)
        print(info)

        if info:
            if info.get('Value') != ip6:
                res = dns_record.update(info['RecordId'], rr,ip6)
                print(f"set dns ip6{ip6} ===> dns{rr}.{config.TEST_HOST}:{res}")
        else:
            res = dns_record.set(record=rr,value=ip6)
            print(f"update dns ip6{ip6} ===> dns{rr}.{config.TEST_HOST}:{res}")


if __name__ == "__main__":
    ddns()
