# Song Guess App

## Setup Instructions

### Backend (Flask)

1. Navigate to the `backend` directory:
   ```sh
   cd backend
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```env
   GENIUS_API_KEY=your_genius_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the Flask application:
   ```sh
   python app.py
   ```

### Frontend (React)

1. Navigate to the `frontend` directory:
   ```sh
   cd ../frontend
   ```

2. Install the dependencies:
   ```sh
   npm install
   ```

3. Start the React application:
   ```sh
   npm start
   ```

The backend server should be running on `http://localhost:5000` and the frontend on `http://localhost:3000`.

## How to Play

- The application will show a random image generated based on a song.
- Enter your guess for the song in the input field and submit.
- Use the hint button to get a hint (limited to one hint per image).
- Your score will be updated based on your correct guesses.
