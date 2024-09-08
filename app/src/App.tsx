import React from 'react';
import { Grid } from '@mui/material';
import CustomToolbar from './components/Toolbar';
import LeftPanel from './components/LeftPanel';
import RightPanel from './components/RightPanel';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    // mode: 'dark', // Set the theme to dark mode
    primary: {
      main: '#ef6c00', // This is the orange color
    },
    secondary: {
      main: '#ffffff', // This is the red color
    },
  },
  
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <>
        <div className='background'></div>
        <CustomToolbar />
        <Grid container className="main-container">
          <Grid item xs={7.5}>
            <LeftPanel />
          </Grid>
          <Grid item xs={4.5}>
            <RightPanel />
          </Grid>
        </Grid>
      </>
    </ThemeProvider>
  );
}

export default App;
