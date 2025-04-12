import os
import random
from datetime import datetime

from django.contrib.auth.models import User
from faker import Faker
from django.core.files import File
from PIL import Image
import io
from ads.models import Ads

fake = Faker()

def generate_img():
    folder = 'SwapSphere/images/'
    image = Image.new('RGB', (100, 100), color='green')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    file_name = f'fake_{timestamp}.png'
    file_path = os.path.join(folder, file_name)
    image.save(file_path, format='PNG')
    return file_path


def create_ads(user):
    title = fake.sentence(nb_words=5)
    description = fake.text(max_nb_chars=300)
    category = random.choice(['Electronics', 'Clothing', 'Furniture', 'Books', 'Toys'])
    condition = random.choice(['new', 'used'])

    ad = Ads.objects.create(
        user=user,
        title=title,
        description=description,
        image_url=generate_img(),
        category=category,
        condition=condition,
        created_at=fake.date_this_decade()
    )
    return ad


def filling_db(n=100):
    users = User.objects.all()
    for _ in range(n):
        user = random.choice(users)
        create_ads(user)
        print(f'Объявление для пользователя {user.username}')