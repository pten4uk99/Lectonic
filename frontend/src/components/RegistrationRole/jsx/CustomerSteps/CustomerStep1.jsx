import React from 'react'
import {connect} from "react-redux";


function CustomerStep1(props) {
  return (
    <>
        <h2>Customer Step1</h2>
    </>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CustomerStep1);