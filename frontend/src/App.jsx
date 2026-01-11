import { useEffect, useState } from "react";
import "./App.css";

/* ================= ROOT ================= */

export default function App() {
  const [tab, setTab] = useState("generate");

  return (
    <div className="container">
      <h1>AI Wiki Quiz Generator</h1>

      <div className="tabs">
        <button
          className={tab === "generate" ? "active" : ""}
          onClick={() => setTab("generate")}
        >
          Generate Quiz
        </button>
        <button
          className={tab === "history" ? "active" : ""}
          onClick={() => setTab("history")}
        >
          History
        </button>
      </div>

      {tab === "generate" && <GenerateQuiz />}
      {tab === "history" && <History />}
    </div>
  );
}

/* ================= GENERATE QUIZ ================= */

function GenerateQuiz() {
  const [url, setUrl] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateQuiz = async () => {
    if (!url.trim()) {
      alert("Please enter a Wikipedia URL");
      return;
    }

    try {
      setLoading(true);
      setQuizData(null);

      const res = await fetch("http://127.0.0.1:8000/generate-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });

      const json = await res.json();
      setQuizData(json);
    } catch {
      alert("Failed to generate quiz");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <input
        className="url-input"
        placeholder="Paste Wikipedia URL here"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button className="primary" onClick={generateQuiz} disabled={loading}>
        {loading ? "Generating..." : "Generate Quiz"}
      </button>

      {loading && <div className="card">Generating quiz…</div>}

      {quizData && !loading && <QuizDisplay data={quizData} />}
    </>
  );
}

/* ================= QUIZ DISPLAY ================= */

function QuizDisplay({ data }) {
  const questions = data?.quiz?.quiz_questions || [];
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const submitQuiz = () => {
    let s = 0;
    questions.forEach((q, i) => {
      if (answers[i] === q.correct_answer) s++;
    });
    setScore(s);
    setSubmitted(true);
  };

  if (questions.length === 0) {
    return <div className="card">No questions available.</div>;
  }

  return (
    <div className="card">
      <h2>{data.title}</h2>

      {questions.map((q, i) => (
        <div className="question" key={i}>
          <p className="question-header">
            <b>Q{i + 1}.</b> {q.question}
            <span className={`badge ${q.difficulty}`}>
              {q.difficulty.toUpperCase()}
            </span>
          </p>

          {q.options.map((opt, idx) => {
            let cls = "option";
            if (!submitted && answers[i] === opt) cls += " selected";
            if (submitted) {
              if (opt === q.correct_answer) cls += " correct";
              else if (opt === answers[i]) cls += " wrong";
            }

            return (
              <div
                key={idx}
                className={cls}
                onClick={() =>
                  !submitted &&
                  setAnswers((a) => ({ ...a, [i]: opt }))
                }
              >
                <input type="radio" checked={answers[i] === opt} readOnly />
                {opt}
              </div>
            );
          })}

          {submitted && (
            <p className="explanation">
              <b>Explanation:</b> {q.explanation}
            </p>
          )}
        </div>
      ))}

      {!submitted && (
        <button className="primary" onClick={submitQuiz}>
          Submit Quiz
        </button>
      )}

      {submitted && (
        <div className="score">
          Score: {score} / {questions.length}
        </div>
      )}
    </div>
  );
}

/* ================= HISTORY ================= */

function History() {
  const [list, setList] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/quizzes")
      .then((r) => r.json())
      .then(setList);
  }, []);

  return (
    <>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>URL</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map((q) => (
            <tr key={q.id}>
              <td>{q.id}</td>
              <td>{q.title}</td>
              <td className="url-cell">{q.url}</td>
              <td>
                <button
                  className="primary"
                  onClick={() =>
                    setSelected({
                      id: q.id,
                      title: q.title,
                      quiz: q.quiz_data,
                    })
                  }
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selected && (
        <div className="modal-overlay">
          <div className="modal">
            <button
              className="primary"
              onClick={() => setSelected(null)}
            >
              Close
            </button>
            <QuizDisplay data={selected} />
          </div>
        </div>
      )}
    </>
  );
}
