// Componente de navegación lateral
import { LayoutDashboard, History, Activity, Settings, Globe } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

/**
 * Componente Sidebar.
 * Muestra la navegación principal de la aplicación con un diseño Glassmorphism Hextech.
 */
export const Sidebar = () => {
  const location = useLocation();
  const { t, i18n } = useTranslation();

  const toggleLanguage = () => {
    i18n.changeLanguage(i18n.language === 'es' ? 'en' : 'es');
  };

  const getLinkClass = (path: string) => {
    const isActive = location.pathname === path;
    return `px-4 py-3 rounded-lg flex items-center gap-3 transition-all duration-300 relative overflow-hidden group ${
      isActive 
        ? 'text-coach-hextech font-semibold bg-coach-hextech/10 shadow-[inset_2px_0_0_0_#0AC8B9]' 
        : 'text-coach-muted hover:text-coach-text hover:bg-white/5 hover:translate-x-1'
    }`;
  };

  return (
    <aside className="w-64 bg-coach-panel/30 backdrop-blur-2xl border-r border-white/5 p-6 flex flex-col gap-10 h-screen sticky top-0 shrink-0 z-50">
      
      {/* Logotipo Hextech */}
      <div className="flex items-center gap-4 group cursor-default">
        <div className="w-10 h-10 rounded-xl bg-coach-panel border border-coach-hextech/50 shadow-glow-hextech flex items-center justify-center transition-all duration-500 group-hover:shadow-[0_0_25px_-5px_rgba(10,200,185,0.7)] group-hover:rotate-6">
          <span className="font-display font-bold text-xl text-coach-hextech tracking-tighter">LC</span>
        </div>
        <div className="flex flex-col">
          <span className="font-display font-bold text-lg tracking-wide text-white leading-tight">LEAGUE</span>
          <span className="font-display font-semibold text-xs tracking-widest text-coach-hextech uppercase">Coach IA</span>
        </div>
      </div>
      
      {/* Navegación Principal */}
      <nav className="flex flex-col gap-2">
        <div className="text-xs font-semibold text-coach-muted/50 uppercase tracking-widest mb-2 px-1">Menu</div>
        
        <Link to="/dashboard" className={getLinkClass('/dashboard')}>
          <LayoutDashboard size={18} className="transition-transform duration-300 group-hover:scale-110" />
          <span>{t('sidebar.overview')}</span>
        </Link>
        <Link to="/matches" className={getLinkClass('/matches')}>
          <History size={18} className="transition-transform duration-300 group-hover:scale-110" />
          <span>{t('sidebar.matches')}</span>
        </Link>
        <Link to="/analysis" className={getLinkClass('/analysis')}>
          <Activity size={18} className="transition-transform duration-300 group-hover:scale-110" />
          <span>{t('sidebar.aiAnalysis')}</span>
        </Link>
      </nav>

      {/* Configuración inferior */}
      <div className="mt-auto flex flex-col gap-2 border-t border-white/5 pt-6">
        <button 
          onClick={toggleLanguage}
          className="px-4 py-3 rounded-lg flex items-center gap-3 transition-all duration-300 text-coach-muted hover:text-coach-text hover:bg-white/5 hover:translate-x-1 text-left group"
        >
          <Globe size={18} className="transition-transform duration-300 group-hover:scale-110" />
          <span className="font-medium flex-1">{i18n.language === 'es' ? 'English' : 'Español'}</span>
          <span className="text-[10px] font-bold bg-white/10 px-2 py-0.5 rounded text-white">{i18n.language.toUpperCase()}</span>
        </button>
        <Link to="/settings" className={getLinkClass('/settings')}>
          <Settings size={18} className="transition-transform duration-300 group-hover:rotate-45" />
          <span>{t('sidebar.settings')}</span>
        </Link>
      </div>
    </aside>
  );
};
