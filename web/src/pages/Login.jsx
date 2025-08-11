import { useState } from "react";
import api from "../api";
import { login as doLogin } from "../auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("admin@rcw.local");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);
      const { data } = await api.post("/auth/login", form, {
        headers: {"Content-Type":"application/x-www-form-urlencoded"}
      });
      doLogin(data.access_token);
      nav("/");
    } catch {
      setError("Échec de connexion");
    }
  };

  return (
    <div style={{maxWidth:360, margin:"48px auto"}}>
      <h2>Connexion</h2>
      <form onSubmit={submit} style={{display:"grid", gap:8}}>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Mot de passe" />
        <button type="submit">Se connecter</button>
        {error && <div style={{color:"red"}}>{error}</div>}
      </form>
    </div>
  );
}
