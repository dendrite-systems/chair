// src/contexts/ScriptsContext.tsx
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { Box, Grid } from '@mui/system';
import StartIcon from '@mui/icons-material/PlayArrow'; // Use the icon you need
import { Button, Typography } from '@mui/material';
interface Script {
  id: string;
  name: string;
  author: string;
  description: string;
  script: string;
  version: string;
  input_json_schema: string;
  output_json_schema: string;
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
  chooseCurScript: (id: number) => void;
  runScript: (id: string) => Promise<void>;
}

const ScriptsContext = createContext<ScriptsContextType | undefined>(undefined);

const ScriptsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [scripts, setScripts] = useState<Script[]>([]);
  const [curScript, setCurScript] = useState<Script | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [inputWindowOpen, setInputWindowOpen] = useState(true);
  const [inputFieldData, setInputFieldData] = useState('');

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
    if (!curScript) return;
    setInputWindowOpen(true);
  };

  const startScript = async (id: string, data: any) => {
    try {
      // parse the input data
      data = JSON.parse(data);
      await axios.post('http://localhost:5050/run_script', {
        script_id: id,
        input_data: data
      });
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

  const chooseCurScript = (id: number) => {
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
    <ScriptsContext.Provider value={{ curScript, scripts, loading, error, reload, chooseCurScript, runScript }}>
      {
        inputWindowOpen && curScript && (
          <>
            <div className="shade-background"
              onClick={() => {setInputWindowOpen(false)}}
            ></div>
            <div className="input-window"
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',

              }}
            >
              <div style={{
                display: 'flex',
                width: '100%',
                height: '100%',
                flexDirection: 'row',
                justifyContent: 'flex-start',
                padding: '20px'
              }}>
                <div style={{
                  display: 'flex',
                  width: '50%',
                  height: '100%',

                  flexDirection: 'column',
                  justifyContent: 'flex-start'
                }}>
                  <Typography variant="h5" color="" gutterBottom>
                    Input Schema
                  </Typography>

                  <textarea
                    style={{
                      width: '80%',
                      height: '90%',
                      padding: '10px',
                      fontSize: '16px',
                      borderRadius: '5px'
                    }}
                    value={curScript.input_json_schema.slice(33, -1)}
                    readOnly
                  ></textarea>
                </div>

                <div style={{
                  display: 'flex',
                  width: '50%',
                  height: '100%',

                  flexDirection: 'column',
                  justifyContent: 'flex-start'
                }}>
                   <Typography variant="h5" color="" gutterBottom>
                    Input Data
                  </Typography>

                  <textarea
                    style={{
                      width: '80%',
                      height: '90%',
                      padding: '10px',
                      fontSize: '16px',
                      borderRadius: '5px'
                    }}
                    value={inputFieldData}
                    onChange={(e) => setInputFieldData(e.target.value)}
                  ></textarea>
                </div>
                
              </div>
              <Button
                  variant="contained"
                  color="primary"
                  startIcon={<StartIcon />}
                  sx={{
                    width: '40%',
                    marginLeft: '20px',
                    backgroundColor: '#ef6c00', // Orange color
                    color: 'white',
                    padding: "20px, 40px",
                    fontSize: '16px',
                    '&:hover': {
                      backgroundColor: '#ff9800'
                    },
                  }}
                  onClick={
                    () => {
                      startScript(curScript.id, inputFieldData);
                      setInputWindowOpen(false);
                      setInputFieldData('');
                    }
                  }
                >
                  Start
                </Button>
            </div>
          </>
        )
      }


      {children}
    </ScriptsContext.Provider>
  );
};

export { ScriptsProvider, ScriptsContext };