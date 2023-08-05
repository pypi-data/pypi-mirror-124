from enum import Enum, unique

from .base_model import BaseModel


@unique
class COSEAlgorithmIdentifier(BaseModel, Enum):
    """ Identifies a cryptographic algorithm. The algorithm identifiers should be values registered in the
        IANA COSE Algorithms registry, for instance, -7 for ``ES256``.

        See `§5.10.5 <https://www.w3.org/TR/webauthn/#biblio-iana-cose-algs-reg>`_ """

    ALG_ES256 = -7
    """ ECDSA with SHA-256. """

    ALG_ES384 = -35
    """ ECDSA with SHA-384. """

    ALG_ES512 = -36
    """ ECDSA with SHA-512. """

    ALG_RS1 = -65535
    """ RSASSA-PKCS1-v1_5 with SHA-1. """

    ALG_RS256 = -257
    """ RSASSA-PKCS1-v1_5 with SHA-256. """

    ALG_RS384 = -258
    """ RSASSA-PKCS1-v1_5 with SHA-384. """

    ALG_RS512 = -259
    """ RSASSA-PKCS1-v1_5 with SHA-512. """

    ALG_PS256 = -37
    """ RSASSA-PSS with SHA-256. """

    ALG_PS384 = -38
    """ RSASSA-PSS with SHA-384. """

    ALG_PS512 = -39
    """ RSASSA-PSS with SHA-512. """

    ALG_EdDSA = -8
    """ EdDSA. """

    def to_json_serializable_internal(self):
        return self.value

    @classmethod
    def from_json_serializable(cls, obj):
        if obj is None:
            return None

        return COSEAlgorithmIdentifier(obj)
