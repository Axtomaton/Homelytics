/* eslint-disable react/prop-types */
import { Component } from 'react';
import axios from 'axios';

export default class SearchBar extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      searchValue: '',
      optionsOpen: false, // State to track if options are open
      selectedState: 'NY', // State to store selected state
      stateMap: {}, 
      addressMap: {},
    };
  }

  async componentDidMount() {
    try {
      const states_data = await axios.get('http://localhost:8080/states');
      this.setState({stateMap: states_data.data});
      
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

  handleSubmit = async () => {
    const { searchValue, selectedState } = this.state;
    try {
      this.props.call_back(selectedState, searchValue);
    } catch (error) {
      console.error('Error setting value at endpoint:', error);
    }
  };

  toggleOptions = () => {
    this.setState((prevState) => ({ optionsOpen: !prevState.optionsOpen }));
  };

  render() {
    const { searchValue, optionsOpen, selectedState, stateMap } = this.state;

    return (
      <div style={{ display: 'flex', justifyContent: 'center', fontSize: '15px', marginBottom: '12px' }}>
        <div className="dropdown">
          <input
            type="search"
            className="form-control rounded"
            placeholder="Search"
            aria-label="Search"
            aria-describedby="search-addon"
            value={searchValue}
            onChange={this.handleChange}
            style={{ width: '200px', height: '40px', fontSize: '20px' }} // Increase width and height
          />
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
              style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)', top: '40px' }}
            >
              {Object.entries(stateMap).map(([abbr, name]) => (
                <button
                  key={abbr}
                  className="dropdown-item"
                  onClick={() => this.handleSelectState(abbr)}
                >
                </button>
              ))}
            </div>
          )}
        </div>
        <button
          type="button"
          className="btn btn-outline-primary ml-2"
          onClick={this.handleSubmit}
          style={{ fontSize: '20px', height: '40px' }} // Increase font size and height
        >
          Search
        </button>
      </div>
    );
  }
}
