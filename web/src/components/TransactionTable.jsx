export default function TransactionTable({ items }) {
  return (
    <table className="table">
      <thead>
        <tr>
          {["#","ClientId","Service","Montant","Devise","Statut","Numéro","Date"].map(h=>(
            <th key={h}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {items.length === 0 && (
          <tr><td colSpan="8" style={{padding:16, textAlign:'center'}}>Aucune transaction</td></tr>
        )}
        {items.map(tx=>(
          <tr key={tx.id}>
            <td>{tx.id}</td>
            <td>{tx.client_id}</td>
            <td>{tx.service}</td>
            <td>{tx.amount}</td>
            <td>{tx.currency}</td>
            <td>{tx.status}</td>
            <td>{tx.tx_number}</td>
            <td>{new Date(tx.created_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
