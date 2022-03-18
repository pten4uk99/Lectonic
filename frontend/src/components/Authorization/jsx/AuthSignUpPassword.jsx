import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
// import '~/styles/Authorization.styl'
import eyeOpen from '~/assets/img/eye-open.svg'
import eyeClose from '~/assets/img/eye-close.svg'
import 'regenerator-runtime/runtime'
import { baseURL } from '~/ProjectConstants'
import {login, signUp} from "../ajax";
import {DeactivateModal} from "../../Layout/redux/actions/header";
import {connect} from "react-redux";


function AuthSignUpPassword(props) {
  //!!!ниже будет повторение кода из Authorisation.js, пока так
  
  const navigate = useNavigate();
  
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
          navigate('/user_profile')
          props.DeactivateModal()
        }
      })
      .catch(error => console.log('ERROR SignIn: ', error))
  }

  //Checkbox не выходить из системы
  const [loggedIn, setLoggedIn] = useState(false)

  function onChangeLoggedIn() {
    setLoggedIn(!loggedIn)
  }

  //РЕГИСТРАЦИЯ
  //изменение значений в инпутах
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
    email: props.email || window.localStorage.getItem('email'),
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
          navigate('/create_profile')
        }
      })
      .catch(error => console.log('ERROR: ', error))
  }

  //переключение блоков Вход и Регистрация
  const [signInShown, setSignInShown] = useState(false)
  const [signUpShown, setSignUpShown] = useState(true)

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

  //Показать / скрыть пароль на входе
  const [hiddenSignIn, setHiddenSignIn] = useState(true)

  function handleHiddenSignIn() {
    setHiddenSignIn(!hiddenSignIn)
  }

  //Показать / скрыть пароль на регистрации
  const [hiddenSignUp, setHiddenSignUp] = useState(true)

  function handleHiddenSignUp() {
    setHiddenSignUp(!hiddenSignUp)
  }

  //Блок Забыл пароль, смена пароля
  const [emailForgottenShown, setEmailForgottenShown] = useState(false)
  const [emailChangePassword, setEmailChangePassword] = useState('')

  function onEmailChangePassword(e) {
    setEmailChangePassword(e.target.value)
    console.log('xtr, ', emailChangePassword)
  }

  function handlePasswordForgotten() {
    setSignInShown(false)
    setEmailForgottenShown(true)
  }

  function onSubmitPasswordChange() {
    //пока нет api
    navigate('/change_password')
  }

  return (
    <div className='auth'>
      <div className='auth__header'>
        <h2
          className='auth__header__SignIn-text'
          onClick={handleSignInShow}
          style={{
            color:
              signInShown || emailForgottenShown
                ? 'var(--main-blue)'
                : 'var(--add-darkGrey)',
          }}
        >
          Вход
        </h2>

        <h2
          className='auth__header__SignUp-text'
          onClick={handleSignUpShow}
          style={{
            color: signUpShown ? 'var(--main-blue)' : 'var(--add-darkGrey)',
          }}
        >
          Регистрация
        </h2>
      </div>

      {/* Блок Вход*/}
      <div style={{ display: signInShown ? 'block' : 'none' }}>
        <div className='auth__text'>Войдите в свой аккаунт</div>
        <form className='auth__form'>
          <div className='auth__form__input-wrapper'>
            <input
              className='form__input'
              name='email'
              type='email'
              placeholder='E-mail'
              value={signInValue.email}
              onChange={onChangeSignIn}
              style={{
                borderBottom: errorMessageEmail
                  ? '1px solid var(--add-pink)'
                  : '',
              }}
            />
            {errorMessageEmail && (
              <div className='form__input-error'>{errorMessageEmail}</div>
            )}
          </div>

          <div className='auth__form__input-wrapper'>
            <input
              className='form__input'
              name='password'
              type={hiddenSignIn ? 'password' : 'text'}
              placeholder='Пароль'
              value={signInValue.password}
              onChange={onChangeSignIn}
              style={{
                borderBottom: errorMessagePassword
                  ? '1px solid var(--add-pink)'
                  : '',
              }}
            />
            <img
              className='password-icon'
              src={hiddenSignIn ? eyeClose : eyeOpen}
              alt={hiddenSignIn ? 'показать' : 'скрыть'}
              onClick={handleHiddenSignIn}
            />
            {errorMessagePassword && (
              <div className='form__input-error'>{errorMessagePassword}</div>
            )}
          </div>

          <div
            className='auth__form__password-forgotten'
            onClick={handlePasswordForgotten}
          >
            Забыли пароль?
          </div>

          <div className='auth__form__checkbox-wrapper signIn'>
            <input
              className='auth__form__checkbox-switch'
              id='checkbox'
              type='checkbox'
              checked={loggedIn}
              onChange={onChangeLoggedIn}
            />
            <label htmlFor='checkbox'>Не выходить из системы</label>
          </div>

          <button
            className='btn auth__form__btn'
            type='submit'
            onClick={onSubmitSignIn}
          >
            Войти
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
          <span onClick={handleSignUpShow}>Зарегистрироваться</span>
        </div>
      </div>

      {/* Блок Регистрация Пароль*/}
      <div style={{ display: signUpShown ? 'block' : 'none' }}>
        <div className='auth__text'>
          Ваш e-mail успешно подтвержден.
          <br />
          Придумайте пароль
          <p>Пароль должен содержать не менее 8 символов</p>
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
              style={{
                borderBottom: errorSignUpPassword
                  ? '1px solid var(--add-pink)'
                  : '',
              }}
            />
            <img
              className='password-icon'
              src={hiddenSignUp ? eyeClose : eyeOpen}
              alt={hiddenSignUp ? 'показать' : 'скрыть'}
              onClick={handleHiddenSignUp}
            />
          </div>

          <div className='input-temporary-margin'>
            <input
              className='form__input password2'
              name='password2'
              type={hiddenSignUp ? 'password' : 'text'}
              placeholder='Повторите пароль'
              value={signUpValue.password2}
              onChange={onChangeSignUp}
              style={{
                borderBottom:
                  errorSignUpPassword ||
                  (signUpValue.password &&
                    signUpValue.password2 &&
                    signUpValue.password !== signUpValue.password2)
                    ? '1px solid var(--add-pink)'
                    : '',
              }}
            />
            <img
              className='password-icon'
              src={hiddenSignUp ? eyeClose : eyeOpen}
              alt={hiddenSignUp ? 'показать' : 'скрыть'}
              onClick={handleHiddenSignUp}
            />
            {errorSignUpPassword && (
              <div className='form__input-error'>{errorSignUpPassword}</div>
            )}
            {signUpValue.password &&
              signUpValue.password2 &&
              signUpValue.password !== signUpValue.password2 && (
                <div className='form__input-error'>Пароль не совпадает</div>
              )}
          </div>

          <button
            className='btn auth__form__btn signUp'
            type='submit'
            onClick={onSubmitSignUp}
            disabled={signUpValue.password !== signUpValue.password2}>
            Продолжить
          </button>
        </form>
      </div>

      {/* Блок Забыл пароль*/}
      <div
        className='auth__password-forgotten'
        style={{ display: emailForgottenShown ? 'block' : 'none' }}
      >
        <div className='auth__text'>Смена пароля</div>
        <form className='auth__form'>
          <div className='auth__form__input-wrapper'>
            <input
              className='form__input'
              name='email_password-forgotten'
              type='email'
              placeholder='E-mail'
              value={emailChangePassword}
              onChange={onEmailChangePassword}
            />
            <div className='auth__password-forgotten__text'>
              Ссылка на смену пароля будет выслана вам по e-mail
            </div>
          </div>

          <button
            className='btn'
            type='submit'
            onClick={onSubmitPasswordChange}
          >
            Продолжить
          </button>
          <h5
            className='auth__password-forgotten__text-bottom'
            onClick={handleSignInShow}
          >
            Авторизоваться
          </h5>
        </form>
      </div>
    </div>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal())
  })
)(AuthSignUpPassword)
