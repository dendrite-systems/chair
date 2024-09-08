import React, { useContext } from 'react';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import { AppBar, IconButton, Toolbar, Typography } from '@mui/material';
import { ScriptsContext } from '../ScriptsContext';

const CustomToolbar: React.FC = () => {

  const context = useContext(ScriptsContext);
  if (!context) {
    return <div>Context not found</div>;
  }

  const { scripts, loading, error, reload, chooseCurScript } = context;

  return (
    <AppBar position="static"
        sx={{
            padding: '10px 20px',
        }}
        color='primary'
    >
        <Toolbar>
            <IconButton edge="start" color="secondary" aria-label="menu" sx={{ mr: 2 }}
              onClick={()=>{chooseCurScript(-1);reload();}}
            >
              <SmartToyIcon />
            </IconButton>
            <Typography variant="h5" color="secondary" component="div"
              onClick={()=>{chooseCurScript(-1);reload();}}
            >
            Find Your Chair
            </Typography>
        </Toolbar>
    </AppBar>
  );
}

export default CustomToolbar;
