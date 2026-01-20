# ✅ Hugging Face Deployment Checklist

Print karein ya save karke follow karein!

---

## 🅰️ BACKEND DEPLOYMENT

### Space Setup
- [ ] HuggingFace per login karein
- [ ] "New Space" click karein
- [ ] Space name: `taskflow-api`
- [ ] SDK: `Docker`
- [ ] Hardware: `CPU basic`
- [ ] "Create Space" click karein

### Files to Upload (Backend)
- [ ] **Dockerfile**: Copy from `huggingface/backend-Dockerfile`
- [ ] **README.md**: Copy from `huggingface/backend-README.md`
- [ ] **main.py**: From `backend/main.py`
- [ ] **database.py**: From `backend/database.py`
- [ ] **auth.py**: From `backend/auth.py`
- [ ] **requirements.txt**: From `backend/requirements.txt`
- [ ] **models/**: Upload entire folder from `backend/models/`
  - [ ] `__init__.py`
  - [ ] `user.py`
  - [ ] `task.py`

### Environment Variables (Backend)
- [ ] DATABASE_URL (Neon/Supabase se lein)
- [ ] JWT_SECRET (Generate: openssl rand -hex 32)
- [ ] JWT_ALGORITHM = HS256
- [ ] JWT_EXPIRATION_MINUTES = 15
- [ ] JWT_REFRESH_EXPIRATION_DAYS = 7
- [ ] CORS_ORIGINS = https://your-frontend-space.hf.space

### Test Backend
- [ ] Logs tab check karein (build successful?)
- [ ] URL note kar lijiye: https://____-taskflow-api.hf.space
- [ ] Test: https://____-taskflow-api.hf.space/docs (Swagger UI)

---

## 🅱️ FRONTEND DEPLOYMENT

### Space Setup
- [ ] "New Space" click karein
- [ ] Space name: `taskflow-app`
- [ ] SDK: `Docker`
- [ ] Hardware: `CPU basic`
- [ ] "Create Space" click karein

### Files to Upload (Frontend)
- [ ] **Dockerfile**: Copy from `huggingface/Dockerfile`
- [ ] **README.md**: Copy from `huggingface/README.md`
- [ ] **next.config.js**: From `frontend/next.config.js` (updated)
- [ ] **package.json**: From `frontend/package.json`
- [ ] **package-lock.json**: From `frontend/package-lock.json`
- [ ] **tailwind.config.ts**: From `frontend/tailwind.config.ts`
- [ ] **tsconfig.json**: From `frontend/tsconfig.json`
- [ ] **app/**: Upload entire folder from `frontend/app/`
- [ ] **components/**: Upload entire folder from `frontend/components/`
- [ ] **lib/**: Upload entire folder from `frontend/lib/`
- [ ] **public/**: Upload entire folder from `frontend/public/`

### Environment Variables (Frontend)
- [ ] NEXT_PUBLIC_API_URL = https://____-taskflow-api.hf.space (backend URL)
- [ ] NEXT_PUBLIC_APP_URL = https://____-taskflow-app.hf.space (apna URL)
- [ ] NODE_ENV = production

### Update Backend CORS
- [ ] Backend Space mein jaen
- [ ] Settings → Variables
- [ ] CORS_ORIGINS update karein: https://____-taskflow-app.hf.space
- [ ] Save karein

### Test Frontend
- [ ] Logs tab check karein (build successful?)
- [ ] URL open karein: https://____-taskflow-app.hf.space
- [ ] Landing page load ho raha hai?
- [ ] Login page test karein
- [ ] Signup test karein
- [ ] Task creation test karein

---

## 🎯 FINAL VERIFICATION

### Backend Test
- [ ] https://____-taskflow-api.hf.space/health → 200 OK
- [ ] https://____-taskflow-api.hf.space/docs → Swagger UI visible
- [ ] POST /api/v1/auth/signup working
- [ ] POST /api/v1/auth/login working

### Frontend Test
- [ ] Landing page loads
- [ ] Login/Signup pages accessible
- [ ] User can signup
- [ ] User can login
- [ ] Tasks visible
- [ ] Create task working
- [ ] Edit task working
- [ ] Delete task working
- [ ] Filters working

---

## 📝 YOUR URLs (Fill These)

```
Backend URL: ____________________________________________

Frontend URL: ____________________________________________

Database URL: ____________________________________________

JWT Secret: ____________________________________________
```

---

## 🆘 TROUBLESHOOTING

### Build Fail?
- [ ] Check Logs tab for errors
- [ ] Verify all files uploaded
- [ ] Check Dockerfile path
- [ ] Environment variables correct?

### API Error?
- [ ] Backend URL correct?
- [ ] NEXT_PUBLIC_API_URL set?
- [ ] CORS_ORIGINS includes frontend URL?
- [ ] Backend is running?

### Database Error?
- [ ] DATABASE_URL correct?
- [ ] SSL mode enabled?
- [ ] Database is accessible?

---

## 🎉 ALL DONE!

Congratulations! 🎊

Apka TaskFlow ab Hugging Face per live hai!

Share your app:
- Backend: https://____-taskflow-api.hf.space
- Frontend: https://____-taskflow-app.hf.space

---

## 📚 FILES LOCATION REFERENCE

```
Project Folder: C:\Users\SheZziiii SaM\Hackathone2\

Backend Files:
  huggingface/backend-Dockerfile    → Copy to Backend Space as "Dockerfile"
  huggingface/backend-README.md     → Copy to Backend Space as "README.md"
  backend/main.py                   → Upload as "main.py"
  backend/database.py               → Upload as "database.py"
  backend/auth.py                   → Upload as "auth.py"
  backend/requirements.txt          → Upload as "requirements.txt"
  backend/models/                   → Upload entire folder

Frontend Files:
  huggingface/Dockerfile            → Copy to Frontend Space as "Dockerfile"
  huggingface/README.md             → Copy to Frontend Space as "README.md"
  frontend/next.config.js           → Upload as "next.config.js"
  frontend/package.json             → Upload as "package.json"
  frontend/app/                     → Upload entire folder
  frontend/components/              → Upload entire folder
  frontend/lib/                     → Upload entire folder
  frontend/public/                  → Upload entire folder
```

---

**Print this checklist and tick items as you complete them! ✅**
