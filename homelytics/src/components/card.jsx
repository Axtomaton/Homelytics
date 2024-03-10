/* eslint-disable react/prop-types */
import { Component } from "react";

export default class Card extends Component {
  constructor(props) {
    super(props);
    this.state = {
      propertyData: {},
    };
  }

  async componentDidMount() {
    this.setState({ propertyData: this.props.propertyData });
    // console.log(this.props.propertyData); //works
  }

  render() {
    const { propertyData } = this.state;
    const { address } = this.props; // Extract the address (key) from props

    return (
      <div
        className="card"
        // key={address} // Use the address as the key prop
        style={{
          width: "281px",
          height: "500px",
          marginBottom: "20px",
          backgroundColor: "#28282B",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        {/* {console.log(this.props)} */}
        <img
          src="https://ik.imagekit.io/y7y0qqdyl/ImageNotAvailable.webp?updatedAt=1707595116136?tr=w-1080"
          className="card-img-top"
          alt="..."
          style={{
            width: "281px",
            height: "281px",
            objectFit: "cover",
            borderRadius: "10px 10px 0 0",
          }}
        />
        <div
          className="card-body"
          style={{
            padding: "10px",
            color: "white",
          }}
        >
          {/* Render property data here */}
          <h3 className="card-title">{propertyData.title}</h3>
          <p className="card-text">{propertyData.description}</p>
          <a href="#" className="btn btn-primary">
            Go somewhere
          </a>
        </div>
      </div>
    );
  }
}
