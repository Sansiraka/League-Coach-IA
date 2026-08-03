import { useState, useEffect } from 'react';
import { getPlayerSummary, syncPlayerMatches } from '../services/api';
import type { MatchSummary } from '../types/api';
import { useTranslation } from 'react-i18next';
import { usePlayer } from '../context/PlayerContext';

/**
 * Hook para manejar la lógica del dashboard principal.
 * Se encarga de cargar el resumen de las partidas y sincronizarlas.
 */
export const useDashboardOverview = () => {
  const { t } = useTranslation();
  const { gameName, setGameName, tagLine, setTagLine } = usePlayer();
  
  const [data, setData] = useState<MatchSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [syncing, setSyncing] = useState(false);

  /**
   * Obtiene el resumen de rendimiento del jugador.
   */
  const fetchData = async () => {
    if (!gameName || !tagLine) return;
    setLoading(true);
    setError('');
    try {
      const summary = await getPlayerSummary(gameName, tagLine);
      setData(summary);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError(t('dashboard.errorNoData', { name: gameName, tag: tagLine }));
      } else {
        setError(err.response?.data?.detail || t('dashboard.errorFetch'));
      }
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Sincroniza las partidas desde la API de Riot y recarga los datos.
   */
  const handleSync = async () => {
    if (!gameName || !tagLine) return;
    setSyncing(true);
    setError('');
    try {
      await syncPlayerMatches(gameName, tagLine);
      await fetchData();
    } catch (err: any) {
      setError(err.response?.data?.detail || t('dashboard.errorSync'));
    } finally {
      setSyncing(false);
    }
  };

  // Carga inicial automática
  useEffect(() => {
    if (gameName && tagLine && !data) {
      fetchData();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gameName, tagLine]);
  return {
    gameName,
    setGameName,
    tagLine,
    setTagLine,
    data,
    loading,
    error,
    syncing,
    fetchData,
    handleSync,
  };
};
