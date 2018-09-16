"""
The module contains internal data representation in SATOSA and general converteras that can be used
for converting from SAML/OAuth/OpenID connect to the internal representation.
"""
from saml2.saml import NAMEID_FORMAT_TRANSIENT
from saml2.saml import NAMEID_FORMAT_PERSISTENT
import datetime
import hashlib
from enum import Enum


def hash_data(salt, value):
    """
    Hashes a value together with a salt.
    :type salt: str
    :type value: str
    :param salt: hash salt
    :param value: value to hash together with the salt
    :return: hash value (SHA512)
    """
    return hashlib.sha512((value + salt).encode("utf-8")).hexdigest()


class AuthenticationInformation(object):
    """
    Class that holds information about the authentication
    """

    def __init__(self, auth_class_ref, timestamp, issuer):
        """
        Initiate the data carrier

        :type auth_class_ref: str
        :type timestamp: str
        :type issuer: str

        :param auth_class_ref: What method that was used for the authentication
        :param timestamp: Time when the authentication was done
        :param issuer: Where the authentication was done
        """
        self.auth_class_ref = auth_class_ref
        self.timestamp = timestamp
        self.issuer = issuer

    @staticmethod
    def from_dict(auth_info_dict):
        """
        :type auth_info_dict: dict[str, str]
        :rtype: satosa.internal_data.AuthenticationInformation
        :param auth_info_dict: A dict representation of an AuthenticationInformation object
        :return: An AuthenticationInformation object
        """
        return AuthenticationInformation(auth_info_dict["auth_class_ref"],
                                         auth_info_dict["timestamp"],
                                         auth_info_dict["issuer"])

    def to_dict(self):
        """
        Converts an AuthenticationInformation object to a dict
        :rtype: dict[str, str]
        :return: A dict representation of the object
        """
        return {"issuer": self.issuer,
                "timestamp": self.timestamp,
                "auth_class_ref": self.auth_class_ref,}


class InternalData(object):
    """
    A base class for the data carriers between frontends/backends
    """
    pass


class InternalRequest(InternalData):
    """
    Internal request for SATOSA.
    """

    def __init__(self, user_id_hash_type, requester, requester_name=None):
        """

        :param user_id_hash_type:
        :param requester: identifier of the requester

        :type user_id_hash_type: UserIdHashType
        :type requester: str
        """
        self.user_id_hash_type = user_id_hash_type
        self.requester = requester
        if requester_name:
            self.requester_name = requester_name
        else:
            self.requester_name = [{"text": requester, "lang": "en"}]
        self.approved_attributes = None


class InternalResponse(InternalData):
    """
    Holds internal representation of service related data.

    :type _user_id: str
    :type attributes: dict[str, str]
    :type user_id_hash_type: UserIdHashType
    :type auth_info: AuthenticationInformation
    """

    def __init__(self, auth_info=None):
        super().__init__()
        self.user_id = None
        # This dict is a data carrier between frontend and backend modules.
        self.attributes = {}
        self.auth_info = auth_info
        self.user_id_hash_type = None
        self.requester = None

    @staticmethod
    def from_dict(int_resp_dict):
        """
        :type int_resp_dict: dict[str, dict[str, str] | str]
        :rtype: satosa.internal_data.InternalResponse
        :param int_resp_dict: A dict representation of an InternalResponse object
        :return: An InternalResponse object
        """
        auth_info = AuthenticationInformation.from_dict(int_resp_dict["auth_info"])
        internal_response = InternalResponse(auth_info=auth_info)
        internal_response.user_id_hash_type = int_resp_dict["hash_type"]
        internal_response.attributes = int_resp_dict["attr"]
        internal_response.user_id = int_resp_dict["usr_id"]
        internal_response.requester = int_resp_dict["to"]
        return internal_response

    def to_dict(self):
        """
        Converts an InternalResponse object to a dict
        :rtype: dict[str, dict[str, str] | str]
        :return: A dict representation of the object
        """
        _dict = {
            "usr_id": self.user_id,
            "attr": self.attributes,
            "to": self.requester,
            "auth_info": self.auth_info.to_dict(),
            "hash_type": self.user_id_hash_type,
        }
        return _dict
