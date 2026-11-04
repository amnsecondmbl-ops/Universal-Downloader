# Universal Media Downloader

A full-stack media downloader supporting Instagram, Facebook, and YouTube using React, Flask, Instaloader, and yt-dlp.

## Features

- Instagram media downloading
- Facebook video downloading
- YouTube downloading
- Instagram multi-post/carousel support
- Preview before download
- Separate preview & download routes
- Fullscreen image preview modal
- Mobile/iPhone compatibility
- Smart loading screen with cold-start detection
- Admin authentication and cleaning system
- Automatic cleanup system
- Environment variable support
- Cloud deployment support (frontend and backend)

---

## Tech Stack

### Frontend
- React
- CSS

### Backend
- Flask
- Instaloader
- yt-dlp
- Flask Sessions
- Flask-CORS
- python-dotenv

### Deployment
- Render (Backend)
- Vercel (Frontend)

---

## Project Structure

```txt
backend/
├── app.py
├── cleanup.py
├── manual_cleanup.py
├── requirements.txt
├── downloaders/
│   ├── instagram.py
│   └── universal.py

frontend/
├── src/
│   └── App.js
├── package.json
```

---

## Installation

### Clone Repository

```bash
git clone YOUR_REPO_LINK
cd universalDownloader
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`

```env
BASE_URL=http://localhost:5000
APP_SECRET_KEY=your_secret_key
ADMIN_PASSWORD=your_password
```

Run backend:

```bash
python app.py
```

---

## Frontend Setup

```bash
cd frontend

npm install
```

Create `.env`

```env
REACT_APP_API_URL=http://localhost:5000
```

Run frontend:

```bash
npm start
```

---

## Environment Variables

### Backend

```env
BASE_URL=
APP_SECRET_KEY=
ADMIN_PASSWORD=
```

### Frontend

```env
REACT_APP_API_URL=
```

---

## Deployment

### Backend
Deployed on Render.

### Frontend
Deployed on Vercel.

---

## Important Notes

- YouTube downloads may occasionally fail on cloud deployments due to platform anti-bot restrictions.
- Render free tier may take time to wake from inactivity.
- Files are stored temporarily and cleaned automatically.

---

## What I Learned

- Full-stack architecture
- Flask API development
- React frontend integration
- Environment variable management
- Render & Vercel deployment
- Session authentication
- Media streaming & downloads
- Mobile/iPhone browser handling
- Production debugging

---
## Future Improvements

- Better YouTube support
- Audio download support
- Download progress tracking
- More platform support
- Improved animations & UI

## License

This project is for educational purposes.
