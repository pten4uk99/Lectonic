import React from 'react'
import {connect} from "react-redux";


function CompanyStep2(props) {
  return (
    <>
      <h2>Company Step2</h2>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CompanyStep2);