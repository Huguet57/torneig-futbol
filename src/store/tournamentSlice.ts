import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface Tournament {
  id: number;
  name: string;
  startDate: string;
  endDate: string;
  description?: string;
}

interface TournamentState {
  tournaments: Tournament[];
  loading: boolean;
  error: string | null;
}

const initialState: TournamentState = {
  tournaments: [],
  loading: false,
  error: null,
};

export const fetchTournaments = createAsyncThunk(
  'tournaments/fetchAll',
  async () => {
    const response = await axios.get('/api/tournaments/');
    return response.data;
  }
);

export const tournamentSlice = createSlice({
  name: 'tournaments',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTournaments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTournaments.fulfilled, (state, action) => {
        state.loading = false;
        state.tournaments = action.payload;
      })
      .addCase(fetchTournaments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch tournaments';
      });
  },
});

export default tournamentSlice.reducer; 