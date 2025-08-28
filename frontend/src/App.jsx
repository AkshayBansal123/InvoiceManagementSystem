


import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [invoices, setInvoices] = useState([]);

  const uploadInvoice = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://127.0.0.1:8000/upload-invoice/", formData);
    alert(res.data.message);
    fetchInvoices();
  };

  const fetchInvoices = async () => {
    const res = await axios.get("http://127.0.0.1:8000/invoices/");
    setInvoices(res.data.invoices);
  };

  useEffect(() => {
    fetchInvoices();
  }, []);

  const exportCSV = async () => {
    await axios.get("http://127.0.0.1:8000/export-csv/");
    alert("CSV exported!");
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>📄 Invoice Manager (MVP)</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadInvoice}>Upload Invoice</button>
      <button onClick={exportCSV}>Export CSV</button>

      <h2>Invoices</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Vendor</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map((inv) => (
            <tr key={inv[0]}>
              <td>{inv[0]}</td>
              <td>{inv[1]}</td>
              <td>{inv[2]}</td>
              <td>{inv[3]}</td>
              <td>{inv[4]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

