import { getCapabilities, getClaims } from "@/lib/data";
import { AlertCircle, CheckCircle2, CircleDashed } from "lucide-react";

export default function Home() {
  const capabilities = getCapabilities();
  const claims = getClaims();

  // Group capabilities by Domain
  const domains = Array.from(new Set(capabilities.map((c) => c.domain)));

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-50 p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-16">
        <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-gradient-to-r from-emerald-400 to-cyan-500 bg-clip-text text-transparent">
          AI Capability Radar
        </h1>
        <p className="text-neutral-400 text-lg max-w-2xl">
          Real-time tracking of the Expanding AI Bubble. This dashboard aggregates signals from
          curated sensors across the web to definitively map what Foundation Models can and cannot do today.
        </p>
      </header>

      <main className="max-w-6xl mx-auto space-y-16">
        {domains.map((domain) => {
          const domainCaps = capabilities.filter((c) => c.domain === domain);
          return (
            <div key={domain}>
              <h2 className="text-3xl font-bold mb-8 border-b border-neutral-800 pb-4">
                {domain.replace(/_/g, " ")}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {domainCaps.map((cap) => {
                  const capClaims = claims.filter((c) => c.capability_id === cap.id);
                  const statusColors = {
                    "Inside_Bubble": "bg-emerald-500/10 border-emerald-500/20 text-emerald-400",
                    "Frontier": "bg-amber-500/10 border-amber-500/20 text-amber-400",
                    "Outside_Bubble": "bg-red-500/10 border-red-500/20 text-red-400",
                  };

                  const statusIcons = {
                    "Inside_Bubble": <CheckCircle2 className="w-5 h-5" />,
                    "Frontier": <CircleDashed className="w-5 h-5 animate-[spin_4s_linear_infinite]" />,
                    "Outside_Bubble": <AlertCircle className="w-5 h-5" />,
                  };

                  const colorClass = statusColors[cap.current_status as keyof typeof statusColors] || statusColors["Frontier"];
                  const Icon = statusIcons[cap.current_status as keyof typeof statusIcons] || statusIcons["Frontier"];

                  return (
                    <div
                      key={cap.id}
                      className={`relative overflow-hidden rounded-2xl border bg-neutral-900/50 backdrop-blur-sm p-6 flex flex-col transition-all hover:-translate-y-1 hover:shadow-xl ${colorClass}`}
                    >
                      <div className="flex justify-between items-start mb-4">
                        <h3 className="text-xl font-bold font-mono tracking-tight text-neutral-100">{cap.skill.replace(/_/g, " ")}</h3>
                        <div title={cap.current_status.replace(/_/g, " ")}>{Icon}</div>
                      </div>

                      <p className="text-sm text-neutral-400 mb-6 flex-grow">{cap.description}</p>

                      <div className="pt-4 border-t border-neutral-800/50">
                        <div className="flex justify-between items-end">
                          <div>
                            <span className="text-xs uppercase tracking-wider text-neutral-500 font-bold">Signals Detected</span>
                            <div className="text-2xl font-black mt-1">{capClaims.length}</div>
                          </div>
                          <span className="text-xs font-mono uppercase px-2 py-1 rounded bg-black/40">{cap.current_status.replace(/_/g, " ")}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </main>
    </div>
  );
}
