import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion() {
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError("Unable to connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  function clearChat() {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  }

  return (
    <div className="container">
      <h1>💬 Finance FAQ Chatbot</h1>

      <textarea
        rows="3"
        placeholder="Ask a consumer banking question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
          }
        }}
      />

      <div className="buttons">
        <button onClick={askQuestion}>Ask Question</button>

        <button onClick={clearChat}>Clear</button>
      </div>

      {loading && (
        <div className="loading">
          🤖 Thinking...
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {answer && (
        <div className="answer">
          <h2>🤖 Answer</h2>

          <p>{answer}</p>

          {sources.length > 0 && (
            <div className="sources">
              <h3>📚 Sources</h3>

              <ul>
                {sources.map((source, index) => (
                  <li key={index}>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {source.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;