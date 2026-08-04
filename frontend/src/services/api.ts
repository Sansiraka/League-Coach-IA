import axios from 'axios';
import type { MatchSummary } from '../types/api';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Obtiene el resumen de las métricas del jugador.
 * @param gameName Nombre del jugador en el juego.
 * @param tagLine Etiqueta del jugador.
 * @returns Promesa con el resumen de la partida.
 */
export const getPlayerSummary = async (gameName: string, tagLine: string): Promise<MatchSummary> => {
  const response = await axios.get(`${API_URL}/analytics/summary/${gameName}/${tagLine}`);
  return response.data;
};

/**
 * Sincroniza las partidas más recientes del jugador.
 * @param gameName Nombre del jugador.
 * @param tagLine Etiqueta del jugador.
 */
export const syncPlayerMatches = async (gameName: string, tagLine: string) => {
  const response = await axios.post(`${API_URL}/sync/${gameName}/${tagLine}`);
  return response.data;
};

/**
 * Genera recomendaciones y análisis de coaching usando IA.
 * @param gameName Nombre del jugador.
 * @param tagLine Etiqueta del jugador.
 */
export const generateCoachingInsight = async (gameName: string, tagLine: string) => {
  const response = await axios.post(`${API_URL}/coaching/generate/${gameName}/${tagLine}`);
  return response.data;
};

/**
 * Obtiene los detalles completos de una partida para el scoreboard.
 * @param matchId ID de la partida.
 */
export const getMatchDetails = async (matchId: string): Promise<any> => {
  const response = await axios.get(`${API_URL}/analytics/match/${matchId}`);
  return response.data;
};
