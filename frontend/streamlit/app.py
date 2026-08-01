import os
import streamlit as st
import requests

API_BASE_URL = os.getenv("OPENSTREAM_API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="OpenStream", page_icon="🎥", layout="wide")
st.title("OpenStream")
st.caption("A transparent, creator-first video experience")

if "videos" not in st.session_state:
    st.session_state.videos = []

@st.cache_data(ttl=15)
def fetch_feed():
    response = requests.get(f"{API_BASE_URL}/feed", timeout=10)
    response.raise_for_status()
    payload = response.json()
    return payload.get("results", [])

try:
    videos = fetch_feed()
    st.session_state.videos = videos
except Exception as exc:
    st.error(f"Unable to connect to the API at {API_BASE_URL}: {exc}")
    videos = st.session_state.videos

if videos:
    cols = st.columns(3)
    for index, video in enumerate(videos):
        with cols[index % 3]:
            st.subheader(video.get("title", "Untitled"))
            st.write(video.get("description") or "No description")
            if video.get("thumbnail_url"):
                st.image(video["thumbnail_url"], use_container_width=True)
            st.caption(f"Channel: {video.get('channel', {}).get('name', 'Unknown')}")
            st.caption(f"Views: {video.get('view_count', 0)} • Likes: {video.get('like_count', 0)}")
            if video.get("video_url"):
                st.link_button("Open video", video["video_url"])
else:
    st.info("No videos are available yet. Start the backend and seed content to populate the feed.")
