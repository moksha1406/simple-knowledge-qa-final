# Frontend Setup & Usage Guide

## 🎨 Beautiful UI with HTML, CSS, and JavaScript

Your project now has a **professional, modern web interface**!

---

## 🚀 How to Use

### Option 1: Open Directly in Browser (Simplest)

1. **Make sure your backend is running**:
   ```bash
   python app.py
   ```

2. **Open the frontend**:
   - Navigate to `frontend` folder
   - Double-click `index.html`
   - It will open in your default browser!

3. **Start using**:
   - Upload documents
   - Ask questions
   - Get AI-powered answers!

---

### Option 2: Run with Python HTTP Server (Better for Testing)

1. **Start backend** (Terminal 1):
   ```bash
   python app.py
   ```

2. **Start frontend** (Terminal 2):
   ```bash
   cd frontend
   python -m http.server 3000
   ```

3. **Open browser**:
   - Go to: `http://localhost:3000`

---

### Option 3: Using VS Code Live Server

1. **Install "Live Server" extension** in VS Code

2. **Right-click on `index.html`**

3. **Select "Open with Live Server"**

4. **Browser will auto-open**!

---

## 📖 Features

### ✅ Upload Documents
- **Drag & drop** `.txt` files
- Or **click to browse** and select
- See upload progress
- Get confirmation when done

### ✅ View Documents
- See all uploaded files
- File sizes displayed
- **Delete** documents with one click

### ✅ Ask Questions
- Type your question in the text area
- Click "Ask Question"
- Get **AI-generated answers** using Gemini
- See **source document** and **similarity score**
- View **which mode** was used (Gemini or retrieval)

### ✅ System Status
- Check backend health
- Verify Gemini is connected
- See vector store stats
- Refresh status anytime

---

## 🎨 UI Features

### Beautiful Design
- ✅ Modern gradient background
- ✅ Smooth animations
- ✅ Responsive layout (works on mobile!)
- ✅ Toast notifications
- ✅ Loading indicators
- ✅ Hover effects

### User Experience
- ✅ Drag & drop file upload
- ✅ Real-time status updates
- ✅ Clear error messages
- ✅ One-click actions
- ✅ Auto-scroll to answers
- ✅ Collapsible sections

---

## 🔧 Configuration

### Change API URL (for Production)

Edit `script.js`, line 2:

```javascript
// For local development
const API_URL = 'http://localhost:8000';

// For production (after deploying backend to Render)
const API_URL = 'https://your-backend-app.onrender.com';
```

**Important**: Remove the trailing slash!

---

## 📱 Responsive Design

Works perfectly on:
- ✅ Desktop (1920×1080 and above)
- ✅ Laptop (1366×768)
- ✅ Tablet (768×1024)
- ✅ Mobile (375×667)

---

## 🎯 Deployment Options

### Option 1: Deploy Frontend to Vercel (FREE)

1. **Create account** at [vercel.com](https://vercel.com)

2. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

4. **Update API URL** in `script.js`:
   ```javascript
   const API_URL = 'https://your-backend.onrender.com';
   ```

5. **Your frontend is live**!

### Option 2: Deploy to Netlify (FREE)

1. **Create account** at [netlify.com](https://netlify.com)

2. **Drag and drop** the `frontend` folder

3. **Done**! Your site is live.

4. **Update API URL** in settings or in `script.js`

### Option 3: Deploy to GitHub Pages (FREE)

1. **Create GitHub repo**

2. **Push frontend folder**:
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/repo.git
   git push -u origin main
   ```

3. **Enable GitHub Pages** in repo settings

4. **Your site** is at: `https://username.github.io/repo`

---

## 🔒 CORS Configuration

Your backend (`app.py`) already has CORS enabled:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This means your frontend can connect from **any domain**!

**For production**, you might want to restrict this:

```python
allow_origins=[
    "https://your-frontend.vercel.app",
    "http://localhost:3000"
],
```

---

## 🐛 Troubleshooting

### "Network error" when uploading/asking

**Fix**:
1. Make sure backend is running: `python app.py`
2. Check API_URL in `script.js` is correct
3. Check browser console (F12) for errors

### Upload works but questions fail

**Fix**:
1. Make sure you set `GEMINI_API_KEY` in `.env`
2. Restart backend after adding API key
3. Check `/status` endpoint shows Gemini as "healthy"

### Frontend shows but doesn't connect

**Fix**:
1. Check CORS is enabled in backend
2. Make sure API_URL doesn't have trailing slash
3. Try opening browser console (F12) to see errors

### "File not found" when opening index.html

**Fix**:
1. Make sure all 3 files are in same folder:
   - `index.html`
   - `style.css`
   - `script.js`
2. Don't move files to different folders

---

## 🎨 Customization

### Change Colors

Edit `style.css`, line 10-20:

```css
:root {
    --primary: #6366f1;  /* Main color */
    --primary-dark: #4f46e5;
    --success: #10b981;  /* Success color */
    --danger: #ef4444;   /* Error color */
}
```

### Change Font

Edit `style.css`, line 23:

```css
body {
    font-family: 'Your Font', sans-serif;
}
```

### Change Background

Edit `style.css`, line 25:

```css
body {
    background: linear-gradient(135deg, #your-color 0%, #your-color2 100%);
}
```

---

## 📂 File Structure

```
frontend/
├── index.html    # Main HTML structure
├── style.css     # All styling
└── script.js     # All functionality
```

**That's it!** Just 3 files, no build process, no npm packages!

---

## ✨ Features Showcase

### 1. Upload
- Drag & drop support
- Instant feedback
- Progress indicators

### 2. Documents List
- Auto-refreshes
- Shows file sizes
- One-click delete
- Smooth animations

### 3. Q&A Interface
- Large text area for questions
- Loading animation while processing
- Beautiful answer display
- Source attribution
- Similarity scores

### 4. System Status
- Collapsible section
- Real-time health checks
- Component-level status
- Refresh button

---

## 🚀 Quick Start Checklist

- [ ] Backend is running (`python app.py`)
- [ ] Gemini API key is set in `.env`
- [ ] Open `frontend/index.html` in browser
- [ ] See "System Online" in header
- [ ] Upload a test document
- [ ] Ask a test question
- [ ] Get AI-powered answer!

---

## 🎯 Pro Tips

1. **Use Chrome DevTools** (F12) to debug issues
2. **Check Network tab** to see API calls
3. **Keep backend terminal open** to see logs
4. **Test on mobile** by opening on your phone
5. **Customize colors** to match your brand

---

## 📱 Mobile Experience

The UI is fully responsive:
- Navigation collapses on small screens
- Touch-friendly buttons
- Optimized text sizes
- Smooth scrolling
- No horizontal scroll

---

## 🌟 What Makes This Frontend Great?

✅ **No build process** - Just open and use!
✅ **No dependencies** - Pure HTML/CSS/JS
✅ **Modern design** - Looks professional
✅ **Fully responsive** - Works on all devices
✅ **Easy to customize** - Change colors/fonts easily
✅ **Production-ready** - Deploy anywhere
✅ **Fast** - Loads instantly
✅ **Accessible** - Works with screen readers

---

Enjoy your beautiful new UI! 🎨✨
