// Vista principal del asistente IA
import { AlertCircle, BrainCircuit, Target, Lightbulb, CheckCircle2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAiAnalysis } from '../hooks/useAiAnalysis';

/**
 * Componente principal para visualizar el análisis del Coach IA.
 * Diseño Glassmorphism Hextech con animaciones avanzadas.
 */
export const AiAnalysis = () => {
  const { t } = useTranslation();
  const { 
    gameName, setGameName, tagLine, setTagLine, 
    data, loading, error, fetchAnalysis 
  } = useAiAnalysis();

  return (
    <div className="flex-1 p-8 overflow-auto relative z-10">
      
      {/* Header & Controles */}
      <header className="mb-10 flex flex-col xl:flex-row justify-between items-start xl:items-end gap-6 animate-fade-in-up">
        <div>
          <h1 className="text-4xl font-display font-bold tracking-tight mb-3 text-white drop-shadow-md flex items-center gap-3">
            <div className="p-2 bg-coach-hextech/20 rounded-xl border border-coach-hextech/30 shadow-glow-hextech">
              <BrainCircuit className="text-coach-hextech" size={32} />
            </div>
            {t('analysis.title', 'AI Coach Analysis')}
          </h1>
          <p className="text-coach-muted mb-6 text-lg">{t('analysis.subtitle', 'Personalized insights based on your recent matches')}</p>
          
          <div className="glass-panel p-2 flex items-center gap-2 max-w-xl">
            <input 
              type="text" 
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              placeholder={t('analysis.placeholderName', 'Game Name')}
              className="bg-transparent px-3 py-2 text-white outline-none w-full placeholder-coach-muted/70 font-medium"
            />
            <span className="text-coach-hextech font-bold opacity-50">#</span>
            <input 
              type="text" 
              value={tagLine}
              onChange={(e) => setTagLine(e.target.value)}
              placeholder={t('analysis.placeholderTag', 'Tag')}
              className="bg-transparent px-3 py-2 text-white outline-none w-28 placeholder-coach-muted/70 font-medium"
            />
            <button 
              onClick={fetchAnalysis}
              disabled={loading}
              className="btn-primary ml-2 disabled:opacity-50 disabled:pointer-events-none"
            >
              {loading ? (
                <BrainCircuit size={18} className="animate-spin text-coach-dark" />
              ) : (
                <BrainCircuit size={18} />
              )}
              <span className="hidden sm:inline">
                {loading ? t('analysis.generating', 'Analyzing...') : t('analysis.generate', 'Generate')}
              </span>
            </button>
          </div>
        </div>
      </header>

      {/* Alertas */}
      {error && (
        <div className="glass-panel !border-coach-accent-red/50 !bg-coach-accent-red/10 p-5 mb-8 flex items-center gap-4 animate-fade-in-up">
          <div className="p-2 bg-coach-accent-red/20 rounded-full text-coach-accent-red">
            <AlertCircle size={24} />
          </div>
          <span className="text-red-200 font-medium">{error}</span>
        </div>
      )}

      {/* Estados de Carga y Vacío */}
      {loading && !data && (
        <div className="flex flex-col items-center justify-center py-20 animate-pulse">
          <div className="w-20 h-20 border-4 border-coach-hextech border-t-transparent rounded-full animate-spin mb-6 shadow-glow-hextech flex items-center justify-center">
            <BrainCircuit className="text-coach-hextech opacity-50" size={24} />
          </div>
          <span className="text-coach-hextech font-display font-bold tracking-widest uppercase text-lg">{t('analysis.generating', 'Analyzing Patterns...')}</span>
        </div>
      )}
      
      {!loading && !data && !error && (
         <div className="glass-panel text-center py-24 flex flex-col items-center gap-5 animate-fade-in-up">
            <div className="p-4 rounded-full bg-white/5 border border-white/10">
              <BrainCircuit size={48} className="text-coach-muted/50" />
            </div>
            <p className="text-coach-muted font-medium text-xl max-w-md">{t('analysis.emptyState', 'Generate an analysis to see your AI Coach insights.')}</p>
         </div>
      )}

      {/* Contenido Analítico */}
      {data && !loading && (
        <div className="space-y-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          
          {/* Resumen Principal */}
          <div className="glass-panel p-8 relative overflow-hidden group">
            <div className="absolute -right-20 -top-20 w-64 h-64 bg-coach-hextech/5 rounded-full blur-3xl transition-transform duration-700 group-hover:scale-150"></div>
            <p className="text-xl md:text-2xl leading-relaxed text-white font-display font-medium relative z-10 drop-shadow-sm">
              <span className="text-coach-hextech text-3xl font-serif mr-2">"</span>
              {data.analysis?.summary || t('analysis.generating', 'Generando resumen...')}
              <span className="text-coach-hextech text-3xl font-serif ml-2">"</span>
            </p>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
            
            {/* Puntos Fuertes (Strengths) */}
            <div className="glass-panel p-8 flex flex-col">
              <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3 text-coach-accent-green border-b border-white/10 pb-4">
                <div className="p-1.5 bg-coach-accent-green/20 rounded-lg">
                  <CheckCircle2 size={24} />
                </div>
                {t('analysis.strengths', 'Strengths & Achievements')}
              </h2>
              <div className="space-y-4 flex-1">
                {(data.analysis?.strengths || []).map((s: any, idx: number) => {
                  
                  // Asignación de estilos dinámicos para los nuevos perfiles Macro
                  let icon = <CheckCircle2 size={20} />;
                  let colorClass = "text-coach-accent-green";
                  let borderHoverClass = "hover:border-coach-accent-green/50";
                  let bgHoverClass = "group-hover:bg-coach-accent-green/10";
                  
                  const claimLower = (s?.claim || "").toLowerCase();
                  if (claimLower.includes("tyrant") || claimLower.includes("línea") || claimLower.includes("lane")) {
                     icon = <Target size={20} />;
                     colorClass = "text-coach-accent-red";
                     borderHoverClass = "hover:border-coach-accent-red/50";
                     bgHoverClass = "group-hover:bg-coach-accent-red/10";
                  } else if (claimLower.includes("macro") || claimLower.includes("dios") || claimLower.includes("god")) {
                     icon = <BrainCircuit size={20} />;
                     colorClass = "text-coach-hextech";
                     borderHoverClass = "hover:border-coach-hextech/50";
                     bgHoverClass = "group-hover:bg-coach-hextech/10";
                  } else if (claimLower.includes("vision") || claimLower.includes("visión")) {
                     icon = <Lightbulb size={20} />;
                     colorClass = "text-coach-accent-blue";
                     borderHoverClass = "hover:border-coach-accent-blue/50";
                     bgHoverClass = "group-hover:bg-coach-accent-blue/10";
                  } else if (claimLower.includes("mechanic") || claimLower.includes("mecánica") || claimLower.includes("outplay") || claimLower.includes("esquive")) {
                     icon = <Zap size={20} />;
                     colorClass = "text-coach-gold";
                     borderHoverClass = "hover:border-coach-gold/50";
                     bgHoverClass = "group-hover:bg-coach-gold/10";
                  }

                  return (
                    <div key={idx} className={`bg-white/5 p-5 rounded-xl border border-white/5 transition-colors group relative overflow-hidden ${borderHoverClass}`}>
                      <div className={`absolute -right-4 -top-4 w-16 h-16 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity ${colorClass.replace('text-', 'bg-')}/20`}></div>
                      
                      <div className="flex items-center gap-3 mb-2 relative z-10">
                         <div className={`p-1.5 rounded-lg bg-white/5 ${bgHoverClass} ${colorClass} transition-colors`}>
                           {icon}
                         </div>
                         <h3 className={`font-bold text-white text-lg group-hover:${colorClass} transition-colors`}>{s?.claim || "Fortaleza detectada"}</h3>
                      </div>
                      
                      <p className="text-coach-muted leading-relaxed pl-10 relative z-10">{s?.evidence || ""}</p>
                    </div>
                  );
                })}
                {!(data.analysis?.strengths?.length > 0) && (
                   <p className="text-coach-muted italic">No se detectaron fortalezas resaltables en estas partidas.</p>
                )}
              </div>
            </div>

            {/* Áreas de Mejora (Priorities) */}
            <div className="glass-panel p-8 flex flex-col relative overflow-hidden">
              <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-l from-coach-accent-red to-transparent"></div>
              <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3 text-coach-accent-red border-b border-white/10 pb-4">
                <div className="p-1.5 bg-coach-accent-red/20 rounded-lg animate-pulse">
                  <Target size={24} />
                </div>
                {t('analysis.priorities', 'Top Priorities')}
              </h2>
              <div className="space-y-5 flex-1">
                {(data.analysis?.priorities || []).map((p: any, idx: number) => (
                  <div key={idx} className="bg-coach-dark/60 p-5 rounded-xl border border-coach-accent-red/20 border-l-4 border-l-coach-accent-red hover:bg-coach-accent-red/5 transition-colors relative overflow-hidden">
                    <div className="flex justify-between items-start mb-3 gap-4">
                      <h3 className="font-bold text-white text-lg">{p?.title || "Prioridad a mejorar"}</h3>
                      <span className="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 bg-coach-accent-red/20 rounded text-coach-accent-red shrink-0">
                        {p?.confidence || "HIGH"}
                      </span>
                    </div>
                    <p className="text-coach-muted/90 mb-4 leading-relaxed">{p?.evidence || ""}</p>
                    
                    <div className="bg-black/30 rounded-lg p-4 space-y-2 border border-white/5">
                      <div className="text-sm flex items-start gap-2">
                        <span className="font-semibold text-coach-hextech min-w-[70px] uppercase tracking-wider text-[10px] mt-1">{t('analysis.action', 'Action:')}</span> 
                        <span className="text-white/90">{p?.action || "Revisa tus repeticiones para corregir esto."}</span>
                      </div>
                      <div className="text-sm flex items-start gap-2">
                        <span className="font-semibold text-coach-accent-green min-w-[70px] uppercase tracking-wider text-[10px] mt-1">{t('analysis.metric', 'Metric:')}</span> 
                        <span className="text-white/90">{p?.success_metric || "-"}</span>
                      </div>
                    </div>
                  </div>
                ))}
                {!(data.analysis?.priorities?.length > 0) && (
                   <p className="text-coach-muted italic">No se detectaron prioridades urgentes.</p>
                )}
              </div>
            </div>
          </div>

          {/* Plan de Siguiente Sesión */}
          <div className="glass-panel p-8">
            <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3 text-coach-gold border-b border-white/10 pb-4">
              <div className="p-1.5 bg-coach-gold/20 rounded-lg">
                <Lightbulb size={24} />
              </div>
              {t('analysis.nextSession', 'Next Session Plan')}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {(data.analysis?.next_session_plan || []).map((item: string, idx: number) => (
                <div key={idx} className="bg-white/5 p-6 rounded-xl border border-white/5 hover:border-coach-gold/30 hover:-translate-y-1 transition-all group relative overflow-hidden">
                  <div className="absolute -right-4 -top-4 w-16 h-16 bg-coach-gold/10 rounded-full blur-xl group-hover:bg-coach-gold/20 transition-all"></div>
                  <span className="text-5xl font-display font-black text-white/5 absolute bottom-2 right-4 group-hover:text-coach-gold/10 transition-colors">
                    0{idx + 1}
                  </span>
                  <div className="w-10 h-10 rounded-full bg-coach-gold/20 text-coach-gold flex items-center justify-center font-bold mb-4 shadow-[0_0_15px_-3px_rgba(200,170,110,0.5)]">
                    {idx + 1}
                  </div>
                  <p className="text-white/90 font-medium relative z-10 leading-relaxed">{item}</p>
                </div>
              ))}
            </div>
          </div>
          
        </div>
      )}
    </div>
  );
};
