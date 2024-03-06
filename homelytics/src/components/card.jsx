/* eslint-disable react/prop-types */
import React from 'react';
import PropTypes from 'prop-types'; // Import PropTypes
import { Component } from "react"
class card extends Component{
  constructor(props){
    super(props)
    this.state = {
      address : props.address || "No address provided",
      bedrooms : props.bedrooms || "No bedrooms provided",
      bathrooms : props.bathrooms || "No bathrooms provided",
      price : props.price || "No price provided",
      image : props.price || "No image provided",
      href: props.href || "#",
      squareFeet: props.squareFeet || "No square feet provided",
    }
  }
  render (){
    return (
      <div className="card" style={{ 
        width: '281px', 
        height: '500px', 
        marginBottom: '20px', 
        backgroundColor: '#28282B',
        borderRadius: '10px', // Adjust the radius as needed
        overflow: 'hidden' 
      }}>
        <img 
          src="https://ik.imagekit.io/y7y0qqdyl/ImageNotAvailable.webp?updatedAt=1707595116136?tr=w-1080" 
          className="card-img-top" 
          alt="..." 
          style={{ 
            width: '281px', 
            height: '281px', 
            objectFit: 'cover',
            borderRadius: '10px 10px 0 0' // Only round the top corners of the image
          }} 
        />
        <div className="card-body" style={{ 
          padding: '10px', // 10px padding on all sides
          color: 'white'
        }}>
          <h3 className="card-title">{this.state.address}</h3>
          <p className="card-text">Some quick example text to build on the card title and make up the bulk of the content.</p>
          <a href="#" className="btn btn-primary">Go somewhere</a>
        </div>
      </div>
    );
  }
}
export default card;
