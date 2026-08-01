import React, { useEffect, useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import FeedScreen from './screens/FeedScreen';
import VideoPlayerScreen from './screens/VideoPlayerScreen';
import ChannelScreen from './screens/ChannelScreen';
import UploadScreen from './screens/UploadScreen';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('openstream_user');
    if (storedUser) setUser(JSON.parse(storedUser));
  }, []);

  return (
    <div className="app-shell">
      <nav className="nav">
        <Link to="/">Feed</Link>
        <Link to="/channels/1">Channel</Link>
        <Link to="/upload">Upload</Link>
        {user ? <span>Welcome, {user.username}</span> : <Link to="/login">Login</Link>}
      </nav>
      <Routes>
        <Route path="/" element={<FeedScreen />} />
        <Route path="/videos/:id" element={<VideoPlayerScreen />} />
        <Route path="/channels/:id" element={<ChannelScreen />} />
        <Route path="/upload" element={<UploadScreen />} />
        <Route path="/login" element={<LoginScreen />} />
        <Route path="/register" element={<RegisterScreen />} />
      </Routes>
    </div>
  );
}

export default App;
