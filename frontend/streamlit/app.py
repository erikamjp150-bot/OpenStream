import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_BASE_URL = os.getenv("OPENSTREAM_API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="OpenStream", page_icon="🎥", layout="wide")
st.title("OpenStream")
st.caption("A transparent, creator-first video experience")

if "videos" not in st.session_state:
    st.session_state.videos = []


@st.cache_data(ttl=60)
def fetch_videos():
    response = requests.get(f"{API_BASE_URL}/videos", timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=60)
def get_signed_play_url(video_id):
    response = requests.get(f"{API_BASE_URL}/videos/{video_id}/play-url", timeout=10)
    response.raise_for_status()
    payload = response.json()
    return payload.get("url")


def render_thumbnail(thumbnail_url):
    if not thumbnail_url:
        return None

    if thumbnail_url.startswith("http://") or thumbnail_url.startswith("https://"):
        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            image_bytes = response.content
            image = Image.open(BytesIO(image_bytes))
            image.load()
            return image
        except Exception:
            return None

    try:
        image = Image.open(thumbnail_url)
        image.load()
        return image
    except Exception:
        return None


try:
    videos = fetch_videos()
    st.session_state.videos = videos
except Exception as exc:
    st.error(f"Unable to connect to the API at {API_BASE_URL}: {exc}")
    videos = st.session_state.videos

if videos:
    cols = st.columns(3)
    for index, video in enumerate(videos):
        with cols[index % 3]:
            st.subheader(video.get("title", "Untitled"))
            thumbnail = render_thumbnail(video.get("thumbnail_url"))
            if thumbnail is not None:
                st.image(thumbnail, use_container_width=True)
            else:
                st.info("Thumbnail unavailable")
            if st.button(f"Play {video.get('title', 'video')}", key=f"play-{video.get('id')}"):
                signed_url = get_signed_play_url(video.get("id"))
                st.video(signed_url)
            st.caption(f"ID: {video.get('id')}")
else:
    st.info("No videos are available yet. Start the backend and seed content to populate the feed.")
