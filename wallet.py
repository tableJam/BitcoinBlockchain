from ecdsa import NIST256p;
from ecdsa import SigningKey;
import base58
import codecs
import hashlib
import util

#ecdsa and NIST256 curve create PrivateKey
#PublicKey from PrivateKey and do sign
#Transaction contain PublicKey and sign

class Wallet(object):
  def __init__(self):
    self._privateKey = SigningKey.generate(curve=NIST256p)
    self._publicKey = self._privateKey.get_verifying_key();

  @property
  def publicKey(self):
    return self._publicKey.to_string().hex();
  @property
  def privateKey(self):
    return self._privateKey.to_string().hex(); 

  def generateBlockchainAddress(self):
        #########
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ##########
        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')
        ##########
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemed160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
        network_bitcoin_public_key, 'hex')
        ##########
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_hex[:8]
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address
if __name__ == '__main__':
  wallet = Wallet();
  