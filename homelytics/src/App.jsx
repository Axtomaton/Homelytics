import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';
import SearchBar from './components/searchbar';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/properties');
        console.log(response);
        if (response.status === 200) {
          console.log('Data fetched:', response.data);
          setData(response.data);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    fetchData();
  }, []);



  return (
    <div>
      <SearchBar/>
      <h1>Hello from React!</h1>
      <h2>blsaasj</h2>
      {/* Display data from the server */}
      <p>{data.message}</p> {/* Display the message from the server */}
      
    </div>
  );
}

export default App;
