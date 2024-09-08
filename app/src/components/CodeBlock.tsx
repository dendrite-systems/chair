// CodeBlock.tsx
import React, { useEffect } from 'react';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css'; // Import a Prism theme
import 'prismjs/components/prism-python.min.js'; // Import Python syntax highlighting
import { width } from '@mui/system';

interface CodeBlockProps {
  code: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code }) => {
  useEffect(() => {
    Prism.highlightAll(); // Highlight code on component mount
  }, [code]);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
  };

  return (
    <pre style={{
        height:"450px",
        overflow:"scroll",
        borderRadius: "10px",
        fontSize: "14px",
        position: 'relative',
    }}>
        <button
        onClick={handleCopy}
        style={{
          position: 'absolute',
          top: '12px',
          right: '12px',
          backgroundColor: '#ef6c00', // Orange color
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          padding: '4px 8px',
          cursor: 'pointer',
          zIndex: 1
        }}
      >
        Copy
      </button>
      <code className="language-python">{code}</code>
    </pre>
  );
};

export default CodeBlock;
