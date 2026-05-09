# Business Idea Generator

An AI-powered SaaS application that generates business ideas for AI agents using real-time streaming and beautiful Markdown rendering.

## Features

- 🚀 **Next.js 14+ App Router** with TypeScript
- 🤖 **FastAPI Backend** with Python
- 📡 **Real-time Streaming** using Server-Sent Events
- 🎨 **Beautiful UI** with Tailwind CSS and gradients
- 📝 **Markdown Rendering** with syntax highlighting
- ☁️ **Vercel Deployment** ready
- 🌓 **Dark Mode** support

## Tech Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI**: Groq API (Mixtral model)
- **Deployment**: Vercel
- **Styling**: Tailwind CSS v4 with Typography plugin

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Groq API key

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.local` and add your `GROQ_API_KEY`

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

### Deployment

Deploy to Vercel:

```bash
vercel --prod
```

## Project Structure

```
saas/
├── api/
│   └── index.py          # FastAPI backend with streaming
├── app/
│   ├── _page.tsx         # Main page component
│   ├── layout.tsx        # App layout
│   └── globals.css       # Global styles
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
└── package.json         # Node.js dependencies
```

## API Endpoints

- `GET /api` - Stream AI-generated business ideas

## Environment Variables

- `GROQ_API_KEY` - Your Groq API key

## Learn More

This project is based on the MLOps Week 1 tutorial, combining:
- FastAPI for the Python backend
- Next.js App Router for the React frontend
- Real-time streaming with Server-Sent Events
- Professional UI with Tailwind CSS

## Deploy on Vercel

The project is configured for seamless Vercel deployment with both Next.js frontend and Python backend.
