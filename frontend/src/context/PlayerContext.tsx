import { createContext, useContext, useState, type ReactNode } from 'react';

interface PlayerContextType {
  gameName: string;
  setGameName: (name: string) => void;
  tagLine: string;
  setTagLine: (tag: string) => void;
}

const PlayerContext = createContext<PlayerContextType | undefined>(undefined);

export const PlayerProvider = ({ children }: { children: ReactNode }) => {
  const [gameName, setGameNameState] = useState(() => localStorage.getItem('coach_gameName') || '');
  const [tagLine, setTagLineState] = useState(() => localStorage.getItem('coach_tagLine') || '');

  const setGameName = (name: string) => {
    setGameNameState(name);
    localStorage.setItem('coach_gameName', name);
  };

  const setTagLine = (tag: string) => {
    setTagLineState(tag);
    localStorage.setItem('coach_tagLine', tag);
  };

  return (
    <PlayerContext.Provider value={{ gameName, setGameName, tagLine, setTagLine }}>
      {children}
    </PlayerContext.Provider>
  );
};

export const usePlayer = () => {
  const context = useContext(PlayerContext);
  if (!context) {
    throw new Error('usePlayer must be used within a PlayerProvider');
  }
  return context;
};
