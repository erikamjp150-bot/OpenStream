import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function ChannelScreen() {
  const { id } = useParams();
  const [channel, setChannel] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/channels/${id}`).then((response) => {
      setChannel(response.data);
    }).catch(() => setChannel(null));
  }, [id]);

  if (!channel) return <div className="card">Loading...</div>;

  return (
    <div className="card">
      <h2>{channel.name}</h2>
      <p>{channel.description}</p>
      <p>Subscribers: {channel.subscriber_count}</p>
    </div>
  );
}

export default ChannelScreen;
