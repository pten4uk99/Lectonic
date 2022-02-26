import React from 'react'
// import '~/styles/Modal.styl'
import closeIcon from '~/assets/img/icon-close.svg'

const Modal = props => {
  return (
    <div
      className={`modal__wrapper ${props.isOpened ? 'open' : 'close'}`}
      style={{ ...props.styleWrapper }}
    >
      <div className='modal__body' style={{ ...props.styleBody }}>
        <img
          className='modal__close'
          src={closeIcon}
          alt='закрыть'
          onClick={props.onModalClose}
        />

        {props.children}
      </div>
    </div>
  )
}

export default Modal
