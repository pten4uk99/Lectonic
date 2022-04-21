import React from "react";
import {connect} from "react-redux";

import errorIcon from '~/assets/img/error-message-icon.svg'
import Loader from "./Loader";

function ErrorMessage(props) {
  return (
    <div className="header__error-message">
      <img src={errorIcon} alt=""/>
      <span>{props.msg}</span>
      <Loader size={15} left={12}/>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(ErrorMessage)