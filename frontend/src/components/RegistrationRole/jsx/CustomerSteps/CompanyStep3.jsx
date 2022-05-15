import React from 'react'
import {connect} from "react-redux";


function CompanyStep3(props) {
  return (
    <>
      <h2>Company Step3</h2>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CompanyStep3);