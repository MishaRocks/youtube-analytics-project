from src.channel import Channel


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_title: str = self.get_video_data()['items'][0]['snippet']['title']
        self.view_count: int = self.get_video_data()['items'][0]['statistics']['viewCount']
        self.like_count: int = self.get_video_data()['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.get_video_data()['items'][0]['statistics']['commentCount']

    def get_video_data(self):
        youtube = Channel.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.video_id).execute()
        return video_response

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

