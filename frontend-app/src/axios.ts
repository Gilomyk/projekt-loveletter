import axios from 'axios';

// Konfiguracja Axios
axios.defaults.baseURL = 'http://localhost:8000/api';  // Podstawowy URL API
axios.defaults.withCredentials = true;  // Umożliwia wysyłanie ciasteczek

export default axios;