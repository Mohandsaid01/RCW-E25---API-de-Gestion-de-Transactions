import { useEffect, useState } from "react";
import api from "../api";

export default function NewTransaction() {
  const [clients, setClients] = useState([]);
  const [form, setForm] = useState({ client_id:"", service:"RIA", amount:"", currency:"CAD", tx_number:"", status:"En attente" });
  const [msg, setMsg] = useState("");

  useEffect(()=>{ (async()=>{ const { data } = await api.get("/clients"); setClients(data); })(); },[]);

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      const payload = { ...form, amount: parseFloat(form.amount) };
      const { data } = await api.post("/transactions", payload);
      setMsg(`Créé: TX #${data.id}`);
      setForm({ client_id:"", service:"RIA", amount:"", currency:"CAD", tx_number:"", status:"En attente" });
    } catch { setMsg("Erreur lors de la création"); }
  };

  return (
    <div className="container" style={{maxWidth:640}}>
      <h2 className="page-title">Nouvelle transaction</h2>
      <form className="form" onSubmit={submit}>
        <div>
          <div className="label">Client</div>
          <select className="select" value={form.client_id} onChange={e=>setForm({...form, client_id:e.target.value})} required>
            <option value="">-- Choisir --</option>
            {clients.map(c => <option key={c.id} value={c.id}>{c.name} ({c.country})</option>)}
          </select>
        </div>

        <div>
          <div className="label">Service</div>
          <select className="select" value={form.service} onChange={e=>setForm({...form, service:e.target.value})}>
            <option>RIA</option><option>WU</option><option>MG</option>
          </select>
        </div>

        <div>
          <div className="label">Montant</div>
          <input className="input" placeholder="Ex. 1200" value={form.amount} onChange={e=>setForm({...form, amount:e.target.value})} required />
        </div>

        <div>
          <div className="label">Devise</div>
          <input className="input" placeholder="Ex. CAD" value={form.currency} onChange={e=>setForm({...form, currency:e.target.value})}/>
        </div>

        <div>
          <div className="label">Numéro de transaction</div>
          <input className="input" placeholder="Ex. TX-0001" value={form.tx_number} onChange={e=>setForm({...form, tx_number:e.target.value})} required />
        </div>

        <div>
          <div className="label">Statut</div>
          <select className="select" value={form.status} onChange={e=>setForm({...form, status:e.target.value})}>
            <option>En attente</option><option>Validée</option><option>Annulée</option>
          </select>
        </div>

        <button className="btn" type="submit">Créer</button>
      </form>
      {msg && <div style={{marginTop:12}}>{msg}</div>}
    </div>
  );
}
