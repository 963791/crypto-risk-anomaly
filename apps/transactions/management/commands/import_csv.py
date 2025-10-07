import csv
from django.core.management.base import BaseCommand
from apps.transactions.models import Batch, Transaction
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Import transactions from CSV. CSV must have tx_hash,from_address,to_address,amount,timestamp"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=str)
        parser.add_argument("--batch-name", type=str, default="imported")
        parser.add_argument("--user", type=str, default=None)

    def handle(self, *args, **kwargs):
        csvfile = kwargs["csvfile"]
        batch_name = kwargs["batch_name"]
        username = kwargs["user"]
        user = None
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING("User not found, continuing without user"))

        batch = Batch.objects.create(name=batch_name, uploaded_by=user)
        count = 0
        with open(csvfile, newline='') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    Transaction.objects.update_or_create(
                        tx_hash=r["tx_hash"],
                        defaults={
                            "batch": batch,
                            "from_address": r.get("from_address"),
                            "to_address": r.get("to_address"),
                            "amount": r.get("amount") or 0,
                            "fee": r.get("fee") or None,
                            "timestamp": parse_datetime(r.get("timestamp")) or r.get("timestamp"),
                        }
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed row: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Imported {count} rows into batch {batch.id}"))
