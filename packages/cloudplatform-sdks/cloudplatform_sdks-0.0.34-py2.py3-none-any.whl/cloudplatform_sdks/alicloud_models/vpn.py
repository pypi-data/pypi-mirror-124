from .clients import vpn_client


class AliVpn:
    STATUS_MAPPER = {
        'active': 'started',
        'init': 'configuring',
        'provisioning': 'configuring',
        'updating': 'configuring',
        'deleting': 'deleting',
    }

    def __init__(self, object):
        self.object = object

    @classmethod
    def get(cls, vpn_id):
        result = vpn_client.describe_vpn_gateway({'VpnGatewayId': vpn_id})
        if result:
            return cls(result)
        return None

    @classmethod
    def list(cls, params=None):
        result = vpn_client.describe_vpns(params)
        vpns = result.get('VpnGateways', {}).get('VpnGateway', []) or []
        return [cls.get(vpn['VpnGatewayId']) for vpn in vpns]

    @classmethod
    def create(cls, params):
        res = vpn_client.create_vpn_gateway(params)
        return res.get('VpnGatewayId')

    def delete(self):
        return vpn_client.delete_vpn_gateway({'VpnGatewayId': self.external_id})

    @property
    def status(self):
        vpn_status = self.object.get('Status')
        return self.STATUS_MAPPER.get(vpn_status, 'lost')

    def modify_vpn_attribute(self, params):
        return vpn_client.modify_vpn_gateway(params)

    @property
    def external_id(self):
        return self.object.get('VpnGatewayId')

    @property
    def external_name(self):
        return self.object.get('Name') or self.external_id

    @property
    def vpc_id(self):
        return self.object.get('VpcId')

    @property
    def vswitch_id(self):
        return self.object.get('VSwitchId')

    @property
    def public_ip(self):
        return self.object.get('InternetIp')

    @property
    def end_time(self):
        return self.object.get('EndTime')

    @property
    def spec(self):
        return self.object.get('Spec')

    @property
    def description(self):
        return self.object.get('Description')

    @classmethod
    def cloud_type(cls):
        return vpn_client.config.get('cloud_type', '')


class AliCustomer:
    def __init__(self, object):
        self.object = object

    @classmethod
    def get(cls, customer_id):
        result = vpn_client.describe_customer_gateway({'CustomerGatewayId': customer_id})
        if result:
            return cls(result)
        return None

    @classmethod
    def list(cls, params=None):
        result = vpn_client.describe_customers(params)
        customers = result.get('CustomerGateways', {}).get('CustomerGateway', []) or []
        return [cls.get(customer['CustomerGatewayId']) for customer in customers]

    @classmethod
    def create(cls, params):
        result = vpn_client.create_customer_gateway(params)
        return result.get('CustomerGatewayId')

    def delete(self):
        return vpn_client.delete_customer_gateway({'CustomerGatewayId': self.external_id})

    @classmethod
    def modify_customer(cls, params):
        return vpn_client.modify_customer_gateway(params)

    @property
    def external_id(self):
        return self.object.get('CustomerGatewayId')

    @property
    def external_name(self):
        return self.object.get('Name')

    @property
    def ip_address(self):
        return self.object.get('IpAddress')

    @property
    def create_time(self):
        return self.object.get('CreateTime')

    @property
    def description(self):
        return self.object.get('Description')


class AliIPsec:
    def __init__(self, object):
        self.object = object

    @classmethod
    def get(cls, ipsec_id):
        result = vpn_client.describe_ipsec_gateway({'VpnConnectionId': ipsec_id})
        if result:
            return cls(result)
        return None

    @classmethod
    def list(cls, params=None):
        result = vpn_client.describe_ipsecs(params)
        ipsecs = result.get('VpnConnections', {}).get('VpnConnection', []) or []
        return [cls.get(ipsec['VpnConnectionId']) for ipsec in ipsecs]

    @classmethod
    def create(cls, params):
        result = vpn_client.create_ipsec_gateway(params)
        return result.get('VpnConnectionId')

    def delete(self):
        return vpn_client.delete_ipsec_gateway({'VpnConnectionId': self.external_id})

    @classmethod
    def modify_ipsec(cls, params):
        return vpn_client.modify_ipsec_gateway(params)

    @property
    def external_id(self):
        return self.object.get('VpnConnectionId')

    @property
    def external_name(self):
        return self.object.get('Name')

    @property
    def status(self):
        return self.object.get('Status')

    @property
    def customer_gateway_id(self):
        return self.object.get('CustomerGatewayId')

    @property
    def vpn_gateway_id(self):
        return self.object.get('VpnGatewayId')

    @property
    def local_subnet(self):
        return self.object.get('LocalSubnet')

    @property
    def remote_subnet(self):
        return self.object.get('RemoteSubnet')

    @property
    def effect_immediately(self):
        return self.object.get('EffectImmediately')

    @property
    def ike_config(self):
        return self.object.get('IkeConfig')

    @property
    def ipsec_config(self):
        return self.object.get('IpsecConfig')

    @property
    def vco_health_check(self):
        return self.object.get('VcoHealthCheck')

    @property
    def vpn_bgp_config(self):
        return self.object.get('VpnBgpConfig')


class AliRouteEntry():
    def __init__(self, object):
        self.object = object
