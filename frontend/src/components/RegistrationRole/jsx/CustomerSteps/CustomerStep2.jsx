import React from 'react'
import {connect} from "react-redux";


function CustomerStep2(props) {
  return (
    <>
      <h2>Customer Step2</h2>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CustomerStep2);