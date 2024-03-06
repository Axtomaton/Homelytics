import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';
import SearchBar from './components/searchbar';
import Card from './components/card';
function App() {


  const [data, setData] = useState({}); //stored pandas dataframe

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

  function callback(state, searchValue) {
    axios.get('http://localhost:8000/properties', {
      params: {
        state: state,
        search: searchValue,
      },
    })
      .then((response) => {
        console.log('Data fetched:', response.data);
        setData(response.data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }

  return (
    <div>
      <SearchBar callback={callback}/>
      <h1>Hello from React!</h1>
      <h2>blsaasj</h2>
      <div className="card-container" style={{padding : "20px"}}> 
        <Card address="Apple" />
        <Card address="Tree" />
        <Card address="1" /> 
        <Card address="2" /> 
        <Card address="3" /> 
        <Card address="4!" /> 
      </div>
      <div className="card-container" style={{ marginTop: '-25px', padding : "20px" }}>        
        <Card address="G" />
        <Card address="H" />
        <Card address="J" /> 
        <Card address="X" /> 
        <Card address="A" /> 
        <Card address="X!" /> 
      </div>
    </div>
  );
}

export default App;
