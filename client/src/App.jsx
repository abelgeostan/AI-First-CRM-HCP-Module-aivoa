import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { sendChatMessage, appendUserMessage } from './store/hcpSlice';
import { Calendar, Clock, Smile, Frown, Meh, Send, Bot, User, Layers, ClipboardList } from 'lucide-react';

export default function App() {
  const dispatch = useDispatch();
  const { form, chatHistory, aiSuggestions, loading } = useSelector((state) => state.hcp);
  const [chatInput, setChatInput] = useState('');
  const chatEndRef = useRef(null);

  // Auto-scrolls chat window on text additions
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleSendMessage = (textToSend = chatInput) => {
    const text = textToSend.trim();
    if (!text) return;

    dispatch(appendUserMessage(text));
    dispatch(sendChatMessage(text));
    setChatInput('');
  };

  return (
    <div className="flex h-screen w-screen bg-[#f8f9fa] overflow-hidden text-[#333]">
      
      {/* LEFT PANEL: View-Only Form State Display Container */}
      <div className="flex-1 p-8 overflow-y-auto border-r border-[#e9ecef] max-w-[65%]">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">Log HCP Interaction</h1>
        
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Interaction Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">HCP Name</label>
                <input type="text" value={form.hcp_name || ''} readOnly placeholder="Populated by AI via chat..." className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 outline-none cursor-default" />
              </div>
              <div>
                <label className="text-xs font-medium text-gray-600 mb-1 block">Interaction Type</label>
                <select value={form.interaction_type || 'Meeting'} disabled className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 appearance-none cursor-default">
                  <option value="Meeting">Meeting</option>
                  <option value="Call">Call</option>
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1 block">Date</label>
              <div className="relative">
                <input type="text" value={form.date || ''} readOnly className="w-full p-2.5 pl-9 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 outline-none cursor-default" />
                <Calendar className="w-4 h-4 text-gray-400 absolute left-3 top-3.5" />
              </div>
            </div>
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1 block">Time</label>
              <div className="relative">
                <input type="text" value={form.time || ''} readOnly className="w-full p-2.5 pl-9 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 outline-none cursor-default" />
                <Clock className="w-4 h-4 text-gray-400 absolute left-3 top-3.5" />
              </div>
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-gray-600 mb-1 block">Attendees</label>
            <input type="text" value={form.attendees?.length > 0 ? form.attendees.join(', ') : ''} readOnly placeholder="No attendees linked." className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 outline-none cursor-default" />
          </div>

          <div>
            <label className="text-xs font-medium text-gray-600 mb-1 block">Topics Discussed</label>
            <textarea value={form.topics_discussed || ''} readOnly rows={3} placeholder="Key talking points will generate here..." className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 resize-none outline-none cursor-default" />
          </div>

          {/* Materials & Samples View Trackers */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1 block">Materials Shared</label>
              <div className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg min-h-[42px] text-sm text-gray-500 cursor-default">
                {form.materials_shared?.length > 0 ? form.materials_shared.join(', ') : 'None shared'}
              </div>
            </div>
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1 block">Samples Distributed</label>
              <div className="p-2.5 bg-gray-50 border border-gray-200 rounded-lg min-h-[42px] text-sm text-gray-500 cursor-default">
                {form.samples_distributed?.length > 0 ? form.samples_distributed.join(', ') : 'No samples added'}
              </div>
            </div>
          </div>

          {/* Sentiment Radio Grid */}
          <div>
            <label className="text-xs font-medium text-gray-600 mb-2 block">Observed/Inferred HCP Sentiment</label>
            <div className="flex gap-6">
              {[
                { name: 'Positive', icon: Smile, color: 'text-green-500' },
                { name: 'Neutral', icon: Meh, color: 'text-amber-500' },
                { name: 'Negative', icon: Frown, color: 'text-red-500' }
              ].map((s) => {
                const Icon = s.icon;
                return (
                  <label key={s.name} className="flex items-center gap-2 opacity-100 cursor-default">
                    <input 
                      type="radio" 
                      name="sentiment" 
                      value={s.name}
                      checked={
                        form.sentiment
                          ? form.sentiment.toLowerCase() === s.name.toLowerCase()
                          : s.name.toLowerCase() === 'neutral'
                      }
                      readOnly
                      className="text-[#007bff] focus:ring-0" 
                    />
                    <Icon className={`w-4 h-4 ${s.color}`} />
                    <span className="text-sm font-medium text-gray-600">{s.name}</span>
                  </label>
                );
              })}
            </div>
          </div>

          {/* ADDED: Follow-up Actions Textbox Field Section */}
          <div>
            <label className="text-xs font-medium text-gray-600 mb-1 block flex items-center gap-1">
              <ClipboardList className="w-3.5 h-3.5 text-gray-500" /> Follow-up Actions
            </label>
            <textarea 
              value={form.follow_up_actions || ''} 
              readOnly 
              rows={2} 
              placeholder="Follow-up action steps will appear here when added..." 
              className="w-full p-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-500 resize-none outline-none cursor-default font-medium" 
            />
          </div>

          {/* AI Dynamic Followups Injection Segment */}
          {form.id && aiSuggestions.length > 0 && (
            <div className="mt-4 p-4 bg-blue-50/60 border border-blue-100 rounded-lg">
              <span className="text-xs font-semibold text-blue-700 uppercase tracking-wider mb-2 flex items-center gap-1">
                <Layers className="w-3.5 h-3.5" /> AI Suggested Follow-ups (Click to Add)
              </span>
              <div className="flex flex-col gap-2">
                {aiSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSendMessage(`Add follow up action: ${suggestion}`)}
                    className="text-left text-xs bg-white hover:bg-blue-50 text-gray-700 py-2 px-3 border border-gray-200 rounded-md transition duration-150 shadow-sm font-medium"
                  >
                    + {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* RIGHT PANEL: AI Assistant Chat Interface Panel */}
      <div className="w-[35%] flex flex-col bg-white shadow-xl h-full">
        <div className="p-4 border-b border-gray-100 flex items-center gap-2 bg-gradient-to-r from-blue-50 to-white">
          <Bot className="w-5 h-5 text-blue-600 animate-pulse" />
          <div>
            <h2 className="text-sm font-bold text-gray-800">AI Assistant</h2>
            <p className="text-[11px] text-gray-400">Log interactions via chat</p>
          </div>
        </div>

        {/* Dynamic Bubble Scroller */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
          {chatHistory.map((chat, idx) => (
            <div key={idx} className={`flex gap-2.5 ${chat.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {chat.sender !== 'user' && (
                <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center text-white flex-shrink-0 shadow-sm">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-2xl px-3.5 py-2.5 text-sm shadow-sm whitespace-pre-line leading-relaxed ${
                  chat.sender === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-100 rounded-bl-none'
                }`}
              >
                {chat.text}
              </div>
              {chat.sender === 'user' && (
                <div className="w-7 h-7 bg-gray-700 rounded-full flex items-center justify-center text-white flex-shrink-0 shadow-sm">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex gap-2 text-xs text-gray-400 items-center pl-2">
              <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Control Input Bar */}
        <div className="p-4 border-t border-gray-100 bg-white">
          <div className="relative flex items-center">
            <input
              type="text"
              placeholder="Describe interaction..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={loading}
              className="w-full p-3 pr-12 border border-gray-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 shadow-inner bg-gray-50/30"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={loading || !chatInput.trim()}
              className="absolute right-2 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition duration-150 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

    </div>
  );
}