import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO = Path("output/funny_minseol.mp4")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"필수 환경변수 {name} 가 없습니다.")
    return value


def upload():
    if not VIDEO.exists():
        raise FileNotFoundError(f"업로드할 영상이 없습니다: {VIDEO}")

    credentials = Credentials(
        token=None,
        refresh_token=required_env("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=required_env("YOUTUBE_CLIENT_ID"),
        client_secret=required_env("YOUTUBE_CLIENT_SECRET"),
        scopes=SCOPES,
    )

    youtube = build("youtube", "v3", credentials=credentials)

    title = os.getenv("YOUTUBE_TITLE", "웃긴민설 오늘의 한마디 😂 #shorts")
    description = os.getenv(
        "YOUTUBE_DESCRIPTION",
        "AI 캐릭터 웃긴민설의 짧은 한마디!\n\n#웃긴민설 #쇼츠 #shorts #AI"
    )

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": "23",
        },
        "status": {
            "privacyStatus": os.getenv("YOUTUBE_PRIVACY_STATUS", "public"),
            "selfDeclaredMadeForKids": False,
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(VIDEO), chunksize=-1, resumable=True),
    )

    response = request.execute()
    print(f"유튜브 업로드 완료: https://youtu.be/{response['id']}")


if __name__ == "__main__":
    upload()
