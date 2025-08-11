import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import NewTransaction from "./pages/NewTransaction";
import PrivateRoute from "./components/PrivateRoute";
import NewClient from "./pages/NewClient";
export default function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/" element={<PrivateRoute><Dashboard/></PrivateRoute>} />
        <Route path="/transactions" element={<PrivateRoute><Transactions/></PrivateRoute>} />
        <Route path="/new" element={<PrivateRoute><NewTransaction/></PrivateRoute>} />
                <Route path="/clients/new" element={<PrivateRoute><NewClient/></PrivateRoute>} />
      </Routes>
    </BrowserRouter>
  );
}
