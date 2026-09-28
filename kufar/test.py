import re
import requests

# Ссылка на нужное объявление
url = "https://www.kufar.by/item/1086880983"

# 1. Загружаем текст страницы
response = requests.get(url)

# 2. Ищем все пути к фотографиям внутри HTML
# На Kufar все пути картинок имеют вид: adim1/хххххххх-хххх-хххх-хххх-хххххххххххх.jpg
raw_paths = re.findall(r"adim1/[a-f0-9\-]+\.jpg", response.text)

# 3. Убираем дубликаты, сохраняя исходный порядок
unique_paths = list(dict.fromkeys(raw_paths))

# 4. Формируем готовые прямые URL
# Префикс /gallery/ дает фото в оригинальном максимальном разрешении
image_urls = [f"https://rms.kufar.by/v1/gallery/{path}" for path in unique_paths]

# Выводим полученные URL
print(image_urls[0])
