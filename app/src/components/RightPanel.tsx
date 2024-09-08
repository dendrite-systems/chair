import React, { useContext, useState } from 'react';
import { Box, Typography, Slider, TextField, FormControlLabel, Switch, Button, IconButton } from '@mui/material';

import StartIcon from '@mui/icons-material/PlayArrow'; // Use the icon you need
import RefreshIcon from '@mui/icons-material/Refresh'; // Use the refresh icon

import Codeblock from './CodeBlock'

import axios from 'axios';

import { ScriptsContext } from '../ScriptsContext';

const RightPanel: React.FC = () => {

    const context = useContext(ScriptsContext);
    if (!context) {
      return <div>Context not found</div>;
    }
  
    const { curScript, scripts, loading, error, reload, chooseCurScript, runScript } = context;

    return (
        <Box
            className="right-panel"
            display="flex"
            flexDirection="column"
            justifyContent="flex-start"
            padding="30px 30px 0 30px"
        >
            {
                curScript !== null ? 
                <>
                    <Typography variant="h5" color="secondary" gutterBottom>
                        {curScript.name}
                    </Typography>
                    <Typography variant="body1" color="secondary" gutterBottom>
                        {curScript.description}
                    </Typography>
                    <div className='border-box'
                        style={{
                            width: "100%",
                            height: "2px",
                            margin: "10px 0"
                        }}
                    />
                    <Codeblock code={
                        curScript.script
                    } />
                    <div
                        style={{
                            padding: "20px 10px",
                            display:'flex',
                            flexDirection:'row',
                            justifyContent:'space-between'
                        }}
                    >
                        <Button
                            variant="contained"
                            color="primary"
                            startIcon={<StartIcon />}
                            sx={{
                                width: '47%',
                                backgroundColor: '#ef6c00', // Orange color
                                color: 'white',
                                padding: "20px, 40px",
                                fontSize: '16px',
                                '&:hover': {
                                    backgroundColor: '#ff9800'
                                },
                            }}
                            onClick = {
                                () => {
                                    runScript(curScript.id);
                                }
                            }
                        >
                            Start
                        </Button>
                        {/* Refresh Button */}
                        <Button
                            variant="contained"
                            color="inherit"
                            startIcon={<RefreshIcon />}
                            sx={{
                                width: '47%',
                                padding: "20px, 40px",
                                backgroundColor: '#f5f5f5', // Light grey
                                fontSize: '16px',

                                color: '#616161', // Dark grey for the text
                                '&:hover': {
                                    backgroundColor: '#e0e0e0', // Slightly darker grey on hover
                                },
                            }}
                            onClick={()=>{reload();}}
                        >
                            Refresh
                        </Button>
                    </div>
                </>
                :
                <>
                    <Typography variant="h5" color="secondary" gutterBottom>
                        Welcome to Smart Chair! Find yours now.
                    </Typography>
                    <pre style={{ color: '#ef6c00', fontFamily: 'monospace', fontSize: '11px', fontWeight: '600' }}>
                        {`

                                   __                  __           
                                  /  |                /  |          
                         _______  $$ |____    ______  $$/   ______  
                        /       | $$      \\  /      \\ /  | /      \\ 
                        /$$$$$$$/ $$$$$$$  | $$$$$$  |$$ |/$$$$$$  |
                        $$ |      $$ |  $$ | /    $$ |$$ |$$ |  $$/ 
                        $$ \\_____ $$ |  $$ |/$$$$$$$ |$$ |$$ |      
                        $$      | $$ |  $$ |$$    $$ |$$ |$$ |      
                        $$$$$$$/  $$/   $$/  $$$$$$$/ $$/ $$/       
                                            
                                        
                       _________________
                     /                /|
                    /                / |
                   /________________/ /|
                ###|      ____      |//|
                #   |     /   /|     |/.|
              #  __|___ /   /.|     |  |_______________
             #  /      /   //||     |  /              /|                  ___
            #  /      /___// ||     | /              / |                 / \\ \\
            # /______/!   || ||_____|/              /  |                /   \\ \\
            #| . . .  !   || ||                    /  _________________/     \\ \\
            #|  . .   !   || //      ________     /  /\\________________  {   /  }
            /|   .    !   ||//~~~~~~/   0000/    /  / / ______________  {   /  /
           / |        !   |'/      /9  0000/    /  / / /             / {   /  /
          / #\\________!___|/      /9  0000/    /  / / /_____________/___  /  /
         / #     /_____\\/        /9  0000/    /  / / /_  /\\_____________\\/  /
        / #                      \`\`^^^^^^    /   \\ \\ . ./ / ____________   /
       +=#==================================/     \\ \\ ./ / /.  .  .  \\ /  /
       |#                                   |      \\ \\/ / /___________/  /
       #                                    |_______\\__/________________/
       |                                    |               |  |  / /       
       |                                    |               |  | / /       
       |                                    |       ________|  |/ /________       
       |                                    |      /_______/    \\_________/\\       
       |                                    |     /        /  /           \\ )       
       |                                    |    /OO^^^^^^/  / /^^^^^^^^^OO\\)       
       |                                    |            /  / /        
       |                                    |           /  / /
       |                                    |          /___\\/
       |Chairs!                             |           oo
       |____________________________________|
       |____________________________________|
                        `}
                    </pre>
                </>
            }
        </Box>
    );
}

export default RightPanel;
