import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import 'regenerator-runtime/runtime'
import {connect} from "react-redux";
import {DeactivateModal, SetErrorMessage} from "../../Layout/redux/actions/header";
import {emailConfirmation, login} from "../ajax";
import {SwapLogin} from "../redux/actions/permissions";
import {reverse} from "../../../ProjectConstants";
import SignUp from "./Elements/SignUp";
import ForgotPassword from "./Elements/ForgotPassword";
import Login from "./Elements/Login";


function Authorization(props) {
  const navigate = useNavigate();
  
  //вывод текста ошибки под инпутами
  const [errorSignUpEmail, setErrorSignUpEmail] = useState('')
  const [errorMessageEmail, setErrorMessageEmail] = useState('')
  const [errorMessagePassword, setErrorMessagePassword] = useState('')

  //ВХОД
  //изменение значений в инпутах
  const [signInValue, setSignInValue] = useState({
    email: '',
    password: '',
  })

  function onChangeSignIn(e) {
    setSignInValue({ ...signInValue, [e.target.name]: e.target.value })
  }

  //отправка данных на сервер
  let userSignIn = {
    email: signInValue.email,
    password: signInValue.password,
  }

   function onSubmitSignIn(e) {
    e.preventDefault()
     login(userSignIn)
      .then(response => {
        setErrorMessageEmail('') //очищаем стейты, чтоб при новом запросе они исчезли
        setErrorMessagePassword('')
        return response.json()
      })
      .then(data => {
        //ниже идет проверка наличия ключа в объекте дата.
        if ('non_field_errors' in data) {
          setErrorMessagePassword(data.non_field_errors[0])
        }
        if ('email' in data) {
          setErrorMessageEmail(data.email[0])
        }
        if ('password' in data) {
          setErrorMessagePassword(data.password[0])
        }
        if (data.status === ('logged_in' || 'signed_in')) {
          props.SwapLogin(true)
          navigate(reverse('workroom'))
          props.DeactivateModal()
        }
      })
      .catch(error => props.SetErrorMessage('login'))
  }

  //РЕГИСТРАЦИЯ
  //изменение значений в инпутах
  const [signUpValue, setSignUpValue] = useState({
    name: '',
    email: '',
    password: '',
    password2: '',
  })

  function onChangeSignUp(e) {
    setSignUpValue({ ...signUpValue, [e.target.name]: e.target.value })
  }

  //отправка данных на сервер
 // let userSignUpEmail = new URLSearchParams()
 // userSignUpEmail.append('email', `${signUpValue.email}`)
  let userSignUpEmail = {
    email: signUpValue.email,
  }

  function onSubmitSignUpEmail(e) {
    e.preventDefault()
    emailConfirmation(userSignUpEmail)
      .then(response => {
        setErrorSignUpEmail('') //очищаем стейты, чтоб при новом запросе прошлая ошибка не оставалась
        return response.json()
      })
      .then(data => {
        //ниже идет проверка наличия ключа в объекте дата.
        if ('email' in data) {
          setErrorSignUpEmail(data.email[0])
        }else if (data.status === 'error') {
          setErrorSignUpEmail(data.detail)
        } else if (data.status === 'success') {
          window.sessionStorage.setItem('email', signUpValue.email) //чтоб отобразить почту на /verify_email
          navigate(reverse('verify_email'))
          props.DeactivateModal()
        }
      })
      .catch(error => props.SetErrorMessage('signup'))
  }

  //Checkbox согласие на обработку персональных данных
  const [agree, setAgree] = useState(false)

  function handleAgree() {
    setAgree(!agree)
  }

  //переключение блоков Вход и Регистрация
  const [signInShown, setSignInShown] = useState(true)
  const [signUpShown, setSignUpShown] = useState(false)

  function handleSignInShow() {
    setSignInShown(true)
    setSignUpShown(false)
    setEmailForgottenShown(false)
  }

  function handleSignUpShow() {
    setSignInShown(false)
    setSignUpShown(true)
    setEmailForgottenShown(false)
  }

  //Блок Забыл пароль, смена пароля
  const [emailForgottenShown, setEmailForgottenShown] = useState(false)
  const [emailChangePassword, setEmailChangePassword] = useState('')

  function onEmailChangePassword(e) {
    setEmailChangePassword(e.target.value)
  }

  function handlePasswordForgotten() {
    setSignInShown(false)
    setEmailForgottenShown(true)
  }

  function onSubmitPasswordChange() {
    //пока нет api
    navigate(reverse('change_password'))
  }

  return (
    <div className='auth'>
      <div className='auth__header'>
        <h2 className='auth__header__SignIn-text' 
            onClick={handleSignInShow} 
            style={{color: signInShown || emailForgottenShown ? 'var(--main-blue)' : 'var(--add-darkGrey)',}}>
          Вход
        </h2>

        <h2 className='auth__header__SignUp-text' 
            onClick={handleSignUpShow} 
            style={{color: signUpShown ? 'var(--main-blue)' : 'var(--add-darkGrey)',}}>
          Регистрация
        </h2>
      </div>

      {/* Блок Вход*/}
      <Login show={signInShown} 
             inputValue={signInValue} 
             onEmailChange={onChangeSignIn} 
             errorMessages={{email: errorMessageEmail, password: errorMessagePassword}}
             onPasswordChange={onChangeSignIn} 
             handleForgotPassword={handlePasswordForgotten} 
             onSubmit={onSubmitSignIn} 
             signUpShow={handleSignUpShow}/>

      {/* Блок Регистрация Почта*/}
      <SignUp show={signUpShown} 
              agree={agree} 
              handleAgree={handleAgree} 
              onSignUp={onSubmitSignUpEmail} 
              errorMessages={errorSignUpEmail} 
              onChange={onChangeSignUp} 
              inputValue={signUpValue}/>

      {/* Блок Забыл пароль*/}
      <ForgotPassword show={emailForgottenShown} 
                      inputValue={emailChangePassword} 
                      onChange={onEmailChangePassword} 
                      onSubmit={onSubmitPasswordChange} 
                      signInShow={handleSignInShow}/>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapLogin: (logged) => dispatch(SwapLogin(logged)),
    DeactivateModal: () => dispatch(DeactivateModal()),
    SetErrorMessage: (message) => dispatch(SetErrorMessage(message)),
  })
)(Authorization)