import React, { useState } from 'react';
import axios from 'axios';

function UploadScreen() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus('Uploading...');
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    const fileInput = document.getElementById('video_file');
    formData.append('video_file', fileInput.files[0]);

    try {
      await axios.post('http://localhost:8000/videos/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus('Upload complete');
    } catch (error) {
      setStatus('Upload failed');
    }
  };

  return (
    <div className="card">
      <h2>Upload a video</h2>
      <form onSubmit={handleSubmit}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" />
        <input id="video_file" type="file" accept="video/*" />
        <button type="submit">Upload</button>
      </form>
      <p>{status}</p>
    </div>
  );
}

export default UploadScreen;
