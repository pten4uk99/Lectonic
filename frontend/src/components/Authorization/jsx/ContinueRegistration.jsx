import React, { useState } from 'react'
import Modal from '~@/Layout/jsx/Modal'
import AuthSignUpPassword from './AuthSignUpPassword'

function ContinueRegistration() {
  const [open, setOpen] = useState(true) //открыто модальное окно или нет

  return (
    <div>
      <Modal
        isOpened={open}
        onModalClose={() => setOpen(false)}
        styleBody={{ width: '400px' }}
      >
        <AuthSignUpPassword />
      </Modal>
      <div className="continue-register-main">
      </div>
    </div>
  )
}

export default ContinueRegistration
