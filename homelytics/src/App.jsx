import { useEffect, useState } from 'react';
import axios from 'axios';
import SearchBar from './components/searchbar';
import Card from './components/card';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; // Import your CSS file here

function App() {
  const [data, setData] = useState({});
  const [address, setAddress] = useState([]);
  const [loading, setLoading] = useState(false); // Add loading state

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8080/');
      setData(Object.values(response.data));
      setAddress(Object.keys(response.data));
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }

  async function call_back(state, searchValue) {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8080/properties/${state}`, {
        params: {
          search: searchValue,
        },
      });
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }

  function chunkArray(arr, chunkSize) {
    const chunks = [];
    for (let i = 0; i < arr.length; i += chunkSize) {
      chunks.push(arr.slice(i, i + chunkSize));
    }
    return chunks;
  }

  return (
    <div style={{ backgroundColor: '#1b1b1b'}}>
      <SearchBar call_back={call_back} />
      <br />
      {loading ? ( // Display loading state
        <div>Loading...</div>
      ) : (
        Object.keys(data).length > 0 &&
        chunkArray(Object.keys(data), 5).map((keyChunk, index) => (
          <div
            key={index}
            className="card-container"
            style={{ padding: '20px', marginTop: index > 0 ? '-25px' : '0', backgroundColor: 'brown' }}
          >
            {keyChunk.map((key, idx) => (
              <Card key={idx} propertyData={data[key]} address={address[index * 5 + idx]} />
            ))}
          </div>
        ))
      )}
    </div>
  );
}

export default App;
