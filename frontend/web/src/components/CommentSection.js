import React, { useState } from 'react';

function CommentSection({ videoId }) {
  const [comments, setComments] = useState([
    { id: 1, content: 'This looks promising!', author_id: 1 }
  ]);
  const [draft, setDraft] = useState('');

  const submitComment = (event) => {
    event.preventDefault();
    if (!draft.trim()) return;
    setComments([...comments, { id: Date.now(), content: draft, author_id: 1 }]);
    setDraft('');
  };

  return (
    <div className="card">
      <h3>Comments</h3>
      <form onSubmit={submitComment}>
        <textarea value={draft} onChange={(e) => setDraft(e.target.value)} placeholder="Write a comment" />
        <button type="submit">Post</button>
      </form>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>{comment.content}</li>
        ))}
      </ul>
    </div>
  );
}

export default CommentSection;
