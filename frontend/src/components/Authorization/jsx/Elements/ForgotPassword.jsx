import React from "react";
import {connect} from "react-redux";


function ForgotPassword(props) {
  return (
    <div className='auth__password-forgotten' 
         style={{ display: props.show ? 'block' : 'none' }}>
      <div className='auth__text'>Смена пароля</div>
      <form className='auth__form'>
        <div className='auth__form__input-wrapper'>
          <input className='form__input' 
                 name='email_password-forgotten' 
                 type='email' 
                 placeholder='E-mail' 
                 value={props.inputValue} 
                 onChange={props.onChange}/>
          <div className='auth__password-forgotten__text'>
            Ссылка на смену пароля будет выслана вам по e-mail
          </div>
        </div>

        <button className='btn' 
                type='submit' 
                onClick={props.onSubmit}>
          Продолжить
        </button>
        <h5 className='auth__password-forgotten__text-bottom' 
            onClick={props.signInShow}>
          Авторизоваться
        </h5>
      </form>
    </div>
  )
}

export default connect(
  state => ({}),
  dispatch => ({})
)(ForgotPassword)