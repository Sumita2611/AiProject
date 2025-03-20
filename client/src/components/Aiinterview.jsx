import React, { useState } from "react";
import axios from "axios";

const Aiinterview = () => {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [score, setScore] = useState(null);

    // Fetch question from backend
    const getQuestion = async () => {
        try {
            const response = await axios.get("http://localhost:5000/api/question");
            setQuestion(response.data.question);
            setAnswer("");
            setScore(null);
        } catch (error) {
            console.error("Error fetching question:", error);
        }
    };

    // Submit answer and get feedback
    const submitAnswer = async () => {
        try {
            const response = await axios.post("http://localhost:5000/api/evaluate", {
                question,
                answer,
            });
            setScore(response.data.score);
        } catch (error) {
            console.error("Error evaluating answer:", error);
        }
    };

    return (
        <div>
            <h2>AI Interviewer</h2>
            <button onClick={getQuestion}>Start Interview</button>

            {question && (
                <>
                    <p><strong>Question:</strong> {question}</p>
                    <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Your answer..."></textarea>
                    <button onClick={submitAnswer}>Submit Answer</button>
                </>
            )}

            {score && <h3>Your Score: {score} / 100</h3>}
        </div>
    );
};

export default Aiinterview;
