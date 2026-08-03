import { useState, useEffect } from 'react';
import { generateCoachingInsight } from '../services/api';
import type { CoachingInsight } from '../types/api';
import { useTranslation } from 'react-i18next';
import { usePlayer } from '../context/PlayerContext';

/**
 * Hook para manejar la lógica de obtención de análisis con IA.
 * Extrae el manejo de estado y llamadas a la API del componente principal.
 */
export const useAiAnalysis = () => {
  const { t } = useTranslation();
  const { gameName, setGameName, tagLine, setTagLine } = usePlayer();
  
  const [data, setData] = useState<CoachingInsight | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * Obtiene el análisis de IA para el jugador configurado.
   */
  const fetchAnalysis = async () => {
    if (!gameName || !tagLine) return;
    setLoading(true);
    setError('');
    try {
      const insight = await generateCoachingInsight(gameName, tagLine);
      setData(insight);
    } catch (err: any) {
      setError(err.response?.data?.detail || t('analysis.errorFetch', 'Error generating analysis.'));
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (gameName && tagLine) {
      fetchAnalysis();
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
    fetchAnalysis,
  };
};
