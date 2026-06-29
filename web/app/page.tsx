"use client";

import { useState } from "react";
import ChatPanel from "../components/ChatPanel";

export default function Page() {
  const [text, setText] = useState("");

  return (
    <div className="space-y-4">
      <p className="text-gray-600">AI-human translation layer and multi-model router.</p>
      <ChatPanel text={text} onTextChange={setText} />
    </div>
  );
}
