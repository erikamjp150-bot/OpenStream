import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import CommentSection from '../components/CommentSection';

function VideoPlayerScreen() {
  const { id } = useParams();
  const [video, setVideo] = useState(null);

  useEffect(() => {
    api.get(`/videos/${id}`).then((response) => {
      setVideo(response.data);
    }).catch(() => setVideo(null));
  }, [id]);

  if (!video) return <div className="card">Loading...</div>;

  return (
    <div className="card">
      <h2>{video.title}</h2>
      <p>{video.description}</p>
      <video controls width="100%" poster={video.thumbnail_url}>
        <source src={video.video_url} type="video/mp4" />
      </video>
      <CommentSection videoId={video.id} />
    </div>
  );
}

export default VideoPlayerScreen;
