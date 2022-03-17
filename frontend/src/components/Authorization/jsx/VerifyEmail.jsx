import React from 'react'
// import '~/styles/VerifyEmail.styl'

function VerifyEmail() {
  return (
    <>
      <div className='verify__wrapper'>
        <h2>Подтверждение e-mail</h2>
        <p>Мы отправили письмо на электронную почту</p>
        <p id='verify__email'>{window.sessionStorage.getItem('email')}</p>
        <p>
          Для завершения регистрации перейдите по ссылке, указанной в письме.
          <br />
          Если письмо не пришло, пожалуйста, проверьте папку «Спам».
        </p>
        <div className='verify__email__text-bottom'>
          <p>Ошиблись в вводе данных?</p>
          <span>Введите корректный e-mail</span>
        </div>
      </div>
    </>
  )
}

export default VerifyEmail
