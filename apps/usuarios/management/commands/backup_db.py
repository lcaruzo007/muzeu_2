from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup automático do banco de dados'

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = settings.BASE_DIR / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        backup_file = backup_dir / f'backup_{timestamp}.json'
        
        with open(backup_file, 'w') as f:
            call_command('dumpdata', stdout=f, indent=2, exclude=['contenttypes', 'auth.permission'])
        
        self.stdout.write(self.style.SUCCESS(f'Backup criado: {backup_file}'))
