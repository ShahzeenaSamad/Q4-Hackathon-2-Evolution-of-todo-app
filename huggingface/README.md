---
title: TaskFlow
emoji: 📝
colorFrom: #092635
colorTo: #9EC8B9
sdk: docker
pinned: false
license: mit
---

# TaskFlow - Modern Todo App

A beautiful, feature-rich todo application built with Next.js and FastAPI.

## 🚀 Features

- ✅ Modern, responsive UI with glassmorphism design
- 🔐 JWT-based authentication with automatic token refresh
- 🎯 Task management with priorities, due dates, and categories
- 🔍 Advanced search and filter functionality
- 📊 Productivity statistics and progress tracking
- 🎨 Beautiful animations and smooth transitions

## 🛠️ Tech Stack

- **Frontend**: Next.js 15, React, Tailwind CSS, TypeScript
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT with refresh tokens

## 📦 Deployment

This Space deploys the **frontend** application. Make sure to configure the following environment variables:

### Required Environment Variables

```bash
NEXT_PUBLIC_API_URL=https://your-backend-api.hf.space
```

### Optional Environment Variables

```bash
NEXT_PUBLIC_APP_URL=https://your-space-name.hf.space
NODE_ENV=production
```

## 🌐 Complete Stack Deployment

For full functionality, deploy both:

1. **Backend API**: Deploy the FastAPI backend on a separate Hugging Face Space
2. **Frontend**: This Space connects to your backend API

See setup instructions in the main repository.

## 📝 License

MIT License - see LICENSE file for details
