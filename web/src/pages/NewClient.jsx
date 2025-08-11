import { useState } from "react";
import api from "../api";

export default function NewClient() {
  const [form, setForm] = useState({ name: "", country: "CA", document_id: "" });
  const [msg, setMsg] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setMsg("");
    try {
      const payload = { name: form.name, country: form.country };
      if (form.document_id) payload.document_id = form.document_id;
      const { data } = await api.post("/clients", payload);
      setMsg(`Client créé: #${data.id} — ${data.name}`);
      setForm({ name: "", country: "CA", document_id: "" });
    } catch (err) {
      setMsg("Erreur lors de la création du client");
    }
  };

  return (
    <div className="container" style={{maxWidth: 640}}>
      <h2 className="page-title">Nouveau client</h2>

      <form className="form" onSubmit={submit}>
        <div>
          <div className="label">Nom complet</div>
          <input
            className="input"
            placeholder="Ex. Jean Dupont"
            value={form.name}
            onChange={(e)=>setForm({...form, name: e.target.value})}
            required
          />
        </div>

        <div>
          <div className="label">Pays</div>
          <input
            className="input"
            placeholder="Ex. CA"
            value={form.country}
            onChange={(e)=>setForm({...form, country: e.target.value})}
            required
          />
        </div>

        <div>
          <div className="label">Document / Référence (optionnel)</div>
          <input
            className="input"
            placeholder="Ex. CNI123 / Tel / Passeport"
            value={form.document_id}
            onChange={(e)=>setForm({...form, document_id: e.target.value})}
          />
        </div>

        <button className="btn" type="submit">Créer le client</button>
      </form>

      {msg && <div style={{marginTop:12}}>{msg}</div>}
    </div>
  );
}

