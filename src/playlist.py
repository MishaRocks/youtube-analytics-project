import datetime

import isodate

from src.channel import Channel


class PlayList:
    youtube = Channel.get_service()

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.title: str = self.get_title
        self.url: str = "https://www.youtube.com/playlist?list=" + self.pl_id

    def get_video_ids(self) -> list:
        """
        Возвращаем все id видео в листе
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    def get_duration(self) -> list:
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.get_video_ids())
                                                    ).execute()
        duration_list = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
        return duration_list

    @property
    def total_duration(self) -> str:
        """
        Преобразуем длительность в нужный формат
        """
        total_duration = sum(self.get_duration(), datetime.timedelta())
        return total_duration

    def show_best_video(self) -> str:
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.get_video_ids())
                                                    ).execute()
        likes = 0
        best_video = None
        for video in video_response['items']:
            if int(video["statistics"]["likeCount"]) > likes:
                likes = int(video["statistics"]["likeCount"])
                best_video = 'https://youtu.be/'+video['id']
        return best_video

    @property
    def get_title(self):
        """
        Получаем заголовок плейлиста
        """
        for i in self.get_playlists()['items']:
            if self.pl_id == i['id']:
                title = i['snippet']['title']
                return title

    def get_playlists(self):
        """
        Список плейлистов
        """
        channel_id = self.get_playlist_data()['items'][0]['snippet']['channelId']
        playlists = self.youtube.playlists().list(channelId=channel_id,
                                             part='contentDetails,snippet', maxResults=50,).execute()
        return playlists

    def get_playlist_data(self):
        """
        Данные по роликам в плейлисте
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                       part='contentDetails, snippet', maxResults=50,).execute()
        return playlist_videos
