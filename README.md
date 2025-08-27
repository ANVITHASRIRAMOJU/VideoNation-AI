# 🎬 VideoNation AI

VideoNation AI is an AI-powered text-to-video platform that transforms text prompts into engaging video content using advanced AI models like **FAL AI** and **Gemini AI**. It’s secure, fast, and designed for creators, marketers, and AI enthusiasts.

---

## 🚀 Features

- Generate videos directly from text prompts  
- AI-enhanced outputs with FAL AI and Gemini AI  
- Secure API key handling via `.env`  
- Interactive, responsive frontend built with HTML, CSS & JS  
- User authentication with Login/Signup system  
- MongoDB for encrypted user data storage  
- Modular architecture for adding multiple AI services  
- Asynchronous processing for faster video generation  

---

## ⚙ How It Works

1. **User Input**: Text is entered on the frontend  
2. **Backend Request**: Sent to FastAPI backend  
3. **FAL AI Adapter**: Generates initial video  
4. **Gemini AI**: Optional prompt refinement for quality enhancement  
5. **Secure Handling**: API keys are read from environment variables  
6. **User Authentication**: Signup/Login data is securely stored in MongoDB  
7. **Video Delivery**: Video is returned for download or preview  

---

## 💻 Tech Stack

- **Backend**: Python, FastAPI, asyncio  
- **Frontend**: HTML, CSS, JavaScript  
- **AI Services**: FAL AI, Gemini AI  
- **Database**: MongoDB (encrypted storage for user data)  
- **Security**: dotenv for environment variables  
- **Utilities**: uuid for unique file names  

---

## 🔐 Security

- **API Keys**: FAL AI and Gemini AI keys stored securely in `.env`  
- **User Data**: Login/Signup information stored in MongoDB with encryption  
- **No Hard-coded Secrets**: All sensitive information is kept out of source code  
- **Session Protection**: Authentication ensures only authorized users can access AI video generation  

---

## ⚡ Quick Start

### Clone Repo
```bash
git clone https://github.com/yourusername/videonation-ai.git
cd videonation-ai
```

### Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Update .env File
```env
FAL_KEY=your_fal_ai_key
GEMINI_KEY=your_gemini_ai_key
MONGODB_URI=your_mongodb_connection_string
DB_NAME=your_database_name
```

### Run Project
```bash
uvicorn main:app --reload
```

### Open in Browser
```
http://127.0.0.1:8000
```

### Use Platform
1. Signup/Login to create a secure account  
2. Enter text prompts to generate videos  
3. Download or preview your AI-generated video  

---

## 📸 Screenshots

<img width="684" height="279" alt="0" src="https://github.com/user-attachments/assets/a3f2d2fd-1e14-44bd-82f9-8d14a8ce46f7" />

<img width="1904" height="858" alt="1" src="https://github.com/user-attachments/assets/c00af591-d300-468f-bd7c-0b28aa404805" />

<img width="1919" height="857" alt="2" src="https://github.com/user-attachments/assets/08f4cd79-b0ce-4446-be97-95d0661bd54e" />
<img width="1919" height="865" alt="3" src="https://github.com/user-attachments/assets/cc27e330-7eab-498d-b2ee-41e3997cc51e" />

<img width="1426" height="264" alt="4" src="https://github.com/user-attachments/assets/2f18bab4-05d8-488a-a463-cda2dd410aa3" />

<img width="1336" height="276" alt="5" src="https://github.com/user-attachments/assets/12f299c3-54c3-4697-aaa6-29f9ec54f79e" />
<img width="716" height="676" alt="6" src="https://github.com/user-attachments/assets/826cfd95-a1fc-484f-a502-b572f3bfffb9" />

---
