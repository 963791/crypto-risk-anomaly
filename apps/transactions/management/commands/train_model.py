from django.core.management.base import BaseCommand
import pandas as pd
from apps.ml_engine.model_trainer import train_and_persist_models

class Command(BaseCommand):
    help = "Train ML models using CSV dataset (labeled)"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=str, help="Path to labeled CSV (must include label column)")

    def handle(self, *args, **kwargs):
        csvfile = kwargs["csvfile"]
        df = pd.read_csv(csvfile)
        train_and_persist_models(df)
        self.stdout.write(self.style.SUCCESS("Training complete and artifacts persisted"))
