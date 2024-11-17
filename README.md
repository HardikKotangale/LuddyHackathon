# LuddyHackathon Project

This project is part of the LuddyHackathon and utilizes Firebase to manage real-time data. Follow the steps below to set up and run the project locally.

## Prerequisites

Ensure you have the following installed on your system:
- **Python** (version 3.8 or above recommended)
- **pip** (Python package manager)
- **Virtual environment tool** (optional but recommended)
- **Firebase credentials** and necessary services configured

## Project Structure
```
LuddyHackathon/
├── app/
│   └── __pycache__/
├── apis/
│   ├── __pycache__/
│   ├── contact_api.c
│   └── contact_api.py
├── static/
│   ├── scripts.js
│   └── styles.css
├── templates/
│   └── index.html
├── __init__.py
├── models.py
├── routes.py
├── utils.py
├── .gitignore
├── config.py
├── firebase_credentials.json
├── firebase_credentials.json.example
├── Procfile
├── README.md
├── requirements.txt
└── run.py
```

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone <repository_url>
cd LuddyHackathon
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Firebase Configuration
1. Create a Firebase project in the Firebase Console
2. Download your Firebase service account key
3. Rename `firebase_credentials.json.example` to `firebase_credentials.json`
4. Replace the contents with your Firebase credentials
5. Update `config.py` with your Firebase configurations

## Project Components

### Backend
- `run.py`: Application entry point
- `config.py`: Configuration settings
- `models.py`: Data models and database schema
- `routes.py`: API endpoints and route handlers
- `utils.py`: Utility functions and helpers

### API Layer
- `apis/contact_api.py`: Contact management API endpoints
- `apis/contact_api.c`: C-language implementations (if applicable)

### Frontend
- `templates/index.html`: Main application template
- `static/scripts.js`: Frontend JavaScript code
- `static/styles.css`: CSS styling

## Running the Application

1. Ensure your virtual environment is activated
2. Run the application:
```bash
python run.py
```
3. Access the application at `http://localhost:5000`

## Development

### Adding New Features
1. Create new routes in `routes.py`
2. Add corresponding models in `models.py`
3. Implement API endpoints in the `apis` directory
4. Update frontend components as needed

### Testing
- Unit tests can be added to test API endpoints
- Ensure Firebase emulators are used for testing

## Deployment

The project includes a `Procfile` for Heroku deployment. To deploy:

1. Create a Heroku account
2. Install Heroku CLI
3. Login to Heroku:
```bash
heroku login
```
4. Create a new Heroku app:
```bash
heroku create your-app-name
```
5. Push to Heroku:
```bash
git push heroku main
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Environment Variables
Create a `.env` file in the root directory with the following variables:
```
FIREBASE_DATABASE_URL=your_database_url
FLASK_ENV=development
FLASK_APP=run.py
```

## License
[Add your license information here]

## Support
For support or questions, please contact the hackathon organizers or create an issue in the repository.

## Acknowledgments
- LuddyHackathon organizers
- Firebase team for the real-time database
- All contributors and participants
