import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

function FeedScreen() {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    api.get('/feed/feed').then((response) => {
      setVideos(response.data.results || []);
    }).catch(() => {
      setVideos([]);
    });
  }, []);

  return (
    <div>
      <h2>Discover videos</h2>
      <div className="video-grid">
        {videos.map((video) => (
          <div className="card video-card" key={video.id}>
            <img src={video.thumbnail_url || 'https://placehold.co/320x180'} alt={video.title} />
            <h3><Link to={`/videos/${video.id}`}>{video.title}</Link></h3>
            <p>{video.description}</p>
            <small>{video.channel?.name}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FeedScreen;
