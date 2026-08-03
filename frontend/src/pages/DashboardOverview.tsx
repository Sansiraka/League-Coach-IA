// Vista general del dashboard
import { AlertCircle, RefreshCw, Search, Zap, Crosshair, ShieldAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useDashboardOverview } from '../hooks/useDashboardOverview';

/**
 * Vista general del dashboard del jugador.
 * Implementa el diseño premium Hextech Glassmorphism.
 */
export const DashboardOverview = () => {
  const { t } = useTranslation();
  const { 
    gameName, setGameName, tagLine, setTagLine, 
    data, loading, error, syncing, fetchData, handleSync 
  } = useDashboardOverview();

  return (
    <div className="flex-1 p-8 overflow-auto relative z-10">
      
      {/* Header & Búsqueda */}
      <header className="mb-10 flex flex-col xl:flex-row justify-between items-start xl:items-end gap-6 animate-fade-in-up">
        <div>
          <h1 className="text-4xl font-bold tracking-tight mb-4 text-white drop-shadow-md">
            {t('dashboard.title')}
          </h1>
          <div className="glass-panel p-2 flex items-center gap-2 max-w-xl">
            <input 
              type="text" 
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              placeholder={t('dashboard.placeholderName')}
              className="bg-transparent px-3 py-2 text-white outline-none w-full placeholder-coach-muted/70 font-medium"
            />
            <span className="text-coach-hextech font-bold opacity-50">#</span>
            <input 
              type="text" 
              value={tagLine}
              onChange={(e) => setTagLine(e.target.value)}
              placeholder={t('dashboard.placeholderTag')}
              className="bg-transparent px-3 py-2 text-white outline-none w-28 placeholder-coach-muted/70 font-medium"
            />
            <button onClick={fetchData} className="btn-primary ml-2">
              <Search size={18} /> 
              <span className="hidden sm:inline">{t('dashboard.search')}</span>
            </button>
          </div>
        </div>
        
        <button 
          onClick={handleSync}
          disabled={syncing}
          className="btn-hextech disabled:opacity-50 disabled:pointer-events-none"
        >
          <RefreshCw size={18} className={syncing ? "animate-spin text-coach-hextech" : ""} />
          {syncing ? t('dashboard.syncing') : t('dashboard.syncButton')}
        </button>
      </header>

      {/* Alertas y Estados */}
      {error && !error.includes('No hay datos') && !error.includes('no encontrado') && !error.includes('No data') && (
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
          <span className="text-coach-hextech font-display font-medium tracking-widest uppercase">{t('dashboard.loading')}</span>
        </div>
      )}
      
      {!loading && !data && (
         <div className="glass-panel text-center py-24 flex flex-col items-center gap-5 animate-fade-in-up">
            <div className="p-4 rounded-full bg-coach-panel border border-coach-hextech/30 shadow-glow-hextech mb-2">
              <RefreshCw size={48} className="text-coach-hextech opacity-90" />
            </div>
            {gameName && tagLine ? (
              <>
                <p className="text-white font-display font-medium text-2xl">
                  Aún no tenemos partidas guardadas para {gameName}#{tagLine}.
                </p>
                <p className="text-coach-muted text-lg max-w-lg">
                  Haz clic en el botón de <strong className="text-coach-hextech">Sincronizar Partidas</strong> en la esquina superior para descargar tu historial desde los servidores de Riot Games.
                </p>
              </>
            ) : (
              <>
                <p className="text-white font-display font-medium text-2xl">
                  Identidad no configurada.
                </p>
                <p className="text-coach-muted text-lg max-w-lg">
                  Ve a la pestaña de Ajustes o introduce tu Riot ID en la barra superior para comenzar.
                </p>
              </>
            )}
         </div>
      )}

      {/* Contenido Principal (Métricas) */}
      {data && !loading && (
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
        
        {/* Tarjeta de Rendimiento Principal */}
        <div className="col-span-1 xl:col-span-2 glass-panel p-8 flex flex-col">
          <div className="flex items-center justify-between mb-8 border-b border-white/10 pb-4">
            <h2 className="text-xl font-display font-semibold text-white flex items-center gap-2">
              <Zap className="text-coach-gold" size={20} />
              {t('dashboard.recentPerformance')}
            </h2>
            <div className="stat-badge !bg-coach-hextech/20 !text-coach-hextech !border-coach-hextech/30">
              {data.matches_analyzed} Partidas Analizadas
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
            <div className="bg-white/5 rounded-xl p-5 border border-white/5 relative overflow-hidden group hover:border-coach-hextech/50 transition-colors">
              <div className="absolute top-0 right-0 w-16 h-16 bg-coach-accent-green/10 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-150"></div>
              <p className="text-xs font-semibold text-coach-muted uppercase tracking-wider mb-2">{t('dashboard.winRate')}</p>
              <p className="text-4xl font-display font-bold text-white drop-shadow-md">{data.win_rate}<span className="text-xl text-coach-accent-green">%</span></p>
            </div>
            
            <div className="bg-white/5 rounded-xl p-5 border border-white/5 relative overflow-hidden group hover:border-coach-gold/50 transition-colors">
              <div className="absolute top-0 right-0 w-16 h-16 bg-coach-gold/10 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-150"></div>
              <p className="text-xs font-semibold text-coach-muted uppercase tracking-wider mb-2">{t('dashboard.avgCs')}</p>
              <p className="text-4xl font-display font-bold text-white drop-shadow-md">{data.averages.cs_per_min}</p>
            </div>
            
            <div className="bg-white/5 rounded-xl p-5 border border-white/5 relative overflow-hidden group hover:border-coach-accent-red/50 transition-colors">
              <div className="absolute top-0 right-0 w-16 h-16 bg-coach-accent-red/10 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-150"></div>
              <p className="text-xs font-semibold text-coach-muted uppercase tracking-wider mb-2">{t('dashboard.avgKp')}</p>
              <p className="text-4xl font-display font-bold text-white drop-shadow-md">{data.averages.kill_participation}<span className="text-xl text-coach-accent-red">%</span></p>
            </div>
            
            <div className="bg-white/5 rounded-xl p-5 border border-white/5 relative overflow-hidden group hover:border-coach-accent-blue/50 transition-colors">
              <div className="absolute top-0 right-0 w-16 h-16 bg-coach-accent-blue/10 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-150"></div>
              <p className="text-xs font-semibold text-coach-muted uppercase tracking-wider mb-2">{t('dashboard.visionMin')}</p>
              <p className="text-4xl font-display font-bold text-white drop-shadow-md">{data.averages.vision_per_min}</p>
            </div>
          </div>
          
          <div className="mt-auto">
            <h3 className="text-xs font-semibold text-coach-muted uppercase tracking-widest mb-4">{t('dashboard.roleEval')}</h3>
            <div className="flex flex-wrap gap-3">
               {Object.entries(data.role_evaluations).map(([role, evalData]: [string, any]) => (
                 <div key={role} className="stat-badge !px-4 !py-2 bg-gradient-to-r from-white/5 to-white/10 hover:from-coach-hextech/20 hover:to-coach-accent-blue/20 transition-all cursor-default border-white/10">
                   <Crosshair size={14} className="text-coach-hextech" />
                   <span className="font-bold text-white">{role}</span>
                   <span className="text-coach-muted mx-1">|</span>
                   <span className="text-coach-hextech">{evalData.matches_played} {t('dashboard.matchesPlayed')}</span>
                 </div>
               ))}
            </div>
          </div>
        </div>

        {/* Tarjeta de Feedback IA (Situacional) */}
        <div className="col-span-1 glass-panel p-8">
          <h2 className="text-xl font-display font-semibold text-white flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
            <ShieldAlert className="text-coach-accent-red animate-pulse" size={20} />
            {t('dashboard.aiInsight')}
          </h2>
          
          <div className="space-y-6">
             {data.recent_matches.slice(0,2).map((match: any) => (
                <div key={match.match_id} className="bg-coach-dark/50 rounded-xl p-5 border border-white/5">
                   <div className="flex justify-between items-center mb-3">
                     <span className="stat-badge !bg-coach-panel !border-white/10">
                       <span className="text-coach-gold">{match.champion}</span> 
                       <span className="text-coach-muted mx-1">•</span> 
                       {match.role}
                     </span>
                     <span className={`text-xs font-bold px-2 py-1 rounded ${match.win ? 'bg-coach-accent-green/20 text-coach-accent-green' : 'bg-coach-accent-red/20 text-coach-accent-red'}`}>
                       {match.win ? 'VICTORIA' : 'DERROTA'}
                     </span>
                   </div>
                   
                   <div className="text-coach-text/90 text-sm space-y-2">
                      {match.support_cs_alert === 'STEALING_CS' && (
                        <div className="text-coach-accent-red bg-coach-accent-red/10 px-3 py-2 rounded border border-coach-accent-red/20">
                          ⚠️ {t('dashboard.stealingCsAlert')}
                        </div>
                      )}
                      
                      {Object.keys(match.situational_analysis_json || {}).length > 0 && (
                        <div className="mt-4">
                          <p className="text-xs font-semibold text-coach-muted uppercase tracking-widest mb-3">{t('dashboard.situationalAlerts')}</p>
                          <ul className="space-y-2">
                            {Object.entries(match.situational_analysis_json).map(([rule, result]: [string, any]) => {
                              // Seleccionar el color basado en nuestro nuevo backend
                              let colorClass = 'text-coach-muted';
                              let icon = '➖';
                              if (result.verdict === 'CORRECT') { colorClass = 'text-coach-accent-green'; icon = '✅'; }
                              if (result.verdict === 'MISSED') { colorClass = 'text-coach-accent-red font-bold'; icon = '❌'; }
                              if (result.verdict === 'TEAM_COVERED') { colorClass = 'text-coach-hextech'; icon = '🛡️'; }
                              if (result.verdict === 'EXEMPT') { colorClass = 'text-coach-gold'; icon = '✨'; }
                              
                              return (
                                <li key={rule} className="flex justify-between items-center bg-white/5 px-3 py-2 rounded">
                                  <span className="capitalize text-xs font-medium text-white/80">{rule.replace('_', ' ')}</span>
                                  <span className={`text-xs flex items-center gap-1 ${colorClass}`}>
                                    {icon} {result.verdict}
                                  </span>
                                </li>
                              )
                            })}
                          </ul>
                        </div>
                      )}
                   </div>
                </div>
             ))}
          </div>
        </div>
        
      </div>
      )}
    </div>
  );
};
