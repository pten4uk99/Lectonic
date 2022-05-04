import React from "react";
import {connect} from "react-redux";
import {getProfileBgc} from "../../../ProjectConstants";


function PhotoName({firstName, lastName, size, colorNumber}) {
  let first = firstName?.slice(0, 1)
  let last = lastName?.slice(0, 1)
  let fontSize = size / 2.6
  
  if (!colorNumber) console.error('Не передан номер цвета')
  
  return (
    <div className="photo-name__wrapper" 
         style={{
           width: size,
           height: size,
           fontSize: fontSize,
           backgroundColor: getProfileBgc(colorNumber)
    }}>
      <span>{first && first.toUpperCase()}</span>
      <span>{last && last.toUpperCase()}</span>
    </div>
  )
}

export default connect(
  state => ({}),
  dispatch => ({})
)(PhotoName)