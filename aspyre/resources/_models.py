#   -------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------

from enum import StrEnum


class StoreName(StrEnum):
    ADDRESS_BOOK = 'AddressBook'
    AUTH_ROOT = 'AuthRoot'
    CERTIFICATE_AUTHORITY = 'CertificateAuthority'
    DISALLOWED = 'Disallowed'
    MY = 'My'
    ROOT = 'Root'
    TRUSTED_PEOPLE = 'TrustedPeople'
    TRUSTED_PUBLISHER = 'TrustedPublisher'


class StoreLocation(StrEnum):
    CURRENT_USER = 'CurrentUser'
    LOCAL_MACHINE = 'LocalMachine'


class IconVariant(StrEnum):
    REGULAR = 'Regular'
    FILLED = 'Filled'


class ProbeType(StrEnum):
    STARTUP = 'Startup'
    READINESS = 'Readiness'
    LIVENESS = 'Liveness'


class CertificateTrustScope(StrEnum):
    NONE = 'None'
    APPEND = 'Append'
    OVERRIDE = 'Override'
    SYSTEM = 'System'


class WaitBehavior(StrEnum):
    WAIT_ON_RESOURCE_UNAVAILABLE = 'WaitOnResourceUnavailable'
    STOP_ON_RESOURCE_UNAVAILABLE = 'StopOnResourceUnavailable'


class ProtocolType(StrEnum):
    UNKNOWN = 'Unknown'
    IP = 'IP'
    IPV6_HOP_BY_HOP_OPTIONS = 'IPv6HopByHopOptions'
    UNSPECIFIED = 'Unspecified'
    ICMP = 'Icmp'
    IGMP = 'Igmp'
    GGP = 'Ggp'
    IV4 = 'IPv4'
    TCP = 'Tcp'
    PUP = 'Pup'
    UDP = 'Udp'
    IDP = 'Idp'
    IV6 = 'IPv6'
    IPV6_ROUTING_HEADER = 'IPv6RoutingHeader'
    IPV6_FRAGMENT_HEADER = 'IPv6FragmentHeader'
    IPSEC_ENCAPSULATING_SECURITY_PAYLOAD = 'IPSecEncapsulatingSecurityPayload'
    IPSEC_AUTHENTICATION_HEADER = 'IPSecAuthenticationHeader'
    ICMPV6 = 'IcmpV6'
    IPV6_NO_NEXT_HEADER = 'IPv6NoNextHeader'
    IPV6_DESTINATION_OPTIONS = 'IPv6DestinationOptions'
    ND = 'ND'
    RAW = 'Raw'
    IPX = 'Ipx'
    SPX = 'Spx'
    SPXII = 'SpxII'

class ReferenceEnvironment(StrEnum):
    NONE = 'None'
    CONNECTION_STRING = 'ConnectionString'
    CONNECTION_PROPERTIES = 'ConnectionProperties'
    SERVICE_DISCOVERY = 'ServiceDiscovery'
    ENDPOINTS = 'Endpoints'
    ALL = 'All'


class OtlpProtocol(StrEnum):
    GRPC = 'Grpc'
    HTTP_PROTOBUF = 'HttpProtobuf'


class ContainerLifetime(StrEnum):
    SESSION = 'Session'
    PERSISTENT = 'Persistent'


class ImagePullPolicy(StrEnum):
    DEFAULT = 'Default'
    ALWAYS = 'Always'
    MISSING = 'Missing'


class UnixFileMode(StrEnum):
    NONE = 'None'
    OTHER_EXECUTE = 'OtherExecute'
    OTHER_WRITE = 'OtherWrite'
    OTHER_READ = 'OtherRead'
    GROUP_EXECUTE = 'GroupExecute'
    GROUP_WRITE = 'GroupWrite'
    GROUP_READ = 'GroupRead'
    USER_EXECUTE = 'UserExecute'
    USER_WRITE = 'UserWrite'
    USER_READ = 'UserRead'
    STICKY_BIT = 'StickyBit'
    SET_GROUP = 'SetGroup'
    SET_USER = 'SetUser'

