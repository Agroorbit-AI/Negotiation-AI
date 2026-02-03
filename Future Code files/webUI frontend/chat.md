<!DOCTYPE html>
<html>
<head>
  <title>AI Negotiation</title>
  <style>
    body { font-family: Arial; margin: 40px; }
    #chat { border: 1px solid #ccc; padding: 20px; height: 300px; overflow-y: scroll; }
    input { width: 80%; padding: 8px; }
    button { padding: 8px; }
  </style>
</head>
<body>

<h2>AI Negotiation Platform</h2>

<div id="chat"></div><br>

<input id="msg" placeholder="Type your message..." />
<button onclick="sendMessage()">Send</button>

<script>
  // TEMP: hardcoded session for now
  const sessionId = "test-session-001";

  async function sendMessage() {
    const input = document.getElementById("msg");
    const text = input.value;
    input.value = "";

    document.getElementById("chat").innerHTML +=
      `<p><b>You:</b> ${text}</p>`;

    const res = await fetch("http://localhost:8000/messages", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        session_id: sessionId,
        message: text
      })
    });

    const data = await res.json();

    document.getElementById("chat").innerHTML +=
      `<p><b>AI:</b> ${data.ai_response}</p>`;
  }
</script>

</body>
</html>
