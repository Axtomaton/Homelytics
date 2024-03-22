import React, { useEffect, useState } from 'react';
import axios from 'axios';
import SearchBar from './components/searchbar';
import Card from './components/card';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [view, setView] = useState("Normal");

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8080/');
      console.log('Response:', response); // Log the response
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  }

  async function call_back(state, city) {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8080/properties/${state}/${city}`);
      if (response.data.length === 0) {
        alert("No properties found for the given city and state");
      }
      else{
        setData(response.data);
      }
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

  function new_selection(newView) {
    console.log(newView);
    setView(newView);
  }

  return (
    <div>
      <SearchBar call_back={call_back} new_selection={new_selection} />
      <br />
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          {view === "Normal" && (
            <>
              {data.properties && Object.keys(data.properties).length > 0 ? (
                chunkArray(Object.keys(data.properties), 5).map((keyChunk, index) => (
                  <div
                    key={index}
                    className="card-container"
                    style={{ padding: '20px', backgroundColor: '#242124' }}
                  >
                    {keyChunk.map((key, idx) => (
                      <Card key={idx} propertyData={data.properties[key]} />
                    ))}
                  </div>
                ))
              ) : (
                <div
                  className="card-container"
                  style={{ padding: '20px', backgroundColor: '#242124' }}
                >
                  {Object.keys(data).map((key, idx) => (
                    <Card key={idx} propertyData={data[key]} />
                  ))}
                </div>
              )}
            </>
          )}
          {view === "Filtered" && (
            <>
              {data.filtered_properties && Object.keys(data.filtered_properties).length > 0 && (
                chunkArray(Object.keys(data.filtered_properties), 5).map((keyChunk, index) => (
                  <div
                    key={index}
                    className="card-container"
                    style={{ padding: '20px', backgroundColor: '#242124' }}
                  >
                    {keyChunk.map((key, idx) => (
                      <Card key={idx} propertyData={data.filtered_properties[key]} />
                    ))}
                  </div>
                ))
              )}
            </>
          )}
          {view === "Graph" && (
            <div>
              <h1>Graph View</h1>
            </div>
          )}
        </>
      )}
    </div>
  );
  
}

export default App;
