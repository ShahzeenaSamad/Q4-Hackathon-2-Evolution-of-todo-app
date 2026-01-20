# 🚀 Hugging Face Spaces Deployment Guide

TaskFlow ko Hugging Face Spaces per deploy karne ke liye ye steps follow karein.

## 📋 Prerequisites

1. **Hugging Face Account**: https://huggingface.co/join
2. **GitHub Repository**: Apna repo ready hona chahiye
3. **Database**: PostgreSQL database (Neon, Supabase, etc.)

## 🎯 Deployment Strategy

TaskFlow ko **2 alag Spaces** per deploy karenge:

### 1️⃣ Backend API Space (FastAPI)
### 2️⃣ Frontend Space (Next.js)

---

## 📦 Step 1: Backend Deployment

### A. New Space Create Karein

1. Hugging Face per login karein: https://huggingface.co
2. **"New Space"** click karein
3. Fill in details:
   - **Owner**: Apna username
   - **Space name**: `taskflow-api` (ya koi bhi naam)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free)

### B. Backend Files Upload Karein

1. **Backend Dockerfile** copy karein:
   - File: `huggingface/backend-Dockerfile`
   - Iska naam `Dockerfile` rakhein

2. **Backend README** copy karein:
   - File: `huggingface/backend-README.md`
   - Iska naam `README.md` rakhein

3. **Backend code** upload karein:
   - `backend/` folder ke saare files
   - `requirements.txt`

### C. Environment Variables Set Karein

Space settings mein ja ke ye variables add karein:

```bash
# Database (Neon/Supabase se lein)
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require

# JWT Secret (generate karein: openssl rand -hex 32)
JWT_SECRET=your-generated-secret-here

# JWT Settings
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7

# CORS (Frontend Space ka URL yahan add karenge baad mein)
CORS_ORIGINS=https://your-frontend-space.hf.space
```

### D. Deploy Check Karein

- Space build hona chahiye
- API documentation check karein: `https://your-space.hf.space/docs`

**Note karein**: Backend Space ka URL copy rakhein, frontend mein use hoga!

---

## 🎨 Step 2: Frontend Deployment

### A. New Space Create Karein

1. **"New Space"** click karein
2. Fill in details:
   - **Space name**: `taskflow-app` (ya koi bhi naam)
   - **SDK**: Docker
   - **Hardware**: CPU basic

### B. Frontend Files Upload Karein

1. **Frontend Dockerfile** copy karein:
   - File: `huggingface/Dockerfile`
   - Iska naam `Dockerfile` rakhein

2. **Frontend README** copy karein:
   - File: `huggingface/README.md`
   - Iska naam `README.md` rakhein

3. **Next.js Config update karein**:
   `frontend/next.config.js` mein ye add karein:

   ```javascript
   module.exports = {
     reactStrictMode: true,
     output: 'standalone', // Add this line
   }
   ```

4. **Frontend code** upload karein:
   - `frontend/` folder ke saare files
   - `package.json`, `package-lock.json`

### C. Environment Variables Set Karein

```bash
# Backend API URL (Step 1 mein jo URL mile use yahan paste karein)
NEXT_PUBLIC_API_URL=https://taskflow-api.hf.space

# Frontend URL
NEXT_PUBLIC_APP_URL=https://taskflow-app.hf.space

# Environment
NODE_ENV=production
```

### D. Deploy!

- Space automatically build hona chahiye
- **"Embed this Space"** se apni app ka URL le sakti hain

---

## ✅ Verification Steps

### 1. Backend Test Karein
```
https://taskflow-api.hf.space/docs
```
- Swagger UI open hona chahiye
- Health check endpoint test karein

### 2. Frontend Test Karein
```
https://taskflow-app.hf.space
```
- Landing page load hona chahiye
- Login/Signup pages test karein
- Task creation test karein

---

## 🔧 Quick Troubleshooting

### Build Fail Ho Raha Hai?
- Dockerfile check karein saari files present hain
- Requirements.txt mein saare dependencies hain
- Environment variables sahi set hain

### API Connection Error?
- Backend URL check karein
- CORS settings verify karein
- Environment variables check karein

### Database Error?
- DATABASE_URL correct hai
- SSL mode enabled hai
- Database accessible hai

---

## 🎉 Success!

Dono Spaces ready hone ke baad:
1. Backend Space URL copy karein
2. Frontend mein NEXT_PUBLIC_API_URL update karein
3. Frontend Space redeploy karein

Apni beautiful TaskFlow app share karein! 🚀

---

## 📚 Useful Links

- Hugging Face Spaces Docs: https://huggingface.co/docs/hub/spaces
- Dockerfile Reference: https://docs.docker.com/engine/reference/builder/
- Next.js Deployment: https://nextjs.org/docs/deployment
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
