import React from 'react'

import closeIcon from '~/assets/img/icon-close.svg'
import {connect} from "react-redux";
import {ActivateModal, DeactivateModal} from "../redux/actions/header";


function Modal(props) {
  return (
    <div className={`modal__wrapper ${props.store.header.modalActive ? 'open' : 'close'}`} 
         style={{ ...props.styleWrapper }}>
      <div className='modal__body' style={{ ...props.styleBody }}>
        <img className='modal__close' 
             src={closeIcon} 
             alt='закрыть' 
             onClick={props.DeactivateModal}/>

        {props.children}
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(Modal)
