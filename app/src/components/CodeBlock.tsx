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

  return (
    <pre style={{
        height:"450px",
        overflow:"scroll",
        borderRadius: "10px",
        fontSize: "14px"
    }}>
      <code className="language-python">{code}</code>
    </pre>
  );
};

export default CodeBlock;
