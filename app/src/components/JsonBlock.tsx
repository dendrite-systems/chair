// JSONPrettyPrint.tsx
import React from 'react';

interface JSONPrettyPrintProps {
  data: object;
}

const JSONPrettyPrint: React.FC<JSONPrettyPrintProps> = ({ data }) => {
  const formattedJSON = JSON.stringify(data, null, 2); // Indent with 2 spaces

  return (
    <pre style={{
        backgroundColor: '#2e2e2e', // Dark background
        color: '#f8f8f2', // Light text color
        borderRadius: '8px',
        padding: '16px',
        fontSize: '14px',
        overflow: 'auto',
        maxHeight: '450px', // Adjust height as needed
        whiteSpace: 'pre-wrap' // Ensures proper wrapping
    }}>
      {formattedJSON}
    </pre>
  );
};

export default JSONPrettyPrint;
