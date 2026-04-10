# 🌍 TravelPlanner: Modern Adventure Orchestrator

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white)](https://www.framer.com/motion/)

TravelPlanner is a high-end, interactive web application designed for modern explorers. Featuring a premium **Glassmorphic UI**, vibrant mesh gradients, and smooth Framer Motion animations, it provides a seamless experience for discovering destinations and crafting detailed travel itineraries.

---

## ✨ Key Features

- 💎 **Premium Glassmorphic UI**: A stunning, lightweight design system with backdrop blurs and mesh gradients.
- 🗺️ **Destination Discovery**: Explore 100+ curated locations with real-time filtering (Country, Price, Rating).
- 📅 **Interactive Itineraries**: build day-by-day schedules with cost tracking and activity notes.
- ❤️ **Social Favorites**: Save your dream locations to a personal "Favorites" collection.
- ⭐ **Experience Reviews**: Read and share community-driven tales and ratings.
- 📱 **Fully Responsive**: Optimized for mobile, tablet, and desktop viewing.
- 🏗️ **Production Ready**: Configured with environment variables, WhiteNoise static serving, and database scalability.

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 4.2.7
- **Frontend**: Tailwind CSS (CDN), React (Components), Framer Motion (Animations)
- **Data Generation**: Faker (Demo data), Requests (Image fetching)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Lokesh19-PP/Travel-Planner-Webapp.git
cd Travel-Planner-Webapp
```

### 2. Set Up Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

_Modify `.env` with your secret keys and local settings._

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python manage.py migrate
```

### 5. Generate Demo Data (100+ Destinations & Images)

```bash
python manage.py populate_db
```

### 6. Run the Adventure

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to start exploring!

---

## ☁️ Deployment

### 🚀 Deploying on Render (Recommended)
1. **Create a Web Service**: Link your GitHub repository.
2. **Environment**: Select `Python` as the runtime.
3. **Build Command**: `./build.sh`
4. **Start Command**: `gunicorn travel_planner.wsgi`
5. **Environment Variables**: Add all keys from `.env.example`.

---

## 🔧 Management Commands

- `python manage.py populate_db`: Clears existing data and downloads 100+ fresh destinations with high-quality travel images.
- `python manage.py collectstatic`: Prepares all assets for production serving.

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Designed with ❤️ for travelers by travelers.
