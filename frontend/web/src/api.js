import axios from 'axios';

export function getApiBaseUrl() {
  if (typeof window === 'undefined') {
    return 'http://127.0.0.1:8000';
  }

  const { protocol, hostname } = window.location;
  if (hostname.includes('.app.github.dev')) {
    return `${protocol}//${hostname.replace(/-\d+\.app\.github\.dev$/, '-8000.app.github.dev')}`;
  }

  return 'http://127.0.0.1:8000';
}

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || getApiBaseUrl(),
});

export default api;
