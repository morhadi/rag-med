# 🚀 Quick Start Guide

## Step 1: Install Pandoc (Required for RTF support)

### Windows:
1. Download from: https://github.com/jgm/pandoc/releases/latest
2. Run the installer
3. Verify: Open CMD and run `pandoc --version`

### Mac:
```bash
brew install pandoc
```

### Linux:
```bash
sudo apt-get install pandoc
```

## Step 2: Set Up Backend

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file:
```bash
copy .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

## Step 3: Set Up Frontend

```bash
cd ..\frontend
pip install -r requirements.txt
```

## Step 4: Run the Application

### Terminal 1 (Backend):
```bash
cd backend
uvicorn main:app --reload
```

### Terminal 2 (Frontend):
```bash
cd frontend
streamlit run app.py
```

## Step 5: Open Your Browser

Frontend: http://localhost:8501

## 🎉 You're Ready!

1. Upload documents using the sidebar
2. Click "Process Documents"
3. Start asking questions!

## Need Help?

- API docs: http://localhost:8000/docs
- Check backend logs in Terminal 1
- Check frontend logs in Terminal 2
