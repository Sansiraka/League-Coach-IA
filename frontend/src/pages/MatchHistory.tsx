import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { AlertCircle, Search, History, Swords, ChevronDown, ChevronUp } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useMatchHistory } from '../hooks/useMatchHistory';

/**
 * Componente que muestra el historial de partidas del jugador y detalles con gráficas.
 * Diseño actualizado a Premium Hextech Glassmorphism con funcionalidad de acordeón.
 */
export const MatchHistory = () => {
  const { t } = useTranslation();
  const { 
    gameName, setGameName, tagLine, setTagLine, 
    data, loading, error, fetchData 
  } = useMatchHistory();
  
  const [expandedMatches, setExpandedMatches] = useState<Record<string, boolean>>({});

  const toggleMatch = (matchId: string) => {
    setExpandedMatches(prev => ({
      ...prev,
      [matchId]: !prev[matchId]
    }));
  };

  return (
    <div className="flex-1 p-8 overflow-auto relative z-10">
      
      {/* Header & Búsqueda */}
      <header className="mb-10 flex flex-col xl:flex-row justify-between items-start xl:items-end gap-6 animate-fade-in-up">
        <div>
          <h1 className="text-4xl font-display font-bold tracking-tight mb-3 text-white drop-shadow-md flex items-center gap-3">
            <div className="p-2 bg-coach-hextech/20 rounded-xl border border-coach-hextech/30 shadow-glow-hextech">
              <History className="text-coach-hextech" size={32} />
            </div>
            {t('matches.title')}
          </h1>
          <p className="text-coach-muted mb-6 text-lg">{t('matches.subtitle')}</p>
          
          <div className="glass-panel p-2 flex items-center gap-2 max-w-xl">
            <input 
              type="text" 
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              placeholder={t('matches.placeholderName')}
              className="bg-transparent px-3 py-2 text-white outline-none w-full placeholder-coach-muted/70 font-medium"
            />
            <span className="text-coach-hextech font-bold opacity-50">#</span>
            <input 
              type="text" 
              value={tagLine}
              onChange={(e) => setTagLine(e.target.value)}
              placeholder={t('matches.placeholderTag')}
              className="bg-transparent px-3 py-2 text-white outline-none w-28 placeholder-coach-muted/70 font-medium"
            />
            <button 
              onClick={fetchData}
              disabled={loading}
              className="btn-primary ml-2 disabled:opacity-50 disabled:pointer-events-none"
            >
              {loading ? (
                <Search size={18} className="animate-spin text-coach-dark" />
              ) : (
                <Search size={18} />
              )}
              <span className="hidden sm:inline">
                {t('matches.search')}
              </span>
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="glass-panel !border-coach-accent-red/50 !bg-coach-accent-red/10 p-5 mb-8 flex items-center gap-4 animate-fade-in-up">
          <div className="p-2 bg-coach-accent-red/20 rounded-full text-coach-accent-red">
            <AlertCircle size={24} />
          </div>
          <span className="text-red-200 font-medium">{error}</span>
        </div>
      )}

      {loading && !data && (
        <div className="flex flex-col items-center justify-center py-20 animate-pulse">
          <div className="w-16 h-16 border-4 border-coach-hextech border-t-transparent rounded-full animate-spin mb-4 shadow-glow-hextech"></div>
          <span className="text-coach-hextech font-display font-medium tracking-widest uppercase">{t('matches.loading')}</span>
        </div>
      )}
      
      {!loading && !data && !error && (
         <div className="glass-panel text-center py-24 flex flex-col items-center gap-5 animate-fade-in-up">
            <div className="p-4 rounded-full bg-white/5 border border-white/10">
              <Swords size={48} className="text-coach-muted/50" />
            </div>
            <p className="text-coach-muted font-medium text-xl">{t('matches.emptyState')}</p>
         </div>
      )}

      {data && !loading && (
      <div className="space-y-4 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
        {data.recent_matches.map((match: any) => {
          // Format data for Recharts (Gold Difference over time: min 10, 15, 25)
          const chartData = [
            { time: '10m', diff: match.gold_diff_10 },
            { time: '15m', diff: match.gold_diff_15 },
            { time: '25m', diff: match.gold_diff_25 }
          ];

          const isExpanded = expandedMatches[match.match_id] || false;

          return (
            <div key={match.match_id} className="glass-panel relative overflow-hidden group transition-all duration-300">
              <div className={`absolute top-0 right-0 w-64 h-64 rounded-full blur-[80px] -mr-20 -mt-20 opacity-20 pointer-events-none transition-all duration-700 ${match.win ? 'bg-coach-hextech group-hover:scale-150' : 'bg-coach-accent-red group-hover:scale-150'}`}></div>
              
              {/* Cabecera Clickable (Acordeón) */}
              <div 
                className="flex flex-col md:flex-row justify-between items-start md:items-center p-6 gap-4 cursor-pointer hover:bg-white/5 transition-colors"
                onClick={() => toggleMatch(match.match_id)}
              >
                <div className="flex items-center gap-5">
                  <div className={`w-1.5 h-12 rounded-full shadow-lg ${match.win ? 'bg-coach-accent-green shadow-coach-accent-green/50' : 'bg-coach-accent-red shadow-coach-accent-red/50'}`}></div>
                  <div>
                    <h3 className="text-xl font-display font-bold text-white drop-shadow-sm mb-1 flex items-center gap-2">
                      {match.champion}
                    </h3>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-coach-muted">{match.role}</span>
                      <span className="text-coach-muted/50">•</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${match.win ? 'bg-coach-accent-green/20 text-coach-accent-green' : 'bg-coach-accent-red/20 text-coach-accent-red'}`}>
                        {match.win ? t('matches.victory') : t('matches.defeat')}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-6">
                  <div className="flex gap-6 text-right bg-black/20 px-4 py-2 rounded-xl border border-white/5">
                    <div>
                      <p className="text-[9px] font-bold text-coach-muted uppercase tracking-widest">{t('matches.visionMin')}</p>
                      <p className="font-display font-bold text-lg text-white">
                         {match.wards_placed + match.wards_killed} <span className="text-[10px] text-coach-muted font-sans font-normal">{t('matches.score')}</span>
                      </p>
                    </div>
                    <div>
                      <p className="text-[9px] font-bold text-coach-muted uppercase tracking-widest">{t('matches.objDeaths')}</p>
                      <p className="font-display font-bold text-lg text-white">{match.deaths_before_objectives}</p>
                    </div>
                  </div>
                  
                  <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-coach-muted border border-white/10">
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </div>
                </div>
              </div>

              {/* Detalle Desplegable */}
              {isExpanded && (
                <div className="p-6 pt-0 border-t border-white/10 mt-2 animate-fade-in-up">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pt-6">
                    {/* Chart Section */}
                    <div>
                      <h4 className="text-xs font-semibold text-white/80 mb-4 uppercase tracking-wider">{t('matches.goldDiffTitle')}</h4>
                      <div className="h-48 w-full bg-black/10 rounded-xl p-4 border border-white/5">
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={chartData} margin={{ top: 10, right: 20, bottom: 5, left: 0 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis dataKey="time" stroke="#8A9BA8" fontSize={10} tickLine={false} axisLine={false} />
                            <YAxis stroke="#8A9BA8" fontSize={10} tickLine={false} axisLine={false} width={40} />
                            <Tooltip 
                              contentStyle={{ backgroundColor: 'rgba(9, 20, 40, 0.95)', border: '1px solid rgba(10,200,185,0.2)', borderRadius: '8px', backdropFilter: 'blur(8px)', boxShadow: '0 0 20px -5px rgba(0,0,0,0.5)' }}
                              itemStyle={{ color: '#F0E6D2', fontWeight: 'bold', fontSize: '12px' }}
                              labelStyle={{ color: '#8A9BA8', marginBottom: '4px', fontSize: '10px' }}
                            />
                            <ReferenceLine y={0} stroke="rgba(255,255,255,0.1)" strokeWidth={2} />
                            <Line 
                              type="monotone" 
                              dataKey="diff" 
                              stroke={match.win ? '#0AC8B9' : '#E84057'} 
                              strokeWidth={2} 
                              dot={{ fill: match.win ? '#0AC8B9' : '#E84057', strokeWidth: 2, r: 4, stroke: '#010A13' }}
                              activeDot={{ r: 6, strokeWidth: 0, fill: '#FFFFFF' }} 
                            />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* Situational Items Analysis */}
                    <div className="flex flex-col">
                      <h4 className="text-xs font-semibold text-white/80 mb-4 uppercase tracking-wider flex items-center gap-2">
                         <AlertCircle size={14} className="text-coach-gold" />
                         {t('matches.situationalChecks')}
                      </h4>
                      <div className="space-y-2 flex-1">
                        {Object.entries(match.situational_analysis_json || {}).map(([rule, result]) => {
                          const typedResult = result as any;
                          const verdict = typedResult.verdict || typedResult.status; 
                          
                          let badgeClasses = 'bg-white/5 text-coach-muted border-white/10';
                          let icon = '➖';
                          if (verdict === 'CORRECT') { badgeClasses = 'bg-coach-accent-green/20 text-coach-accent-green border-coach-accent-green/30'; icon = '✅'; }
                          if (verdict === 'MISSED') { badgeClasses = 'bg-coach-accent-red/20 text-coach-accent-red border-coach-accent-red/30 shadow-[0_0_10px_-2px_rgba(232,64,87,0.3)]'; icon = '❌'; }
                          if (verdict === 'TEAM_COVERED') { badgeClasses = 'bg-coach-hextech/20 text-coach-hextech border-coach-hextech/30'; icon = '🛡️'; }
                          if (verdict === 'EXEMPT') { badgeClasses = 'bg-coach-gold/20 text-coach-gold border-coach-gold/30'; icon = '✨'; }
                          
                          return (
                            <div key={rule} className="flex justify-between items-center bg-black/20 hover:bg-black/40 transition-colors rounded-lg p-3 border border-white/5">
                              <div>
                                <p className="text-xs font-bold capitalize text-white/90">{rule.replace('_', ' ')}</p>
                                {typedResult.reason && <p className="text-[10px] text-coach-muted leading-tight mt-0.5">{typedResult.reason}</p>}
                              </div>
                              <div className={`px-2 py-1 rounded text-[9px] uppercase tracking-widest font-bold border flex items-center gap-1 whitespace-nowrap ml-4 ${badgeClasses}`}>
                                <span>{icon}</span> {verdict}
                              </div>
                            </div>
                          )
                        })}
                        {Object.keys(match.situational_analysis_json || {}).length === 0 && (
                          <div className="h-full flex items-center justify-center p-4 border border-dashed border-white/10 rounded-lg">
                            <p className="text-xs font-medium text-coach-muted text-center">{t('matches.noThreats')}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
      )}
    </div>
  );
};
