import React, { Component } from 'react';
import axios from 'axios';
export default class SearchBar extends Component {

    constructor(props) {
        super(props);
        this.state = {
          searchValue: '' // Initialize search value state
        };
    }

    handleChange = (e) => {
        this.setState({searchValue: e.target.value});
    }
    
    handleSubmit = () => {
        const { searchValue } = this.state;
        console.log('Search value:', searchValue);
        axios.get(`http://localhost:8000/properties/${searchValue}`)
        // Perform action with the search value (e.g., submit it to the server)
    };

    render() {
        return (
          <div>
          <div style={{ display: 'flex', justifyContent: 'center' }}>           
          <input
                type="search"
                className="form-control rounded"
                placeholder="Search"
                aria-label="Search"
                aria-describedby="search-addon"
                value={this.state.searchValue}
                onChange={this.handleChange} 
            />
              <button
                type="button"
                className="btn btn-outline-primary"
                data-mdb-ripple-init
                onClick={this.handleSubmit} 
              >
                Search
              </button>
            </div>
          </div>
        );
      }
    }
