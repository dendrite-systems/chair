import React from 'react';
import { Typography } from '@mui/material';
import { Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';


const data = [
  { name: 'Project 1', author: 'Author A', description: 'Description A' },
  { name: 'Project 2', author: 'Author B', description: 'Description B' },
  { name: 'Project 3', author: 'Author C', description: 'Description C' },
];

const LeftPanel: React.FC = () => {
  return (
    <Box 
      display="flex" 
      justifyContent="flex-start"
      flexDirection="column"
      alignItems="center" 
      height="70vh"
      padding="16px"
    >
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell className='table-header-cell'>Name </TableCell>
              <TableCell className='table-header-cell'>Author</TableCell>
              <TableCell className='table-header-cell'>Description</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow 
                key={index}
                className='table-content-row'
              >
                <TableCell className='table-content-cell'>{row.name}</TableCell>
                <TableCell className='table-content-cell'>{row.author}</TableCell>
                <TableCell className='table-content-cell'>{row.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default LeftPanel;
