import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = self.get_channel_data()["items"][0]["snippet"]["title"]
        self.description = self.get_channel_data()["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + channel_id
        self.subscriberCount: int = self.get_channel_data()["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.get_channel_data()["items"][0]["statistics"]["videoCount"]
        self.view_count = self.get_channel_data()["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.get_channel_data(), indent=2, ensure_ascii=False))

    def get_channel_data(self) -> dict:
        """
        Возвращаем данные о канале
        """
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @property
    def channel_id(self):
        """
        Возвращаем переданный Айди каналла
        """
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Возвращаем класс ютуб
        """
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    def to_json(self, filename) -> None:
        channel_dict = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriberCount,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, "w") as file:
            json.dump(channel_dict, file)

    def __str__(self):
        return f'{self.title} {self.url}'

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __eq__(self, other):
        return self.subscriberCount == other.subscriberCount

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        return self.subscriberCount >= other.subscriberCount

