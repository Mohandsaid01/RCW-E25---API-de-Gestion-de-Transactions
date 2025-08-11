import { useEffect, useState } from "react";
import api from "../api";
import TransactionTable from "../components/TransactionTable";

export default function Transactions() {
  const [items, setItems] = useState([]);
  const [filters, setFilters] = useState({ client_name:"", service:"", status:"" });

  const load = async () => {
    const params = {};
    if (filters.client_name) params.client_name = filters.client_name;
    if (filters.service) params.service = filters.service;
    if (filters.status) params.status = filters.status;
    const { data } = await api.get("/transactions", { params });
    setItems(data);
  };

  useEffect(()=>{ load(); },[]);

  return (
    <div style={{padding:16}}>
      <h2>Transactions</h2>
      <div style={{display:"flex", gap:8, marginBottom:12}}>
        <input placeholder="Client" value={filters.client_name} onChange={e=>setFilters({...filters, client_name:e.target.value})}/>
        <select value={filters.service} onChange={e=>setFilters({...filters, service:e.target.value})}>
          <option value="">Service</option><option>RIA</option><option>WU</option><option>MG</option>
        </select>
        <select value={filters.status} onChange={e=>setFilters({...filters, status:e.target.value})}>
          <option value="">Statut</option><option>En attente</option><option>Validée</option><option>Annulée</option>
        </select>
        <button onClick={load}>Rechercher</button>
      </div>
      <TransactionTable items={items}/>
    </div>
  );
}
