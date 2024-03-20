import { useEffect, useState } from 'react';
import axios from 'axios';
import SearchBar from './components/searchbar';
import Card from './components/card';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; 

function App() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false); // Add loading state
  // const [graph, setgraph] = useState("");
  const [view, setView] = useState("Normal"); //options are Normal, Filtered, and Graph


  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8080/');
      setData(Object.values(response.data));
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }

  async function call_back(state, city) {
    // console.log(state, city)
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8080/properties/${state}/${city}`, {});
      console.log(response.data)
      // const 
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

function new_selection(newView){
  this.setState({view: newView})}
  

  return (
    <div>
      <SearchBar call_back={call_back} new_selection={new_selection} />
      <br/>
      {loading ? ( // Display loading state
        <div>Loading...</div>
      ) : (
        Object.keys(data).length > 0 &&
        chunkArray(Object.keys(data), 5).map((keyChunk, index) => (
          <div
            key={index}
            className="card-container"
            style={{ padding: '20px', backgroundColor: '#242124' }}
          >
            {keyChunk.map((key, idx) => (
              <Card key={idx} propertyData={data[key]} />
            ))}
          </div>
        ))
      )}
    </div>
  );
}

export default App;
