import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';
import SearchBar from './components/searchbar';
import Card from './components/card';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    try {
      const response = await axios.get('http://localhost:8080/');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  async function call_back(state, searchValue) {
    try {
      const response = await axios.get(`http://localhost:8080/properties/${state}`, {
        params: {
          search: searchValue,
        },
      });
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
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
    <div>
      <SearchBar call_back={call_back}/>
      <br />
      <div>
        {data &&
          chunkArray(Object.values(data), 5).map((chunk, index) => (
            <div
              key={index}
              className="card-container"
              style={{ padding: '20px', marginTop: index > 0 ? '-25px' : '0' }}
            > 
              {chunk.map((propertyData, idx) => (
                <Card key={idx} propertyData={propertyData} />
              )
              )}

            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
