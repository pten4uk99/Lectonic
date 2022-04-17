import React, {useEffect} from "react";
import Modal from "../../Layout/jsx/Modal";


function ConfirmAction(props) {
  return (
    <Modal onCancel={props.onCancel} styleBody={{maxWidth: 500, textAlign: 'center'}}>
      <div className="confirm-action">
        <span>{props.children || props.text}</span>
        <div className="btn btn-main btn-confirm" onClick={props.onConfirm}>Подтвердить</div>
      </div>
    </Modal>
  )
}

export default ConfirmAction