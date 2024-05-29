import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [image, setImage] = useState(null);
    const [guess, setGuess] = useState("");
    const [score, setScore] = useState(0);
    const [hintUsed, setHintUsed] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log("Fetching random image...");
        fetchRandomImage();
    }, []);

    const fetchRandomImage = () => {
        setLoading(true);
        fetch("/api/random-image")
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                console.log("Image data received:", data);
                setImage(data);
                setLoading(false); // Set loading to false once the image is loaded
            })
            .catch(error => {
                console.error('Error fetching the image:', error);
                setLoading(false); // Set loading to false even if there's an error
            });
    };

    const handleGuess = () => {
        if (!image) {
            alert("No image loaded yet");
            return;
        }

        fetch("/api/guess", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user: "defaultUser", guess: guess, song_id: image.song_id })
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                if (data.correct) {
                    setScore(data.score);
                    setImage({ url: data.new_image_url, song_id: data.new_song_id });
                    setGuess(""); // Clear the guess input
                } else {
                    alert("Incorrect! Try again.");
                }
            })
            .catch(error => console.error('Error making a guess:', error));
    };

    const handleHint = () => {
        if (!image) {
            alert("No image loaded yet");
            return;
        }

        if (!hintUsed) {
            fetch("/api/hint", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ song_id: image.song_id })
            })
                .then(res => {
                    if (!res.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return res.json();
                })
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    setImage(data);
                    setHintUsed(true);
                })
                .catch(error => console.error('Error fetching the hint:', error));
        } else {
            alert("Hint already used for this image.");
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    image && <img src={image.url} alt="Guess the song" />
                )}
                <input
                    type="text"
                    value={guess}
                    onChange={(e) => setGuess(e.target.value)}
                    placeholder="Guess the song"
                />
                <button onClick={handleGuess}>Submit Guess</button>
                <button onClick={handleHint}>Hint</button>
                <p>Score: {score}</p>
            </header>
        </div>
    );
}

export default App;
