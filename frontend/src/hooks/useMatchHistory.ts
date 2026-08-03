import { useState, useEffect } from 'react';
import { getPlayerSummary } from '../services/api';
import type { MatchSummary } from '../types/api';
import { useTranslation } from 'react-i18next';
import { usePlayer } from '../context/PlayerContext';

/**
 * Hook para la página de historial de partidas.
 * Maneja el estado y la obtención de partidas recientes.
 */
export const useMatchHistory = () => {
  const { t } = useTranslation();
  const { gameName, setGameName, tagLine, setTagLine } = usePlayer();
  
  const [data, setData] = useState<MatchSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Carga el historial de partidas del jugador desde el backend.
   */
  const fetchData = async () => {
    if (!gameName || !tagLine) return;
    setLoading(true);
    setError('');
    try {
      const summary = await getPlayerSummary(gameName, tagLine);
      setData(summary);
    } catch (err: any) {
      setError(err.response?.data?.detail || t('matches.errorFetch'));
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (gameName && tagLine) {
      fetchData();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    gameName,
    setGameName,
    tagLine,
    setTagLine,
    data,
    loading,
    error,
    fetchData,
  };
};
