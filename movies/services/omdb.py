import requests
from django.conf import settings
from django.core.cache import cache
import hashlib
import json


class OMDBClient:
    """
    Клиент для работы с OMDb API.
    Инкапсулирует всю логику HTTP-запросов,
    чтобы views / services не знали про requests и API-детали.
    """

    def __init__(self):
        """
        Инициализация клиента.

        Проверяем, что API-ключ задан в settings.
        Это защита от тихих ошибок в проде.
        """
        if not settings.OMDB_API_KEY:
            raise RuntimeError("OMDB_API_KEY is not set")

        # Сохраняем ключ и базовый URL в объекте
        self.api_key = settings.OMDB_API_KEY
        self.base_url = settings.OMDB_BASE_URL

    def _make_cache_key(self, params: dict) -> str:

        params_str = json.dumps(params, sort_keys=True)
        hash_key = hashlib.md5(params_str.encode()).hexdigest()
        return f"omdb:{hash_key}"
    
    def _get(self, params):
        """
        Низкоуровневый метод для выполнения GET-запроса к OMDb.

        params — словарь параметров запроса (без api key).
        Этот метод:
        - добавляет api key
        - делает HTTP-запрос
        - проверяет HTTP-статус
        - возвращает JSON
        """

        params["apikey"] = self.api_key

        cache_key = self._make_cache_key(params)
        cached_response = cache.get(cache_key)
        
        if cached_response:
            return cached_response

        response = requests.get(
            self.base_url,
            params=params,
            timeout=10  
        )

        response.raise_for_status()

        data = response.json()

        cache.set(cache_key, data, timeout=60*60)
        return data
        
    
    def search_movie(self, title):
        """
        Поиск фильмов по названию.

        Использует параметр:
        s — search (поиск по названию)

        Возвращает список фильмов (если найдено).
        """
        return self._get({
            "s": title,
            "type": "movie",  # ограничиваем поиск фильмами
        })

    def get_movie_by_title(self, title):
        """
        Получение одного фильма по точному названию.

        Использует параметр:
        t — title (точное совпадение)

        plot=full — получить полное описание.
        """
        return self._get({
            "t": title,
            "plot": "full",
        })

    def get_movie_by_imdb_id(self, imdb_id):
        """
        Получение одного фильма по IMDb ID.

        Использует параметр:
        i — imdbID (например tt0137523)

        Это самый надёжный способ получить фильм.
        """
        return self._get({
            "i": imdb_id,
            "plot": "full",
        })
