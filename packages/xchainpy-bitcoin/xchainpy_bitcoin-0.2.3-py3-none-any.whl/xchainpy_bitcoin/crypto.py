from bip_utils.bip.bip_keys import BipPrivateKey
from mnemonic import Mnemonic
from bip_utils import Bip32, P2WPKH, BitcoinConf
from bip_utils.conf import Bip32Conf

def mnemonic_to_seed(mnemonic, language="english"):
    """Convert mnemonic (phrase) to seed

    :param mnemonic: A phrase
    :type mnemonic: str
    :param language: language
    :type language: str
    :returns: seed
    """
    mnemo = Mnemonic(language)
    seed = mnemo.to_seed(mnemonic)
    return seed

def mnemonic_to_private_key(mnemonic:str, derivation_path:str, network:str, mnemonic_language:str='english') -> BipPrivateKey:
    """Convert mnemonic (phrase) to a private key

    :param mnemonic: A phrase
    :type mnemonic: str
    :param derivation_path: derivation_path. example: "m/84'/0'/0'/0/1"
    :type derivation_path: str
    :param network: for example 'mainnet' or 'testnet'
    :type network: str
    :returns: private_key
    """
    seed = mnemonic_to_seed(mnemonic=mnemonic, language=mnemonic_language)
    key_net_ver = Bip32Conf.KEY_NET_VER.Test() if network == 'testnet' else Bip32Conf.KEY_NET_VER.Main()
    bip32_ctx = Bip32.FromSeedAndPath(seed, derivation_path, key_net_ver)
    private_key = bip32_ctx.PrivateKey()

    return private_key

def mnemonic_to_address(mnemonic:str, derivation_path:str, network:str, mnemonic_language:str='english') -> str:
    """Convert a private key to a public key

    :param mnemonic: A phrase
    :type mnemonic: str
    :param network: for example 'mainnet' or 'testnet'
    :type network: str
    :param derivation_path: derivation_path
    :type derivation_path: str
    :param mnemonic_language: A language
    :type mnemonic_language: str
    :returns: address
    """
    seed = mnemonic_to_seed(mnemonic=mnemonic, language=mnemonic_language)
    bip32_ctx = Bip32.FromSeedAndPath(seed, derivation_path)
    public_key_bytes = bip32_ctx.PublicKey().RawCompressed().ToBytes()

    net_addr_ver = BitcoinConf.P2WPKH_NET_VER.Test() if network == 'testnet' else BitcoinConf.P2WPKH_NET_VER.Main()
    address = P2WPKH.ToAddress(pub_key_bytes=public_key_bytes, net_addr_ver=net_addr_ver)
    return address