/**
 * Resumen de estadísticas de las partidas de un jugador.
 * Agrupa datos generales, promedios y evaluaciones de rol.
 */
export interface MatchSummary {
  player: string;
  matches_analyzed: number;
  win_rate: number;
  averages: {
    cs_per_min: number;
    kill_participation: number;
    vision_per_min: number;
  };
  role_evaluations: Record<string, any>;
  totals: {
    deaths_before_objectives: number;
  };
  recent_matches: MatchDetail[];
}

/**
 * Detalles específicos de una partida individual.
 * Incluye información sobre desempeño, ventajas de oro y análisis situacional.
 */
export interface MatchDetail {
  match_id: string;
  champion: string;
  role: string;
  win: boolean;
  game_creation: string | null;
  kills: number;
  deaths: number;
  assists: number;
  deaths_before_objectives: number;
  gold_diff_10: number;
  gold_diff_15: number;
  gold_diff_25: number;
  team_damage_percentage: number;
  damage_mitigated: number;
  heal_shield_effective: number;
  cc_time: number;
  turret_plates: number;
  wards_placed: number;
  wards_killed: number;
  vision_wards_bought: number;
  vision_score_advantage: number;
  support_cs_alert: string | null;
  situational_analysis_json: Record<string, any>;
}

export interface MatchScoreboardData {
  match_id: string;
  game_creation: number;
  game_duration: number;
  teams: TeamData[];
  participants: ParticipantData[];
}

export interface TeamData {
  teamId: number;
  win: boolean;
  objectives: Record<string, any>;
}

export interface ParticipantData {
  puuid: string;
  riotIdGameName: string;
  riotIdTagline: string;
  championName: string;
  teamId: number;
  role: string;
  kills: number;
  deaths: number;
  assists: number;
  totalDamageDealtToChampions: number;
  goldEarned: number;
  champLevel: number;
  totalMinionsKilled: number;
  visionScore: number;
  dragonKills: number;
  baronKills: number;
  turretKills: number;
  inhibitorKills: number;
  items: number[];
}

/**
 * Insights generados por la IA para un jugador.
 * Contiene fortalezas, prioridades y plan para la siguiente sesión.
 */
export interface CoachingInsight {
  insight_id: string;
  player: string;
  provider: string;
  analysis: {
    summary: string;
    strengths: Array<{ claim: string; evidence: string }>;
    priorities: Array<{
      title: string;
      evidence: string;
      confidence: string;
      action: string;
      success_metric: string;
    }>;
    next_session_plan: string[];
  };
}
