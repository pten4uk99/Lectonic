import React from 'react'
import mainIllustration from '~/assets/img/main-illustration.svg'
import {ActivateModal, DeactivateModal} from "../redux/actions/header";
import {connect} from "react-redux";

function Main(props) {
  return (
    <>
      <div className="main">
        <div className="main__text-wrapper">
          <p className="main__text-header">
            Платформа для лекторов
            <br />и не только!
          </p>
          <p className="main__text">
            Работаем, чтобы слушатели слышали,
            <br />а лекторы читали.
          </p>
          <button className="btn main__btn" onClick={props.ActivateModal}>
            Присоединиться
          </button>
        </div>
        <div className="main__illustration-wrapper">
          <img
            className="main__illustration"
            src={mainIllustration}
            alt="Иллюстрация"
          />
        </div>
      </div>
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(Main)