import { useEffect, useState } from 'react';
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
      console.log('Response:', response);
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
      // console.log('Response:', response);
      if (response.data.length === 0) {
        alert("No properties found for the given city and state");
      } else {
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
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
          <div className="spinner-border" style={{ width: '5rem', height: '5rem' }} role="status">
              <span className="visually-hidden">Loading...</span>
          </div>
          <div style={{ marginTop: '1rem' }}>Loading...</div>
        </div>     
        
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
          <div className="container">
              <div className="chart-container">
                  <img
                      src={`http://localhost:8080/charts/${data.chart_id}`}
                      alt="Chart"
                  />
              </div>
              <div className="stats-container">
                  <div className="card-body">
                      <h5 className="card-title">Statistics</h5>
                      <ul className="list-group list-group-flush">
                          <li className="list-group-item">Median Price: {data.basic_stats['Median Price']}</li>
                          <li className="list-group-item">Standard Deviation of Price: {data.basic_stats['Standard Deviation of Price'].toFixed(2)}</li>
                          <li className="list-group-item">Minimum Price: {data.basic_stats['Minimum Price']}</li>
                          <li className="list-group-item">Maximum Price: {data.basic_stats['Maximum Price']}</li>
                          <li className="list-group-item">Median Value Score: {data.median_value_score.toFixed(2)}</li>
                      </ul>
                  </div>
              </div>
          </div>
      )}
        </>
      )}
    </div>
  );
}

export default App;
