import React, {useEffect} from 'react'

import closeIcon from '~/assets/img/icon-close.svg'
import {connect} from "react-redux";
import {ActivateModal, DeactivateModal} from "../redux/actions/header";
import {SetCheckedDate} from "../../WorkRooms/FullCalendar/Calendar/redux/actions/calendar";


function Modal(props) {
  
  function handleCancel() {
    if (props.onCancel) props.onCancel()
    props.DeactivateModal()
  }
  
  return props.store.header.modalActive && (
    <div className='modal__background'
         style={props.styleWrapper}>
      <div className='modal__wrapper' style={props.styleBody}>
        <div className="block__close-icon">
          <img className='modal__close' 
             src={closeIcon} 
             alt='закрыть' 
             onClick={handleCancel}/>
        </div>
        <div className="modal__body">
          {props.children}
        </div>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal()),
    SetCheckedDate: (date) => dispatch(SetCheckedDate(date))
  })
)(Modal)
