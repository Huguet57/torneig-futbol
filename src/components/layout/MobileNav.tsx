import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { BottomNavigation, BottomNavigationAction, Paper } from '@mui/material';
import { SportsSoccer, EmojiEvents, Groups, Assessment } from '@mui/icons-material';

export const MobileNav = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [value, setValue] = useState(() => {
    const path = location.pathname;
    if (path.startsWith('/matches')) return 0;
    if (path.startsWith('/tournaments')) return 1;
    if (path.startsWith('/teams')) return 2;
    if (path.startsWith('/stats')) return 3;
    return 0;
  });

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
    switch (newValue) {
      case 0:
        navigate('/matches');
        break;
      case 1:
        navigate('/tournaments');
        break;
      case 2:
        navigate('/teams');
        break;
      case 3:
        navigate('/stats');
        break;
    }
  };

  return (
    <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
      <BottomNavigation value={value} onChange={handleChange}>
        <BottomNavigationAction
          label="Matches"
          icon={<SportsSoccer />}
        />
        <BottomNavigationAction
          label="Tournaments"
          icon={<EmojiEvents />}
        />
        <BottomNavigationAction
          label="Teams"
          icon={<Groups />}
        />
        <BottomNavigationAction
          label="Stats"
          icon={<Assessment />}
        />
      </BottomNavigation>
    </Paper>
  );
}; 