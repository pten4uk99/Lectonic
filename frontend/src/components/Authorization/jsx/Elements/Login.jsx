import React, {useState} from "react";
import {connect} from "react-redux";

import eyeOpen from '~/assets/img/eye-open.svg'
import eyeClose from '~/assets/img/eye-close.svg'
import Loader from "../../../Utils/jsx/Loader";


function Login(props) {
  const [hiddenSignIn, setHiddenSignIn] = useState(true)
  const [loggedIn, setLoggedIn] = useState(false)
  
  function handleHiddenSignIn() {
    setHiddenSignIn(!hiddenSignIn)
  }
  function onChangeLoggedIn() {
    setLoggedIn(!loggedIn)
  }
  
  return (
    <div style={{ display: props.show ? 'block' : 'none' }}>
      <div className='auth__text'>Войдите в свой аккаунт</div>
      <form className='auth__form'>
        <div className='auth__form__input-wrapper'>
          <input className='form__input' name='email' 
                 type='email' 
                 placeholder='E-mail' 
                 value={props.inputValue.email} 
                 onChange={props.onEmailChange} 
                 style={{borderBottom: props.errorMessages.email ? '1px solid var(--add-pink)' : '',}}/>
          {props.errorMessages.email && (<div className='form__input-error'>{props.errorMessages.email}</div>)}
        </div>

        <div className='auth__form__input-wrapper'>
          <input className='form__input' 
                 name='password' 
                 type={hiddenSignIn ? 'password' : 'text'} 
                 placeholder='Пароль' 
                 value={props.inputValue.password} 
                 onChange={props.onPasswordChange} 
                 style={{borderBottom: props.errorMessages.password ? '1px solid var(--add-pink)' : '',}}/>
          <img className='password-icon' 
               src={hiddenSignIn ? eyeClose : eyeOpen} 
               alt={hiddenSignIn ? 'показать' : 'скрыть'} 
               onClick={handleHiddenSignIn}/>
          {props.errorMessages.password && 
            <div className='form__input-error'>{props.errorMessages.password}</div>}
        </div>
        
        <div className="auth__form__bottom-block">
          <div className='auth__form__password-forgotten' 
               onClick={props.handleForgotPassword}>
            Забыли пароль?
          </div>
  
          <div className='auth__form__checkbox-wrapper signIn'>
            <input className='auth__form__checkbox-switch' 
                   id='checkbox' 
                   type='checkbox' 
                   checked={loggedIn} 
                   onChange={onChangeLoggedIn}/>
            <label htmlFor='checkbox'>Не выходить из системы</label>
          </div>
        </div>

        <button className='btn auth__form__btn' 
                type='submit' 
                onClick={props.onSubmit}>
          {!props.requestLoaded ? 
            <Loader size={20} 
                    left="50%" 
                    top="50%" 
                    tX="-50%" tY="-50%"/> : 
            "Войти"}
        </button>
      </form>

      {/* пока вход через соц сети не используется
              <div className="auth__socials">
                  <span>или</span>
                  <button className="auth__socials__btn-google"><public src={require("~/public/google-icon.svg").default}/>Войти через Google</button>
                  <button className="auth__socials__btn-fb"><public src={require("~/public/fb-icon.svg").default}/>Войти через Facebook</button>
                  <button className="auth__socials__btn-vk"><public src={require("~/public/vk-icon.svg").default}/>Войти через VK</button>
              </div> */}

      <div className='auth__bottom-text'>
        Ещё нет аккаунта?{' '}
        <span onClick={props.signUpShow}>Зарегистрироваться</span>
      </div>
    </div>
  )
}

export default connect(
  state => ({}),
  dispatch => ({})
)(Login)