import React, { useState } from 'react'
import {connect} from "react-redux";

import { useNavigate } from 'react-router-dom'
import eyeOpen from '~/assets/img/eye-open.svg'
import eyeClose from '~/assets/img/eye-close.svg'
import 'regenerator-runtime/runtime'
import {signUp} from "../../ajax";
import {DeactivateModal} from "../../../Layout/redux/actions/header";
import {reverse} from "../../../../ProjectConstants";
import {SwapLogin, SwapUserId} from "../../redux/actions/permissions";


function CreatePassword(props) {
  const navigate = useNavigate();

  const [signUpValue, setSignUpValue] = useState({
    email: '',
    password: '',
    password2: '',
  })

  function onChangeSignUp(e) {
    setErrorSignUpPassword('')
    setSignUpValue({ ...signUpValue, [e.target.name]: e.target.value })
  }

  //стейты для вывода ошибок с сервера при регистрации пароля
  const [errorSignUpPassword, setErrorSignUpPassword] = useState('')

  //отправка email и пароля на сервер
  let userSignUp = {
    email: props.email,
    password: signUpValue.password,
  }

  function onSubmitSignUp(e) {
    e.preventDefault()
    signUp(userSignUp)
      .then(response => response.json())
      .then(data => {
        if ('password' in data) {
          setErrorSignUpPassword(data.password[0])
        }
        if (data.status === 'signed_in') {
          props.SwapLogin(true)
          navigate(reverse('create_profile'))
          props.DeactivateModal()
        }
      })
      .catch(error => console.log('ERROR: ', error))
  }

  //Показать / скрыть пароль на регистрации
  const [hiddenSignUp, setHiddenSignUp] = useState(true)

  function handleHiddenSignUp() {
    setHiddenSignUp(!hiddenSignUp)
  }

  return (
    <div>
      <div className='auth__text'>
        Ваш e-mail успешно подтвержден.<br/>
        Придумайте пароль
      </div>
      <form className='auth__form'>
        <div className='input-temporary-margin'>
          <input
            className='form__input'
            name='password'
            type={hiddenSignUp ? 'password' : 'text'}
            placeholder='Пароль'
            value={signUpValue.password}
            onChange={onChangeSignUp}
            style={{borderBottom: errorSignUpPassword ? '1px solid var(--add-pink)' : '',}}/>
          <img className='password-icon' 
               src={hiddenSignUp ? eyeClose : eyeOpen} 
               alt={hiddenSignUp ? 'показать' : 'скрыть'} 
               onClick={handleHiddenSignUp}/>
        </div>

        <div className='input-temporary-margin'>
          <input className='form__input password2' 
                 name='password2' 
                 type={hiddenSignUp ? 'password' : 'text'} 
                 placeholder='Повторите пароль' 
                 value={signUpValue.password2} 
                 onChange={onChangeSignUp} 
                 style={{borderBottom: errorSignUpPassword || 
                   (signUpValue.password && signUpValue.password2 && 
                     signUpValue.password !== signUpValue.password2) ? '1px solid var(--add-pink)' : ''}}/>
          <img className='password-icon' 
               src={hiddenSignUp ? eyeClose : eyeOpen} 
               alt={hiddenSignUp ? 'показать' : 'скрыть'} 
               onClick={handleHiddenSignUp}/>
          {errorSignUpPassword && <div className='form__input-error'>{errorSignUpPassword}</div>}
          {signUpValue.password && signUpValue.password2 && 
            signUpValue.password !== signUpValue.password2 && 
            <div className='form__input-error'>Пароль не совпадает</div>}
        </div>
        
        <p className='auth__bottom-text fz-11'>Пароль должен содержать не менее 8 символов</p>
        
        <button className='btn auth__form__btn signUp'
                type='submit' 
                onClick={onSubmitSignUp} 
                disabled={signUpValue.password !== signUpValue.password2}>
          Продолжить
        </button>
      </form>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapLogin: (logged) => dispatch(SwapLogin(logged)),
    SwapUserId: (user_id) => dispatch(SwapUserId(user_id)),
    DeactivateModal: () => dispatch(DeactivateModal()),
  })
)(CreatePassword)
