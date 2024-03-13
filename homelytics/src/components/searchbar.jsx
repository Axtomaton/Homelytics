import { Component } from 'react';
import axios from 'axios';
import "./searchbar.css"
export default class SearchBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchValue: '',
      optionsOpen: false, // check if dropdown is open
      selectedState: 'NY', // default state
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
      <div style={{ display: 'flex', justifyContent: 'center', fontSize: '15px', marginBottom: '12px'}}>
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
            />
          </div>
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
