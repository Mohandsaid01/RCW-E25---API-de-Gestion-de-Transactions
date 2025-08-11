import { useEffect, useState } from "react";
import api from "../api";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(()=>{
    (async ()=>{
      try { const { data } = await api.get("/reports/summary"); setSummary(data); }
      finally { setLoading(false); }
    })();
  },[]);

  if (loading) return <div className="container">Chargement…</div>;
  if (!summary) return <div className="container">Aucune donnée</div>;

  return (
    <div className="container">
      <h2 className="page-title">Tableau de bord</h2>

      <div className="cards">
        <div className="card">
          <h4>Totaux par service</h4>
          <ul style={{margin:0, paddingLeft:18}}>
            {Object.entries(summary.by_service).length === 0 && <li>—</li>}
            {Object.entries(summary.by_service).map(([k,v]) => (
              <li key={k}>{k}: {v.toFixed(2)}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h4>Totaux par devise</h4>
          <ul style={{margin:0, paddingLeft:18}}>
            {Object.entries(summary.by_currency).length === 0 && <li>—</li>}
            {Object.entries(summary.by_currency).map(([k,v]) => (
              <li key={k}>{k}: {v.toFixed(2)}</li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h4>Totaux par pays</h4>
          <ul style={{margin:0, paddingLeft:18}}>
            {Object.entries(summary.by_country).length === 0 && <li>—</li>}
            {Object.entries(summary.by_country).map(([k,v]) => (
              <li key={k}>{k}: {v.toFixed(2)}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="total">
        Total en {summary.base_currency}: <b>{summary.total_in_base_currency.toFixed(2)} {summary.base_currency}</b>
      </div>
    </div>
  );
}
