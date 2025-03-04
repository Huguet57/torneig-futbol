import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { theme } from './theme';
import { store } from './store';
import { AppLayout } from './components/layout/AppLayout';

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <AppLayout>
            <Routes>
              <Route path="/" element={<Navigate to="/tournaments" replace />} />
              <Route path="/tournaments" element={<div>Tournaments</div>} />
              <Route path="/matches" element={<div>Matches</div>} />
              <Route path="/teams" element={<div>Teams</div>} />
              <Route path="/stats" element={<div>Stats</div>} />
            </Routes>
          </AppLayout>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App; 