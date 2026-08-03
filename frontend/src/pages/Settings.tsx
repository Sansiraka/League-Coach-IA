// Vista de configuración de usuario
import { useState } from 'react';
import { Settings as SettingsIcon, Save, CheckCircle2, User } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { usePlayer } from '../context/PlayerContext';

/**
 * Componente de Configuración.
 * Permite al usuario establecer su Riot ID por defecto (Game Name y Tag Line).
 */
export const Settings = () => {
  const { t } = useTranslation();
  const { gameName, setGameName, tagLine, setTagLine } = usePlayer();
  
  // Estados locales para el formulario
  const [localName, setLocalName] = useState(gameName);
  const [localTag, setLocalTag] = useState(tagLine);
  const [saved, setSaved] = useState(false);

  // Guarda las credenciales en el contexto y localStorage
  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setGameName(localName);
    setTagLine(localTag);
    setSaved(true);
    
    // Oculta el mensaje de éxito después de 3 segundos
    setTimeout(() => {
      setSaved(false);
    }, 3000);
  };

  return (
    <div className="flex-1 p-8 overflow-auto relative z-10 animate-fade-in-up">
      
      {/* Header */}
      <header className="mb-10 flex flex-col gap-2">
        <h1 className="text-4xl font-display font-bold tracking-tight text-white drop-shadow-md flex items-center gap-3">
          <div className="p-2 bg-coach-hextech/20 rounded-xl border border-coach-hextech/30 shadow-glow-hextech">
            <SettingsIcon className="text-coach-hextech" size={32} />
          </div>
          {t('sidebar.settings', 'Settings')}
        </h1>
        <p className="text-coach-muted text-lg">
          Configura tu identidad de jugador por defecto para realizar búsquedas automáticas.
        </p>
      </header>

      <div className="max-w-2xl">
        {saved && (
          <div className="glass-panel !border-coach-accent-green/50 !bg-coach-accent-green/10 p-4 mb-6 flex items-center gap-3 animate-fade-in-up">
            <div className="p-1.5 bg-coach-accent-green/20 rounded-full text-coach-accent-green">
              <CheckCircle2 size={20} />
            </div>
            <span className="text-green-200 font-medium">Configuración guardada correctamente. Este será tu perfil predeterminado.</span>
          </div>
        )}

        <div className="glass-panel p-8">
          <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3 text-white border-b border-white/10 pb-4">
            <User className="text-coach-accent-blue" size={24} />
            Perfil de Riot Games
          </h2>
          
          <form onSubmit={handleSave} className="space-y-6">
            <div className="flex flex-col gap-2">
              <label htmlFor="gameName" className="text-sm font-semibold text-coach-muted uppercase tracking-wider">
                Riot ID (Game Name)
              </label>
              <input
                id="gameName"
                type="text"
                value={localName}
                onChange={(e) => setLocalName(e.target.value)}
                placeholder="Ej. Hide on bush"
                className="bg-black/20 border border-white/10 px-4 py-3 rounded-xl text-white outline-none focus:border-coach-hextech transition-colors focus:bg-black/40"
                required
              />
            </div>
            
            <div className="flex flex-col gap-2">
              <label htmlFor="tagLine" className="text-sm font-semibold text-coach-muted uppercase tracking-wider">
                Tagline (Sin el #)
              </label>
              <input
                id="tagLine"
                type="text"
                value={localTag}
                onChange={(e) => setLocalTag(e.target.value)}
                placeholder="Ej. KR1"
                className="bg-black/20 border border-white/10 px-4 py-3 rounded-xl text-white outline-none focus:border-coach-hextech transition-colors focus:bg-black/40"
                required
              />
            </div>

            <div className="pt-4 border-t border-white/5">
              <button 
                type="submit"
                className="btn-primary w-full sm:w-auto"
              >
                <Save size={18} />
                Guardar Configuración
              </button>
            </div>
          </form>
        </div>
        
        {/* Helper Note */}
        <div className="mt-8 p-6 bg-coach-dark/50 rounded-xl border border-white/5">
          <h4 className="font-bold text-white mb-2">¿Por qué configurar esto?</h4>
          <p className="text-sm text-coach-muted leading-relaxed">
            League of Coach utiliza estos datos para pre-llenar las búsquedas en el Dashboard, Historial y Análisis IA. 
            No necesitas volver a escribir tu nombre de invocador cada vez que inicies la aplicación. Aún así, siempre podrás realizar búsquedas manuales de otros jugadores desde cualquiera de esas secciones.
          </p>
        </div>
      </div>
    </div>
  );
};
