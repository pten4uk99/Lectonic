import React from "react";
import {connect} from "react-redux";


function PhotoName(props) {
  let firstName = props.firstName[0]
  let lastName = props.lastName[0]
  let fontSize = props.size / 2.6
  return (
    <div className="photo-name__wrapper" 
         style={{width: props.size, height: props.size, fontSize: fontSize}}>
      <span>{firstName && firstName.toUpperCase()}</span>
      <span>{lastName && lastName.toUpperCase()}</span>
    </div>
  )
}

export default connect(
  state => ({}),
  dispatch => ({})
)(PhotoName)