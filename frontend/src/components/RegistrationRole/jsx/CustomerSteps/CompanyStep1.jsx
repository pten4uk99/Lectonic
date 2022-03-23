import React from 'react'
import {connect} from "react-redux";


function CompanyStep1(props) {
  return (
    <>
      <h2>Company Step1</h2>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CompanyStep1);