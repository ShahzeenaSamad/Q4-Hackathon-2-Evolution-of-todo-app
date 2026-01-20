# 🚀 Hugging Face Deployment - Simple Step-by-Step Guide

TaskFlow ko Hugging Face per deploy karne ke liye ye simple steps follow karein.

---

## 📋 Overall Process:

**2 Spaces banane hain:**
1. **Backend API** (FastAPI) - Pehle isay deploy karein
2. **Frontend App** (Next.js) - Baad mein isay deploy karein

---

## 🎯 STEP 1: Backend Space Deploy Karein

### 1.1 Hugging Face per Space Create Karein

1. Browser mein karein: https://huggingface.co
2. Login karein (ya account banayein)
3. Top right mein **"New Space"** click karein
4. Form bharein:
   - **Owner**: Apna username select karein
   - **Space name**: `taskflow-api` (ya jo naam chahein)
   - **License**: `MIT` select karein
   - **SDK**: `Docker` select karein (IMPORTANT!)
   - **Hardware**: `CPU basic` (free tier)
5. **"Create Space"** click karein

### 1.2 Files Upload Karein

Hugging Face Space khulne ke baad, ye files upload karein:

#### File 1: Dockerfile
```
Copy karne ke liye file: C:\Users\SheZziiii SaM\Hackathone2\huggingface\backend-Dockerfile
Iska naam change karke: Dockerfile
```

**Steps:**
1. `huggingface/backend-Dockerfile` file open karein
2. Saara content copy karein
3. Hugging Face Space mein **"Files"** tab pe jayein
4. **"+"** button click karein → **"New file"**
5. File name: `Dockerfile`
6. Paste content
7. **"Commit new file to main"** click karein

#### File 2: README.md
```
Copy karne ke liye file: C:\Users\SheZziiii SaM\Hackathone2\huggingface\backend-README.md
Iska naam change karke: README.md
```

**Steps:**
1. Pehle wale `README.md` ko delete karein (Hugging Face ne banaya hoga)
2. `huggingface/backend-README.md` file open karein
3. Saara content copy karein
4. New file banayein naam: `README.md`
5. Paste content
6. **"Commit"** click karein

#### File 3: Backend Code Files

**Ye sab files upload karein backend/ folder se:**

```
backend/main.py
backend/models/__init__.py
backend/models/user.py
backend/models/task.py
backend/auth.py
backend/database.py
backend/requirements.txt
```

**Easy way - GitHub se:**
1. Hugging Face Space mein **"Files"** tab pe jayein
2. Scroll down to **"Git LFS"** or **"Upload files"**
3. Ya direct GitHub se files copy-paste kar sakti hain

**Manual upload:**
1. Har file ke liye:
   - **"+"** → **"New file"**
   - Path: `main.py` (agar backend/ hai to `backend/main.py`)
   - Content paste karein
   - **"Commit"** click karein

### 1.3 Environment Variables Set Karein

1. Hugging Face Space mein **"Settings"** tab pe jayein
2. **"Variables"** section mein jaen
3. **"New variable"** click karein
4. Ye variables add karein:

```
Variable 1:
Name: DATABASE_URL
Value: postgresql://user:password@host:port/database?sslmode=require
(Use your real database URL here - Neon/Supabase se lein)

Variable 2:
Name: JWT_SECRET
Value: your-super-secret-key-here
(Generate karein: https://randomkeygen.com/ ya `openssl rand -hex 32`)

Variable 3:
Name: JWT_ALGORITHM
Value: HS256

Variable 4:
Name: JWT_EXPIRATION_MINUTES
Value: 15

Variable 5:
Name: JWT_REFRESH_EXPIRATION_DAYS
Value: 7

Variable 6:
Name: CORS_ORIGINS
Value: https://your-frontend-space.hf.space
(Baad mein frontend ka URL yahan update karenge)
```

### 1.4 Deploy Check Karein

- **"Logs"** tab mein jaen
- Build process dekhen
- Jab green checkmark aye, success!
- URL note kar lijiye: `https://your-username-taskflow-api.hf.space`

**Test karein:**
```
https://your-username-taskflow-api.hf.space/docs
```
Swagger UI open hona chahiye!

---

## 🎨 STEP 2: Frontend Space Deploy Karein

### 2.1 New Space Create Karein

1. Hugging Face pe **"New Space"** click karein
2. Form bharein:
   - **Space name**: `taskflow-app` (ya jo naam chahein)
   - **SDK**: `Docker` select karein
   - **Hardware**: `CPU basic`

