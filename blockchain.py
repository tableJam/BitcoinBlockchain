import time
import utils
import json
import hashlib
DIFFICULTY = 3;
SENDER = 'SATOSHINAKAMOTO';
REWORD = '0.1';
class Blockchain():
  def __init__(self,minerAddress:str) -> None:
    self.chain = [];
    self.transactionPool = [];
    self.createBlock(0,self.hash({}));
    self.minerAddress = minerAddress;

  def createBlock(self,nonce:int,previousHash:str):
    block = utils.sort_by_key({
      'timestamp': time.time(),
      'transactions': self.transactionPool,
      'nonce': nonce,
      'previous_hash':previousHash
    });
    self.chain.append(block);
    self.transactionPool = [];
    
  def hash(self,block:dict):
    sortedBlock = json.dumps(block,sort_keys=True);
    return hashlib.sha256(sortedBlock.encode()).hexdigest();

  def addTransaction(self,senderAddress:str,recipientAddress:str,value:int):
    transaction = utils.sort_by_key({
      'sender_address': senderAddress,
      'recipient_address': recipientAddress,
      'value': value
    });
    self.transactionPool.append(transaction);
  
  def proofOfWork(self):
    transactions = self.transactionPool.copy();
    previousHash = self.hash(self.chain[-1]);
    nonce = 0;
    while self.work(transactions,previousHash,nonce)==False:
      nonce+=1;
    return nonce;

  def work(self,transaction:list, previousHash:str,nonce:int,difficulty=DIFFICULTY):
    guessBlock =utils.sort_by_key({
      'transactions': transaction,
      'nonce': nonce,
      'previous_hash': previousHash
    })
    guessHash = self.hash(guessBlock);
    return guessHash[:difficulty] == '0'*difficulty;
  
  def mining(self):
    self.addTransaction(SENDER,self.minerAddress,REWORD);
    previousHash = self.hash(self.chain[-1]);
    nonce = self.proofOfWork();
    self.createBlock(nonce,previousHash);
    print('⛏⛏⛏⛏Mining Success⛏⛏⛏⛏')
    
  def balanceOf(self,targetAddress:str):
    balance = 0;
    for block in self.chain:
      for tx in block['transactions']:
        value = tx['value'];
        if tx['recipient_address'] == targetAddress:
          balance += value;
        elif tx['sender_address'] == targetAddress:
          balance -= value;
    return balance;
  
def pprint(chain):
  print('📦--'*5,'⛓blockchain⛓','--📦'*5);
  print('==='*15)
  for block in chain:
    print('📦', block);
    print('==='*15)
  
  print('-'*50);


if __name__ == '__main__':
  blockchain = Blockchain('0x86939381938329');
  pprint(blockchain.chain);
  blockchain.addTransaction('Alice','Bob',10);
  blockchain.addTransaction('Bob','Alice',20);
  blockchain.mining();
  pprint(blockchain.chain);
  print('Alice`Bitcoin',blockchain.balanceOf('Alice'))
  print('Bob`Bitcoin',blockchain.balanceOf('Bob'))
  
