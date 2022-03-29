import React from "react";
import {connect} from "react-redux";

import errorIcon from '~/assets/img/error-message-icon.svg'

function ErrorMessage(props) {
  let message = props.store.header.errorMessage
  return (
    <div className="header__error-message">
      <img src={errorIcon} alt=""/>
      <span>Ошибка сервера: {message}</span>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(ErrorMessage)