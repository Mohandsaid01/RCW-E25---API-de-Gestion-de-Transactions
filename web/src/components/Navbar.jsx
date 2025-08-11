import { Link, useNavigate } from "react-router-dom";
import { isAuthenticated, logout } from "../auth";

export default function Navbar() {
  const nav = useNavigate();
  return (
    <nav className="navbar">
      <Link to="/">Dashboard</Link>
      <Link to="/transactions">Transactions</Link>
      <Link to="/new">Nouvelle transaction</Link>
      <Link to="/clients/new">Nouveau client</Link>
      <div className="navbar__spacer">
        {isAuthenticated()
          ? <button className="btn btn--danger" onClick={()=>{logout();nav("/login");}}>Se déconnecter</button>
          : <Link to="/login">Se connecter</Link>}
      </div>
    </nav>
  );
}
