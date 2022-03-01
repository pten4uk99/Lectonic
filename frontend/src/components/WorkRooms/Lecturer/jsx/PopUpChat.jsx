import React from 'react'
// import '../index.styl'
import closeIcon from '~/assets/img/icon-close.svg'

const PopUpChat = props => {
  return (
    <div
      className={`Smodal__wrapper ${props.isOpened ? 'open' : 'close'}`}
      style={{ ...props.styleWrapper }}
    >
      <div className='Smodal__body' style={{ ...props.styleBody }}>
        <img
          className='Smodal__close'
          src={closeIcon}
          alt='закрыть'
          onClick={props.onModalClose}
        />

        {props.children}
      </div>
    </div>
  )
}

export default PopUpChat
