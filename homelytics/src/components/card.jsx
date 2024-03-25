import { Component } from "react";
import "./card.css"


function formatPrice(price) {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export default class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {
      propertyData: {},
    };
  }

  async componentDidMount() {
    this.setState({ propertyData: this.props.propertyData});
    // console.log(this.props.propertyData);
    // console.log(this.props.address); // Accessing the uniqueKey prop
  }

  

  render() {
    const { propertyData } = this.state;

    return (
      <div
        className="card"
        style={{backgroundColor : "#28282B"}}
      >
        <a href={propertyData.href} target="_blank" rel="noopener noreferrer">
          <img
            src={propertyData.img || "https://ik.imagekit.io/y7y0qqdyl/ImageNotAvailable.webp?updatedAt=1707595116136?tr=w-1080"}
            className="property-image" 
            alt="..."
          />
        </a>

        <div className="card-body">
        <h3 className="card-title card-text" style={{color: "white"}}>{propertyData.Address}</h3>



    <div className="card-text-container">
      <div className="bed-container">
        <img src="https://www.trulia.com/images/icons/txl3/BedIcon.svg" alt="Bed Icon" />
        <h6 className="card-text">{propertyData.Beds}</h6>
      </div>
      <div className="bath-container">
        <img src="https://www.trulia.com/images/icons/txl3/BathIcon.svg" alt="Bath Icon" />
        <h6 className="card-text">{propertyData.Baths}</h6>
      </div>
    </div>


<h6 className="card-text">Price: ${propertyData.Price}</h6>
<h6 className="card-text">
  {propertyData.SquareFoot !== "Undisclosed" && (
    <>
      Square Foot: {propertyData.SquareFoot}
    </>
  )}
</h6><div>
  <a>
    {propertyData["Value Score"] && (
      <span className="card-text">
        Value: {propertyData["Value Score"].toFixed(2)}
      </span>
    )}
  </a>
</div>
</div>
      </div>
    );
  }
}
