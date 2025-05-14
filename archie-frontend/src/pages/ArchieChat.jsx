import { useState } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, SendHorizonal } from 'lucide-react';

export default function ArchieChat() {
  const [messages, setMessages] = useState([
    { role: 'archie', text: 'Hi Vijay 👋 I'm ready. Just tell me what to do.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;
    const userMessage = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('https://archie-bridge.onrender.com/parse_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();
      const archieReply = {
        role: 'archie',
        text: data.reply || '✅ Command executed, Vijay.'
      };

      setMessages((prev) => [...prev, archieReply]);

      if (data.action === 'create_sheet' && data.title) {
        const sheetRes = await fetch('https://archie-bridge.onrender.com/create_sheet', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: data.title })
        });

        const sheetData = await sheetRes.json();
        if (sheetData.status === 'success') {
          setMessages((prev) => [
            ...prev,
            {
              role: 'archie',
              text: `📄 Sheet created: [${data.title}](${sheetData.sheet_url})`
            }
          ]);
        } else {
          setMessages((prev) => [
            ...prev,
            { role: 'archie', text: `⚠️ Sheet creation failed: ${sheetData.message}` }
          ]);
        }
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'archie', text: '⚠️ Something went wrong, jaan.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold text-center">Archie 💬</h1>
      <Card className="h-[450px] overflow-hidden border shadow-xl rounded-2xl">
        <CardContent className="p-4 h-full">
          <ScrollArea className="h-full pr-2 space-y-3">
            {messages.map((msg, idx) => (
              <div key={idx} className={`p-3 rounded-xl w-fit whitespace-pre-line ${msg.role === 'user' ? 'ml-auto bg-blue-100' : 'bg-gray-100'}`}>
                {msg.text}
              </div>
            ))}
          </ScrollArea>
        </CardContent>
      </Card>
      <div className="flex items-center gap-2">
        <Input
          placeholder="Type your command, Vijay..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <Button onClick={handleSend} disabled={loading}>
          {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <SendHorizonal className="w-4 h-4" />}
        </Button>
      </div>
    </div>
  );
}
