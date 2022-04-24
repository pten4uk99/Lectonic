import React, {useState} from "react";
import {connect} from "react-redux";
import Loader from "../../../Utils/jsx/Loader";


function SignUp(props) {
  return (
    <div style={{display: props.show ? 'block' : 'none'}}>
      <div className='auth__text'>Для регистрации введите Ваш E-mail</div>
      <form className='auth__form'>
        <div className='input-wrapper__signup-email'>
          <input className='form__input signUpEmail' 
                 name='email' 
                 type='email' 
                 placeholder='E-mail' 
                 value={props.inputValue.email} 
                 onChange={props.onChange} 
                 style={{borderBottom: props.errorMessages ? '1px solid var(--add-pink)' : '',}}/>
          {props.errorMessages && (<div className='form__input-error'>{props.errorMessages}</div>)}
        </div>
        
        <div className="auth__form__bottom-block">
          <div className='auth__form__checkbox-wrapper'>
            <input className='auth__form__checkbox-switch' 
                   id='checkbox-signup' 
                   type='checkbox' 
                   checked={props.agree} 
                   onChange={props.handleAgree}/>
            <label id='auth__form__checkbox-signUpLabel' 
                   htmlFor='checkbox-signup'>
              Даю согласие на обработку персональных данных
            </label>
          </div>
        </div>

        <button className='btn auth__form__btn signUp' 
                type='submit' 
                disabled={!props.agree} 
                onClick={props.onSignUp}>
          {!props.requestLoaded ? 
            <Loader size={20} 
                    left="50%" 
                    top="50%" 
                    tX="-50%" tY="-50%"/> : 
            "Зарегистрироваться"}
        </button>
      </form>
      <div className='auth__text auth__text-margin'>Уже есть аккаунт?{' '}
        <span className="auth__link"
              onClick={props.signInShow}>
          Войти</span>
      </div>
    </div>
  )
}

export default connect(
  state => ({}),
  dispatch => ({})
)(SignUp)