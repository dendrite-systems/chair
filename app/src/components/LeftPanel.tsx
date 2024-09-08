import React, { useContext, useEffect, useState } from 'react';
import { Typography } from '@mui/material';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import axios from 'axios';

import { ScriptsContext } from '../ScriptsContext';

const LeftPanel: React.FC = () => {

  const context = useContext(ScriptsContext);
  if (!context) {
    return <div>Context not found</div>;
  }

  const { scripts, loading, error, reload, chooseCurScript } = context;

  return (
    <Box 
      display="flex" 
      justifyContent="flex-start"
      flexDirection="column"
      alignItems="center" 
      height="80vh"
      padding="16px"
      overflow={'scroll'}
    >
      <TableContainer>
        <Table>
          <TableHead onClick={()=>{chooseCurScript(-1)}}
          >
            <TableRow>
              <TableCell className='table-header-cell'>Name </TableCell>
              <TableCell className='table-header-cell'>Version</TableCell>
              <TableCell className='table-header-cell'>Author</TableCell>
              <TableCell className='table-header-cell'>Description</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {scripts.map((script, index) => (
              <TableRow key={index} className='table-content-row'
                onClick={()=>{chooseCurScript(index)}}
              >
                <TableCell className='table-content-cell'>{script.name}</TableCell>
                <TableCell className='table-content-cell'>{script.version}</TableCell>
                <TableCell className='table-content-cell'>{script.author}</TableCell>
                <TableCell className='table-content-cell'>{script.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default LeftPanel;
