import { useEffect, useState } from 'react';
import axios from 'axios';
export default function Admin() {
  const [subs, setSubs] = useState([]);
  useEffect(()=> {
    const f = async ()=> {
      try {
        const res = await axios.get((process.env.NEXT_PUBLIC_BACKEND_URL||'http://localhost:8000') + '/submissions');
        setSubs(res.data || []);
      } catch(e) { console.error(e) }
    }
    f();
  },[]);
  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>Submissions</h1>
      <table border="1" cellPadding="6">
        <thead><tr><th>ID</th><th>Name</th><th>PAN</th><th>Aadhaar</th><th>PIN</th><th>City</th><th>State</th></tr></thead>
        <tbody>
          {subs.map(s=>(
            <tr key={s.id}><td>{s.id}</td><td>{s.name}</td><td>{s.pan}</td><td>{s.aadhaar}</td><td>{s.pin}</td><td>{s.city}</td><td>{s.state}</td></tr>
          ))}
        </tbody>
      </table>
      <a href="/">Back</a>
    </div>
  );
}