### 2.2 Files Upload Karein

#### File 1: Dockerfile
```
Copy from: huggingface/Dockerfile
Save as: Dockerfile
```

#### File 2: README.md
```
Copy from: huggingface/README.md
Save as: README.md
(Pehle wale README ko delete karke)
```

#### File 3: Frontend Code

**Ye folders/files upload karein:**
```
frontend/app/
frontend/components/
frontend/lib/
frontend/public/
frontend/package.json
frontend/package-lock.json
frontend/next.config.js (updated wala)
frontend/tailwind.config.ts
frontend/tsconfig.json
```

### 2.3 Environment Variables Set Karein

**Settings** → **Variables** mein ye add karein:

```
Variable 1:
Name: NEXT_PUBLIC_API_URL
Value: https://your-username-taskflow-api.hf.space
(Step 1 mein jo backend URL mila use yahan paste karein)

Variable 2:
Name: NEXT_PUBLIC_APP_URL
Value: https://your-username-taskflow-app.hf.space
(Apna frontend URL yahan)

Variable 3:
Name: NODE_ENV
Value: production
```

**IMPORTANT:** Backend Space ko update karein:
- Backend Space mein jaen
- `CORS_ORIGINS` variable update karein
- Value: `https://your-username-taskflow-app.hf.space` (frontend ka URL)

### 2.4 Deploy Check Karein

- **"Logs"** tab check karein
- Build complete hone ka intezaar karein
- Frontend URL check karein

---

## ✅ STEP 3: Final Testing

### Test Backend:
```
https://your-username-taskflow-api.hf.space/docs
```
- Swagger UI open hona chahiye
- `/health` endpoint test karein

### Test Frontend:
```
https://your-username-taskflow-app.hf.space
```
- Landing page open hona chahiye
- Login page pe jaen
- Signup test karein
- Task create test karein

---

## 📁 File Locations (Quick Reference):

```
huggingface/
├── backend-Dockerfile       → Backend Space mein: Dockerfile
├── backend-README.md        → Backend Space mein: README.md
├── Dockerfile               → Frontend Space mein: Dockerfile
├── README.md                → Frontend Space mein: README.md
└── DEPLOYMENT_GUIDE.md      → Detailed guide (padhne ke liye)

frontend/
├── next.config.js           → Updated with `output: 'standalone'`
├── .dockerignore            → Ignore file (optional)
└── (all other files)        → Upload to Frontend Space

backend/
├── (all files)              → Upload to Backend Space
└── .dockerignore            → Ignore file (optional)
```

---

## 🔧 Common Issues & Solutions:

### Issue 1: Build Fail Ho Raha Hai
**Solution:**
- Dockerfile check karein saare files hain ya nahi
- requirements.txt mein saari dependencies hain
- Environment variables sahi set hain

### Issue 2: API Connection Error
**Solution:**
- NEXT_PUBLIC_API_URL check karein
- Backend URL sahi hai ya nahi
- CORS settings check karein backend mein

### Issue 3: Database Error
**Solution:**
- DATABASE_URL sahi hai
- SSL mode enabled hai
- Database accessible hai (check locally)

---

## 🎉 Success Checklist:

- [ ] Backend Space created
- [ ] Backend files uploaded
- [ ] Backend environment variables set
- [ ] Backend deployed successfully
- [ ] Frontend Space created
- [ ] Frontend files uploaded
- [ ] Frontend environment variables set
- [ ] Frontend deployed successfully
- [ ] Backend CORS updated with frontend URL
- [ ] Full app tested end-to-end

---

## 📝 Pro Tips:

1. **Pehle Backend deploy karein** - Frontend ko backend URL chahiye
2. **Logs tab check karte raho** - Build status dekhne ke liye
3. **Environment variables double check karo** - Koi typo nahi
4. **Public space banana** - Private spaces mein limits hoti hain
5. **Free tier use karo** - Shuru mein CPU basic sufficient hai

---

## 🆘 Help Needed?

Agar koi issue aaye:
1. **Logs tab** check karein - Error message dikhega
2. **Settings** verify karein - Variables sahi hain
3. **Files** check karein - Saari files upload hain
4. **GitHub issues** - Repository mein check karein

---

**Good luck! 🚀**

Apni beautiful TaskFlow app jald hi Hugging Face per live hogi!
