import React, { Component } from 'react';
import axios from 'axios';
import "./searchbar.css"

export default class DuplicatedSearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchValue: '',
      optionsOpen: false, // check if state dropdown is open
      selectedState: 'NY', // default state
      stateMap: {}, 
      addressMap: {},
      selectedOption: 'normal', // default selected option
      // Adding new state for the duplicated dropdown menu
      duplicateOptionsOpen: false,
      SelectedViewState: 'Regular', // Set default to 'Regular'
    };
  }

  async componentDidMount() {
    try {
      const states_data = await axios.get('http://localhost:8080/states');
      this.setState({ stateMap: states_data.data });
    } catch (error) {
      console.error('Error fetching states data:', error);
    }
  }

  handleChange = (e) => {
    this.setState({ searchValue: e.target.value });
  };

  handleSelectState = (state) => {
    this.setState({ selectedState: state, optionsOpen: false });
  };

  handleViewChange = (state) => {
    this.setState({ SelectedViewState: state, duplicateOptionsOpen: false });
  };

  handleSubmit = async () => {
    const { searchValue, selectedState, selectedOption } = this.state;
    try {
      this.props.call_back(selectedState, searchValue, selectedOption);
    } catch (error) {
      console.error('Error setting value at endpoint:', error);
    }
  };

  handleDuplicateSubmit = async () => {
    // Add your functionality for the duplicated search button here
  };

  toggleOptions = () => {
    this.setState((prevState) => ({ optionsOpen: !prevState.optionsOpen }));
  };

  toggleDuplicateOptions = () => {
    this.setState((prevState) => ({ duplicateOptionsOpen: !prevState.duplicateOptionsOpen }));
  };

  handleSelectOption = (option, event) => {
    event.stopPropagation(); // Stop event propagation to prevent closing the dropdown
    this.setState({ selectedOption: option });
  };

  handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      this.handleSubmit();
    }
  };
  
  render() {
    const { searchValue, optionsOpen, selectedState, stateMap, selectedOption,
            duplicateOptionsOpen, SelectedViewState } = this.state;

    return (
      <div style={{ display: 'flex', justifyContent: 'center', fontSize: '15px', marginBottom: '12px'}}>
        {/* Original dropdown menu */}
        <div className="dropdown">
          <div className="input-group">
            <button
              className="btn btn-outline-primary dropdown-toggle"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              onClick={this.toggleOptions}
              style={{ fontSize: '20px', height: '40px' }} // Increase font size and height
            >
              {selectedState ? stateMap[selectedState] : 'Select State'}
            </button>
            {optionsOpen && (
              <div
                className="dropdown-menu show"
                aria-labelledby="dropdownMenuButton"
              >
                {Object.entries(stateMap).map(([abbr, name]) => (
                  <button
                    key={abbr}
                    className="dropdown-item"
                    onClick={() => this.handleSelectState(abbr)}
                    style={{ color: '#000' }} 
                  >
                    {name}
                  </button>
                ))}
              </div>
            )}
            <input
              type="search"
              className="form-control rounded"
              placeholder="Search"
              aria-label="Search"
              aria-describedby="search-addon"
              value={searchValue}
              onChange={this.handleChange}
              onKeyPress={this.handleKeyPress} // Call handleKeyPress function
            />
          </div>
        </div>
        {/* Original search button */}
        <button
          type="button"
          className="btn btn-outline-primary ml-2"
          onClick={this.handleSubmit}
        >
          Search
        </button>    

        {/* Duplicated dropdown menu */}
        <div className="dropdown">
          <div className="input-group">
            <button
              className="btn btn-outline-primary dropdown-toggle"
              type="button"
              id="dropdownMenuButtonDuplicate"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              onClick={this.toggleDuplicateOptions}
              style={{ fontSize: '20px', height: '40px' }} // Increase font size and height
            >
              {SelectedViewState ? SelectedViewState : 'Select Option'}
            </button>
            {duplicateOptionsOpen && (
              <div
                className="dropdown-menu show"
                aria-labelledby="dropdownMenuButtonDuplicate"
              >
                <button
                  className="dropdown-item"
                  onClick={() => this.handleViewChange('Regular')} // Change to appropriate value
                  style={{ color: '#000' }} 
                >
                  Regular
                </button>
                <button
                  className="dropdown-item"
                  onClick={() => this.handleViewChange('Filtered')} // Change to appropriate value
                  style={{ color: '#000' }} 
                >
                  Filtered
                </button>
                <button
                  className="dropdown-item"
                  onClick={() => this.handleViewChange('Graph')} // Change to appropriate value
                  style={{ color: '#000' }} 
                >
                  Graph
                </button>
              </div>
            )}
          </div>
        </div>
  
      </div>
    );
  }
}
