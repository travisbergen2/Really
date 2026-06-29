"use client";

import { useState } from "react";

export default function ChatPanel({
  text,
  onTextChange
}: {
  text: string;
  onTextChange: (t: string) => void;
}) {
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleRoute() {
    setLoading(true);
    try {
      const res = await fetch("/api/route", {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: { "Content-Type": "application/json" }
      });
      const json = await res.json();
      setResponse(`${json.model}: ${json.output}`);
    } catch (error) {
      setResponse("Error connecting to API");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border rounded p-4 bg-white shadow-sm">
      <textarea
        value={text}
        onChange={e => onTextChange(e.target.value)}
        className="w-full border p-2 rounded h-32"
        placeholder="Say something in human language…"
      />
      <button 
        onClick={handleRoute} 
        disabled={loading}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Routing..." : "Route"}
      </button>
      {response && (
        <div className="mt-4 p-3 bg-gray-100 rounded border">
          <h3 className="text-sm font-semibold text-gray-500 uppercase">Response</h3>
          <pre className="mt-1 whitespace-pre-wrap">{response}</pre>
        </div>
      )}
    </div>
  );
}
