import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Generates a consistent random thread ID for LangGraph Memory Saver tracking
const THREAD_ID = `thread_${Math.random().toString(36).substring(7)}`;

export const sendChatMessage = createAsyncThunk(
  'hcp/sendChatMessage',
  async (messageText, { getState }) => {
    const { hcp } = getState();
    const response = await axios.post('http://localhost:8000/api/chat', {
      message: messageText,
      thread_id: THREAD_ID,
      current_log_id: hcp.form.id || null
    });
    return response.data;
  }
);

const initialState = {
  form: {
    id: null,
    hcp_name: '',
    interaction_type: 'Meeting',
    date: '19-04-2025',
    time: '19:36',
    attendees: [],
    topics_discussed: '',
    materials_shared: [],
    samples_distributed: [],
    sentiment: 'Neutral',
    outcomes: '',
    follow_up_actions: ''
  },
  chatHistory: [
    { sender: 'ai', text: 'Log interaction details here via chat (e.g., "Met Dr. Smith, discussed Prodo-X efficacy...") or ask for help.' }
  ],
  aiSuggestions: [],
  loading: false
};

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    appendUserMessage: (state, action) => {
      state.chatHistory.push({ sender: 'user', text: action.payload });
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state) => {
        state.loading = true;
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.loading = false;
        // Update response text
        if (action.payload.reply) {
          state.chatHistory.push({ sender: 'ai', text: action.payload.reply });
        }
        // Sync layout forms
        if (action.payload.form_state && Object.keys(action.payload.form_state).length > 0) {
          state.form = { ...state.form, ...action.payload.form_state };
        } else if (action.payload.reply?.includes('soft-deleted')) {
          // Reset if deleted
          state.form = initialState.form;
        }
        // Push suggestion pills
        state.aiSuggestions = action.payload.ai_suggestions || [];
      })
      .addCase(sendChatMessage.rejected, (state) => {
        state.loading = false;
        state.chatHistory.push({ sender: 'ai', text: 'Connection error. Check backend execution loops.' });
      });
  }
});

export const { appendUserMessage } = hcpSlice.actions;
export default hcpSlice.reducer;