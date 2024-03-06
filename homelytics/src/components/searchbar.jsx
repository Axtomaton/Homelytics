import React, { Component } from 'react';
import axios from 'axios';

const stateMap = {
  "AL": "Alabama",
  "AK": "Alaska",
  "AZ": "Arizona",
  "AR": "Arkansas",
  "CA": "California",
  "CO": "Colorado",
  "CT": "Connecticut",
  "DE": "Delaware",
  "DC": "District Of Columbia",
  "FL": "Florida",
  "GA": "Georgia",
  "HI": "Hawaii",
  "ID": "Idaho",
  "IL": "Illinois",
  "IN": "Indiana",
  "IA": "Iowa",
  "KS": "Kansas",
  "KY": "Kentucky",
  "LA": "Louisiana",
  "ME": "Maine",
  "MD": "Maryland",
  "MA": "Massachusetts",
  "MI": "Michigan",
  "MN": "Minnesota",
  "MS": "Mississippi",
  "MO": "Missouri",
  "MT": "Montana",
  "NE": "Nebraska",
  "NV": "Nevada",
  "NH": "New Hampshire",
  "NJ": "New Jersey",
  "NM": "New Mexico",
  "NY": "New York",
  "NC": "North Carolina",
  "ND": "North Dakota",
  "OH": "Ohio",
  "OK": "Oklahoma",
  "OR": "Oregon",
  "PA": "Pennsylvania",
  "RI": "Rhode Island",
  "SC": "South Carolina",
  "SD": "South Dakota",
  "TN": "Tennessee",
  "TX": "Texas",
  "UT": "Utah",
  "VT": "Vermont",
  "VA": "Virginia",
  "WA": "Washington",
  "WV": "West Virginia",
  "WI": "Wisconsin",
  "WY": "Wyoming"
};

export default class SearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchValue: '',
      optionsOpen: false, // State to track if options are open
      selectedState: 'NY', // State to store selected state
    };
  }

  handleChange = (e) => {
    this.setState({ searchValue: e.target.value });
  };

  handleSelectState = (state) => {
    this.setState({ selectedState: state, optionsOpen: false });
  };

  handleSubmit = () => {
    const { searchValue, selectedState } = this.state;
    // console.log('Search value:', searchValue);
    // console.log('Selected state:', selectedState);
    this.props.callback(selectedState, searchValue);
  };

  toggleOptions = () => {
    this.setState((prevState) => ({ optionsOpen: !prevState.optionsOpen }));
  };

  render() {
    const { searchValue, optionsOpen, selectedState } = this.state;

    return (
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <div className="dropdown">
          <input
            type="search"
            className="form-control rounded"
            placeholder="Search"
            aria-label="Search"
            aria-describedby="search-addon"
            value={searchValue}
            onChange={this.handleChange}
          />
          <button
            className="btn btn-outline-primary dropdown-toggle"
            type="button"
            id="dropdownMenuButton"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            onClick={this.toggleOptions}
          >
            {selectedState ? stateMap[selectedState] : 'Select State'}
          </button>
          {/* Dropdown menu for states */}
          {optionsOpen && (
            <div
              className="dropdown-menu show"
              aria-labelledby="dropdownMenuButton"
              style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)', top: '40px' }}
            >
              {Object.entries(stateMap).map(([abbr, name]) => (
                <button
                  key={abbr}
                  className="dropdown-item"
                  onClick={() => this.handleSelectState(abbr)}
                >
                  {name}
                </button>
              ))}
            </div>
          )}
        </div>
        <button
          type="button"
          className="btn btn-outline-primary ml-2"
          onClick={this.handleSubmit}
        >
          Search
        </button>
      </div>
    );
  }
}
