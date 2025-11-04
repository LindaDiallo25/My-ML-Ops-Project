# Plant Classification WebApp 🌼🌱

Beautiful React frontend for the Dandelion vs Grass ML classifier.

## Features

✨ **Modern UI/UX**
- Drag & drop image upload
- Real-time classification with loading states
- Animated results with confidence scores
- Responsive design (mobile & desktop)
- Beautiful gradient backgrounds

🔌 **API Integration**
- Connects to FastAPI backend (`/api/predict`)
- Automatic fallback to mock data if API unavailable
- Error handling and user feedback

🎨 **Tech Stack**
- React 18 + TypeScript
- Vite for fast development
- TailwindCSS for styling
- Framer Motion for animations
- Lucide React for icons

## Quick Start

### Development Mode

```bash
# Install dependencies
npm install

# Start dev server (requires API running on port 8000)
npm run dev

# Open http://localhost:5173
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### With Docker Compose (Recommended)

```bash
# From project root
cd ..
docker-compose up --build

# Frontend: http://localhost:3000
# API: http://localhost:8000
```

## API Configuration

The frontend automatically detects the environment:
- **Development**: Calls `http://localhost:8000/predict` directly
- **Production**: Uses `/api/predict` (proxied by nginx)

## Usage

1. **Upload Image**: Click upload area or drag & drop (JPG, PNG, GIF)
2. **View Results**: Classification label + confidence percentage
3. **Actions**: Upload Another or Reclassify

## Project Structure

```
Front/
├── src/
│   ├── App.tsx              # Main application with API integration
│   ├── main.tsx             # Entry point
│   ├── index.css            # Global styles + Tailwind
│   └── components/          # Reusable UI components
├── Dockerfile               # Production nginx build
├── nginx.conf               # Reverse proxy config
└── package.json
```

---

**Built with ❤️ using React + Vite + TailwindCSS**