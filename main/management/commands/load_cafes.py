import os
import json
from django.core.management.base import BaseCommand
from main.models import Cafe  # Cafe 모델 가져오기
from django.conf import settings  # BASE_DIR 사용


class Command(BaseCommand):
    help = "Load cafes from a JSON file located in the main app's data directory"

    def handle(self, *args, **kwargs):
        # JSON 파일 경로 설정
        file_path = os.path.join(settings.BASE_DIR, 'main', 'data.json')

        try:
            # JSON 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # JSON 데이터를 Cafe 모델에 저장
            for entry in data:
                Cafe.objects.update_or_create(
                    name=entry['name'],
                    defaults={
                        'address': entry.get('address'),
                        'isConcentrate': entry.get('isConcentrate', False),
                        'opening_hours': entry.get('opening_hours'),
                        'latitude': float(entry['latitude']),
                        'longitude': float(entry['longitude']),
                    }
                )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully loaded {len(data)} cafes into the database from {file_path}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Invalid JSON format in file: {file_path}"))
