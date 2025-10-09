# apps/transactions/validators.py
import re
from django.core.exceptions import ValidationError

ETH_ADDR_RE = re.compile(r'^0x[a-fA-F0-9]{40}$')
TX_HASH_RE = re.compile(r'^0x[a-fA-F0-9]{64}$')

def validate_ethereum_address(value):
    if value is None:
        return
    if not ETH_ADDR_RE.match(value):
        raise ValidationError(f'{value} is not a valid Ethereum address')

def validate_transaction_hash(value):
    if value is None:
        return
    if not TX_HASH_RE.match(value):
        raise ValidationError(f'{value} is not a valid transaction hash')

def validate_csv_file(value):
    if not getattr(value, 'name', '').lower().endswith('.csv'):
        raise ValidationError('Only CSV files are allowed')
    max_size = 10 * 1024 * 1024  # 10MB
    if getattr(value, 'size', 0) > max_size:
        raise ValidationError('CSV must be under 10MB')

