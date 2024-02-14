
import json
import logging


from typing import List, Dict, Iterator

from .erc20 import ERC20
from .erc721 import ERC721
from .erc1155 import ERC1155

from sentinel.models.contract import ABISignature
from sentinel.db.contract.utils import to_signature_record


logger = logging.getLogger(__name__)


class StandardABISignatures:
    '''
    Standard ABI Signatures

    - ERC-20
    - ERC-721
    - ERC-1155
    '''
    def __init__(self, standards: List[str] = list()) -> None:
        '''
        Standard ABI Signatures Init
        '''
        self._db = []
        self._standards = standards
        self.update(standards=self._standards)

    @property
    def total_records(self):
        '''
        returns total records number in database
        '''
        return len(self._db)

    def update(self, standards: List[str] = list()) -> None:
        '''
        Update ABI Signatures
        '''
        if len(standards) == 0:
            return
        
        for standard in standards:
            if standard == 'ERC20':
                self._load('ERC20', json.loads(ERC20))
            elif standard == 'ERC721':
                self._load('ERC721', json.loads(ERC721))
            elif standard == 'ERC1155':
                self._load('ERC1155', json.loads(ERC1155))
            else:
                logger.warning(f'Unknown standard name, {standard}')

    def _load(self, standard: str,  abi_records: List[Dict]) -> None:
        '''
        Load ABI signatures to local database
        '''
        for abi_record in abi_records:
            self._db.append(to_signature_record(standard, abi_record))


    def search(self, standard: str = None, 
               signature_type: str = None, 
               signature_hash: str = None) -> Iterator[ABISignature]:
        '''
        Search signatures
        '''
        for signature in self._db:
            if standard is not None:
                if signature.contract_address != standard:
                    continue
            if signature_type is not None:
                if signature.type != signature_type:
                    continue 
            yield signature
