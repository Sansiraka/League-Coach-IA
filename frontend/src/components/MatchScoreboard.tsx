import { useEffect, useState } from 'react';
import { getMatchDetails } from '../services/api';
import type { MatchScoreboardData, ParticipantData } from '../types/api';
import { useTranslation } from 'react-i18next';
import { Target, Sword, Shield, Activity, Flame } from 'lucide-react';

interface MatchScoreboardProps {
  matchId: string;
}

export const MatchScoreboard = ({ matchId }: MatchScoreboardProps) => {
  const { t } = useTranslation();
  const [data, setData] = useState<MatchScoreboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await getMatchDetails(matchId);
        setData(result);
      } catch (err) {
        setError(t('matches.errorFetch'));
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [matchId, t]);

  if (loading) {
    return (
      <div className="flex justify-center py-10">
        <div className="w-10 h-10 border-4 border-coach-hextech border-t-transparent rounded-full animate-spin shadow-glow-hextech"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="text-coach-accent-red text-center py-4 text-sm font-medium">
        {error || 'No data found'}
      </div>
    );
  }

  const blueTeam = data.participants.filter(p => p.teamId === 100);
  const redTeam = data.participants.filter(p => p.teamId === 200);
  
  const blueObj = data.teams.find(t => t.teamId === 100)?.objectives || {};
  const redObj = data.teams.find(t => t.teamId === 200)?.objectives || {};

  const renderTeamTable = (team: ParticipantData[], isBlue: boolean, objectives: any) => {
    const teamColor = isBlue ? 'text-coach-hextech' : 'text-coach-accent-red';
    const bgHeader = isBlue ? 'bg-coach-hextech/10 border-coach-hextech/30' : 'bg-coach-accent-red/10 border-coach-accent-red/30';

    return (
      <div className="mt-6 border border-white/10 rounded-xl overflow-hidden glass-panel">
        <div className={`p-3 flex justify-between items-center border-b ${bgHeader}`}>
          <h4 className={`font-display font-bold ${teamColor} uppercase tracking-wider text-sm`}>
            {isBlue ? t('matches.blueTeam') || 'Blue Team' : t('matches.redTeam') || 'Red Team'}
          </h4>
          <div className="flex gap-4 text-xs font-semibold text-white/80">
            <span className="flex items-center gap-1" title="Towers"><Target size={14} /> {objectives.tower?.kills || 0}</span>
            <span className="flex items-center gap-1" title="Dragons"><Flame size={14} /> {objectives.dragon?.kills || 0}</span>
            <span className="flex items-center gap-1" title="Barons"><Sword size={14} /> {objectives.baron?.kills || 0}</span>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-black/40 text-coach-muted text-xs uppercase">
              <tr>
                <th className="px-4 py-3">Champion</th>
                <th className="px-4 py-3 text-center">KDA</th>
                <th className="px-4 py-3 text-center">Ratio</th>
                <th className="px-4 py-3 text-center">Damage</th>
                <th className="px-4 py-3 text-center">Gold</th>
                <th className="px-4 py-3 text-center">CS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {team.map(p => {
                const kdaRatio = p.deaths === 0 ? 'Perfect' : ((p.kills + p.assists) / p.deaths).toFixed(2);
                return (
                  <tr key={p.puuid} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-black/50 overflow-hidden border border-white/10 flex-shrink-0">
                          {/* Image placeholder */}
                          <img src={`https://ddragon.leagueoflegends.com/cdn/14.3.1/img/champion/${p.championName}.png`} 
                               onError={(e) => { e.currentTarget.src = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/-1.png' }}
                               alt={p.championName} className="w-full h-full object-cover" />
                        </div>
                        <div>
                          <p className="font-bold text-white text-xs truncate max-w-[120px]">{p.riotIdGameName}</p>
                          <p className="text-[10px] text-coach-muted">{p.championName}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center font-display tracking-wider">
                      <span className="text-white">{p.kills}</span>
                      <span className="text-coach-muted mx-1">/</span>
                      <span className="text-coach-accent-red">{p.deaths}</span>
                      <span className="text-coach-muted mx-1">/</span>
                      <span className="text-white">{p.assists}</span>
                    </td>
                    <td className="px-4 py-3 text-center text-xs font-semibold text-coach-hextech">{kdaRatio}</td>
                    <td className="px-4 py-3 text-center text-xs text-white/80">{p.totalDamageDealtToChampions.toLocaleString()}</td>
                    <td className="px-4 py-3 text-center text-xs text-coach-gold">{p.goldEarned.toLocaleString()} <span className="text-[9px]">g</span></td>
                    <td className="px-4 py-3 text-center text-xs text-white/80">{p.totalMinionsKilled}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="w-full mt-8 animate-fade-in-up">
      <h3 className="text-sm font-bold text-white/90 uppercase tracking-widest mb-4 flex items-center gap-2">
        <Activity size={16} className="text-coach-hextech" />
        {t('matches.scoreboardTitle') || 'Match Scoreboard'}
      </h3>
      
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {renderTeamTable(blueTeam, true, blueObj)}
        {renderTeamTable(redTeam, false, redObj)}
      </div>
    </div>
  );
};
