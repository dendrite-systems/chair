// src/contexts/ScriptsContext.tsx
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface Script {
    id: string;
    name: string;
    author: string;
    description: string;
    script: string;
    version: string;
  }
  

interface ScriptsContextType {
  scripts: Script[];
  loading: boolean;
  error: string | null;
}

interface ScriptsContextType {
    curScript: Script | null;
    scripts: Script[];
    loading: boolean;
    error: string | null;
    reload: () => void;
    chooseCurScript: (id:number) => void;
    runScript: (id: string) => Promise<void>;
  }
  
  const ScriptsContext = createContext<ScriptsContextType | undefined>(undefined);
  
  const ScriptsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [scripts, setScripts] = useState<Script[]>([]);
    const [curScript, setCurScript] = useState<Script | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
  
    const fetchScripts = async () => {
      try {
        const response = await axios.get('http://localhost:5050/get_scripts_list');
        setScripts(response.data.scripts);
      } catch (error) {
        setError('Failed to fetch scripts');
      } finally {
        setLoading(false);
      }
    };

    const runScript = async (id: string) => {
      try {
        await axios.post('http://localhost:5050/run_script', { script_id: id });
        // Optionally handle any success logic here
        console.log(`Script ${id} executed successfully.`);
      } catch (error) {
        console.error(`Failed to run script ${id}:`, error);
        setError('Failed to run script');
      }
    };
  
    const reload = () => {
      setLoading(true);
      setError(null);
      fetchScripts();
    };

    const chooseCurScript = (id:number) => {
      console.log(id);
      if (id === -1) {
        setCurScript(null);
      } else {
        setCurScript(scripts[id]);
      }
    }
  
    useEffect(() => {
      fetchScripts();
    }, []);
  
    return (
      <ScriptsContext.Provider value={{ curScript, scripts, loading, error, reload, chooseCurScript, runScript}}>
        {children}
      </ScriptsContext.Provider>
    );
  };
  
  export { ScriptsProvider, ScriptsContext };