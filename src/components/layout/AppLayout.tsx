import { Box, Container } from '@mui/material';
import { MobileNav } from './MobileNav';

interface AppLayoutProps {
  children: React.ReactNode;
}

export const AppLayout = ({ children }: AppLayoutProps) => {
  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: 'background.default',
      paddingBottom: '56px' // Height of the bottom navigation
    }}>
      <Container maxWidth="lg" sx={{ py: 2 }}>
        {children}
      </Container>
      <MobileNav />
    </Box>
  );
}; 