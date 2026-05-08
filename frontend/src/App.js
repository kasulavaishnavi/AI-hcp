import { useState } from "react";

import { useSelector, useDispatch } from "react-redux";

import { updateForm, resetForm } from "./redux/formSlice";

import "./App.css";

function App() {
  const formData = useSelector((state) => state.form);

  const dispatch = useDispatch();

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: message,
      },
    ]);

    try {
      const res = await fetch("https://ai-hcp.onrender.com/agent", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message,
        }),
      });

      // Parse response
      const data = await res.json();

      // LangGraph response handling
      const response = data.result || data;

      console.log("Backend Response:", response);

      //  Redux form update
      if (response?.data) {
        dispatch(updateForm(response.data));
      }

      //  Default AI text
      let aiText = `Tool used: ${response.tool}`;

      //  Assistant prompt
      if (response.assistant_message) {
        aiText += `\n${response.assistant_message}`;
      }

      // Summary tool
      if (response.tool === "summarize_interaction") {
        aiText = "Tool used: summarize_interaction";

        if (response.summary) {
          aiText += `\n${response.summary}`;
        }
      }

      // Follow-up tool
      if (response.tool === "suggest_followup") {
        aiText = "Tool used: suggest_followup";
      }

      // Reset tool
      if (response.tool === "reset") {
        aiText = "Tool used: reset\nForm reset successfully.";

        dispatch(resetForm());
      }

      // Submit tool
      if (response.tool === "submit_interaction") {
        aiText =
          "Tool used: submit_interaction\nInteraction submitted successfully.";

        dispatch(resetForm());
      }

      // Add AI message
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: aiText,
        },
      ]);

      setMessage("");
    } catch (err) {
      console.error("FETCH ERROR:", err);
    }
  };

  return (
    <div className="container">
      {/* LEFT FORM */}

      <div className="form-section">
        <h1>Log HCP Interaction</h1>

        <div className="form-group">
          <label>HCP Name</label>
          <input value={formData.name} readOnly />
        </div>

        <div className="row">
          <div className="form-group">
            <label>Date</label>
            <input value={formData.date} readOnly />
          </div>

          <div className="form-group">
            <label>Time</label>
            <input value={formData.time} readOnly />
          </div>
        </div>

        <div className="form-group">
          <label>Attendees</label>
          <input value={formData.attendees} readOnly />
        </div>

        <div className="form-group">
          <label>Topics Discussed</label>
          <textarea value={formData.topics} readOnly />
        </div>

        <div className="form-group">
          <label>Materials Shared</label>
          <input value={formData.materials} readOnly />
        </div>

        <div className="form-group">
          <label>Samples Distributed</label>
          <input value={formData.samples} readOnly />
        </div>

        <div className="form-group">
          <label>Observed/Inferred HCP Sentiment</label>

          <div className="sentiment-options">
            <label>
              <input
                type="radio"
                checked={formData.sentiment === "positive"}
                readOnly
              />
              😊 Positive
            </label>

            <label>
              <input
                type="radio"
                checked={formData.sentiment === "neutral"}
                readOnly
              />
              😐 Neutral
            </label>

            <label>
              <input
                type="radio"
                checked={formData.sentiment === "negative"}
                readOnly
              />
              😟 Negative
            </label>
          </div>
        </div>

        <div className="form-group">
          <label>Outcomes</label>
          <textarea value={formData.outcomes} readOnly />
        </div>

        <div className="form-group">
          <label>Follow-up Actions</label>
          <textarea value={formData.followup} readOnly />
        </div>
      </div>

      {/* RIGHT CHAT */}

      <div className="chat-section">
        <h2>🤖 AI Assistant</h2>

        <div className="chat-messages">
          <div className="ai-card intro">
            Log interaction details here using natural language.
          </div>

          {messages.map((msg, index) => (
            <div
              key={index}
              className={msg.role === "user" ? "user-message" : "ai-message"}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="chat-input">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe interaction..."
          />

          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
