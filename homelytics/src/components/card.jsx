import { Component } from "react";
import "./card.css"
export default class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {
      propertyData: {},
      address: ""
    };
  }

  async componentDidMount() {
    this.setState({ propertyData: this.props.propertyData });
    // console.log(this.props.propertyData);
    this.setState({ address: this.props.address })
    // console.log(this.props.address); // Accessing the uniqueKey prop
  }

  render() {
    const { propertyData, address } = this.state;

    return (
      <div
        className="card"
        style={{backgroundColor : "#28282B"}}
      >
        <a href={propertyData.href} target="_blank" rel="noopener noreferrer">
          <img
            src={propertyData.img || "https://ik.imagekit.io/y7y0qqdyl/ImageNotAvailable.webp?updatedAt=1707595116136?tr=w-1080"}
            className="property-image" // Apply the class here
            alt="..."
          />
        </a>

        <div className="card-body">
        <h3 className="card-title card-text" style={{color: "white"}}>{address}</h3>
<div className="card-text-container">
  <img src="https://www.trulia.com/images/icons/txl3/BedIcon.svg" alt="Bed Icon" />
  <h8 className="card-text">{propertyData.Beds}</h8>
</div>
<div className="card-text-container">
  <img src="https://www.trulia.com/images/icons/txl3/BathIcon.svg" alt="Bath Icon" />
  <h8 className="card-text">{propertyData.Baths}</h8>
</div>
<h8 className="card-text">Price: ${propertyData.Price}</h8>
<h8 className="card-text">{propertyData.SquareFoot}</h8>
<div>
  <a>
    {propertyData.value && (
      <span className="card-text">
        Value: {propertyData.value}
      </span>
    )}
  </a>
</div>
</div>
      </div>
    );
  }
}
