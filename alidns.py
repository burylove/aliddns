#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

import json
import config



class DnsRecord():
    def __init__(self,access_key=config.ACCESS_KEY, access_id=config.ACCSEE_ID, domain_name=config.TEST_HOST):
        """
        :param access_key: 
        :param access_id:
        :param domain_name
        """
        self.client = AcsClient(access_id, access_key, 'cn-hangzhou')
        self.domain = domain_name
        self.nds_list = []



    def get_dns_all(self, page_size=500):
        """
        获取解析记录列表
        """
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self.domain)
        request.set_PageSize(page_size)

        res = json.loads(str(self.client.do_action_with_exception(request), encoding='utf-8'))
        self.nds_list = res['DomainRecords'].get('Record')
        # TODO: 是否需要分页

        return self.nds_list

    def get(self, record,type_=config.TYPE_['IPV6']):
        """
        获取解析对应的ip
        :param recode: 主机记录
        """
        if not self.nds_list:
            self.get_dns_all()

        d = {
            r['RR']:r for r in self.nds_list if r["Type"] == type_
        }
        return d.get(record)


    def set(self, record, value, type_=config.TYPE_['IPV6']):
        """
        设置域名解析:
        :param record: 主机记录(前缀)
        :param value:  记录值(ip)
        :param type_: 解析类型(IPV6, IPV4)
        """
        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_DomainName(self.domain)
        request.set_RR(record)
        request.set_Type(type_)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        res = json.loads(str(response, encoding='utf-8'))
        return res

    def update(self,record_id, record, value, type_=config.TYPE_['IPV6']):
        """
        更新解析
        :param record_id 解析记录id
        :param record   主机记录
        :param value    记录值(ip)
        :param type_    解析类型(IPV6, IPV4)
        """
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        request.set_RecordId(record_id)
        request.set_RR(record)
        request.set_Type(type_)
        request.set_Value(value)
        response = self.client.do_action_with_exception(request)

        res = json.loads(str(response, encoding='utf-8'))
        return res


    

if __name__ == "__main__":
    record = DnsRecord(config.ACCESS_KEY, config.ACCSEE_ID,config.TEST_HOST)
    print(record.get_dns_all())
    # print(record.get('ss', type_=config.TYPE_['IPV4']))
    # print(record.set('hello', '47.101.191.40', config.TYPE_['IPV4']))
    # res = record.update('17023583676816384','hello','2400:a980:fe:4a9:7555:7bd9:f162:8528' )
    # print(res)





