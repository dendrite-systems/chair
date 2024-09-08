import React from 'react';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { AppBar, IconButton, Toolbar, Typography } from '@mui/material';

const CustomToolbar: React.FC = () => {
  return (
    <AppBar position="static"
        sx={{
            padding: '10px 20px',
        }}
        color='primary'
    >
        <Toolbar>
            <IconButton edge="start" color="secondary" aria-label="menu" sx={{ mr: 2 }}>
            <SmartToyIcon />
            </IconButton>
            <Typography variant="h5" color="secondary" component="div">
            Find Your Chair
            </Typography>
        </Toolbar>
    </AppBar>
  );
}

export default CustomToolbar;
