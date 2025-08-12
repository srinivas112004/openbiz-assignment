// Main form page - dynamically renders schema into a 2-step form
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function Home(){
  const [schema, setSchema] = useState([]);
  const [data, setData] = useState({});
  const [message, setMessage] = useState('');
  const [step, setStep] = useState(1);
  const [pinMap, setPinMap] = useState({});

  useEffect(()=> {
    const fetchSchema = async () => {
      try {
        const res = await axios.get((process.env.NEXT_PUBLIC_BACKEND_URL||'http://localhost:8000') + '/schema');
        setSchema(res.data || []);
      } catch(e) { console.error(e) }
    }
    const fetchPin = async () => {
      try {
        const res = await axios.get('/pin_map.json');
        setPinMap(res.data || {});
      } catch(e){ console.error(e) }
    }
    fetchSchema();
    fetchPin();
  },[]);

  const handleChange = (e) => {
    const {name, value} = e.target;
    setData({...data, [name]: value});
    // Autofill city/state when PIN exists in offline map
    if(name === 'pin' && pinMap[value]){
      setData(prev=>({...prev, city: pinMap[value].city, state: pinMap[value].state}));
    }
  }

  const handleNext = (e) => { e.preventDefault(); setStep(2); window.scrollTo(0,0); }
  const handleBack = (e) => { e.preventDefault(); setStep(1); window.scrollTo(0,0); }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try{
      const res = await axios.post((process.env.NEXT_PUBLIC_BACKEND_URL||'http://localhost:8000') + '/submit', data);
      setMessage('Submitted id=' + res.data.id);
    } catch(err){
      setMessage('Error: ' + (err.response?.data?.detail || err.message));
    }
  }

  const stepFields = (s) => schema.filter(f => {
    // simple split: if field name includes 'aadhaar' or 'pan' map to step1/step2; otherwise if pin/city/state in step2
    const n = (f.name || f.id || '').toLowerCase();
    if(s===1) return n.includes('aadhaar') || n.includes('pan') || n.includes('name');
    return n.includes('pin') || n.includes('city') || n.includes('state') || n.includes('email') || (!n.includes('aadhaar') && !n.includes('pan') && !n.includes('name'));
  });

  return (
    <div className="container">
      <h1>Udyam-like Dynamic Form</h1>
      <div style={{marginBottom:12}}>
        <strong>Step {step} of 2</strong>
        <div style={{height:8, background:'#eee', borderRadius:4, overflow:'hidden', marginTop:6}}>
          <div style={{width: step===1 ? '50%' : '100%', height:8, background:'#4caf50'}}></div>
        </div>
      </div>

      <form onSubmit={step===1?handleNext:handleSubmit}>
        { (step===1 ? stepFields(1) : stepFields(2)).map(f=>(
          <div key={f.name||f.id} style={{marginBottom:10}}>
            <label>{f.label || f.name || f.id}</label><br/>
            { f.options ? (
              <select name={f.name||f.id} onChange={handleChange}>
                <option value="">Select</option>
                {f.options.map(o=><option key={o.value} value={o.value}>{o.text}</option>)}
              </select>
            ) : (
              <input name={f.name||f.id} onChange={handleChange} placeholder={f.label} />
            )}
          </div>
        ))}

        <div style={{marginTop:12}}>
          { step===1 ? <button type="submit">Next</button> : <><button onClick={handleBack}>Back</button> <button type="submit">Submit</button></> }
        </div>
      </form>

      {message && <p>{message}</p>}
      <hr/>
      <a href="/admin">Admin View</a>
    </div>
  );
}
