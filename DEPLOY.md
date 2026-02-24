# ReloPlan — Deployment Guide

## Option 1 — Streamlit Community Cloud (Free, Recommended)

Fastest way to go live. Free hosting, auto-deploys from GitHub.

### Steps

1. **Push to GitHub**
   ```bash
   cd ReloPlan
   git init
   git add .
   git commit -m "initial commit"
   # Create a repo at github.com, then:
   git remote add origin https://github.com/YOUR_USERNAME/reloplan.git
   git push -u origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **New app**
   - Select your repo → branch: `main` → file: `app.py`
   - Click **Deploy**

3. **Done** — your app is live at `https://YOUR_APP.streamlit.app`

---

## Option 2 — Railway (Free tier, custom domain)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. Deploy:
   ```bash
   cd ReloPlan
   railway init
   railway up
   ```

3. Set port variable in Railway dashboard:
   ```
   PORT = 8501
   ```

4. Get your live URL from the Railway dashboard.

---

## Option 3 — Render (Free tier)

1. Push to GitHub (same as Option 1, Step 1)
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Click **Deploy**

---

## Option 4 — Docker (VPS / any cloud)

### Build & run locally
```bash
cd ReloPlan
docker build -t reloplan .
docker run -p 8501:8501 reloplan
```

### Deploy to any VPS (Ubuntu)
```bash
# On your VPS
sudo apt update && sudo apt install -y docker.io

# Clone or copy your project
git clone https://github.com/YOUR_USERNAME/reloplan.git
cd reloplan

# Build and run
docker build -t reloplan .
docker run -d -p 80:8501 --restart always --name reloplan reloplan
```

App is now accessible at `http://YOUR_VPS_IP`

---

## Pre-Deploy Checklist

- [ ] Update `WA_NUMBER` in `app.py` with your real WhatsApp number
- [ ] Change `admin123` password in `app.py` to something strong
- [ ] Test the form end-to-end locally before pushing
- [ ] Confirm `requirements.txt` is up to date

## Files Overview

```
ReloPlan/
├── app.py                 # Main app
├── requirements.txt       # Dependencies
├── Dockerfile             # For Docker/VPS deployment
├── .streamlit/
│   └── config.toml        # Theme and server config
└── .gitignore
```
