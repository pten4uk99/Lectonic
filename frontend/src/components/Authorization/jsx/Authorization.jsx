import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
// import '~/styles/Authorization.styl'
import eyeOpen from '~/assets/img/eyeOpen.svg'
import eyeClose from '~/assets/img/eyeClose.svg'
import 'regenerator-runtime/runtime'
import { baseURL } from '~/ProjectConstants'

export default function Authorization() {
  const navigate = useNavigate() //Для перехода

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
    console.log('VALUE: ', signInValue)
  }

  //отправка данных на сервер
  let userSignIn = {
    email: signInValue.email,
    password: signInValue.password,
  }
  console.log('USER Sign In: ', userSignIn)

  async function onSubmitSignIn(e) {
    e.preventDefault()
    await fetch(`${baseURL}/api/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userSignIn),
    })
      .then(response => {
        console.log('RESPONSE SignIn: ', response)
        setErrorMessageEmail('') //очищаем стейты, чтоб при новом запросе они исчезли
        setErrorMessagePassword('')
        return response.json()
      })
      .then(data => {
        console.log('data: ', data)
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
        if (data.status == ('logged_in' || 'signed_in')) {
          navigate('/user_profile')
        }
      })
      .catch(error => {
        console.log('ERROR SignIn: ', error)
      })
  }

  //Checkbox не выходить из системы
  const [loggedIn, setLoggedIn] = useState(false)

  function onChangeLoggedIn() {
    setLoggedIn(!loggedIn)
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
    console.log('VALUE: ', signUpValue)
  }

  //отправка данных на сервер
  let userSignUpEmail = new URLSearchParams()
  userSignUpEmail.append('email', `${signUpValue.email}`)
  console.log('userSignUpEmail: ', userSignUpEmail)

  async function onSubmitSignUpEmail(e) {
    e.preventDefault()
    await fetch(`${baseURL}/api/email/email_confirmation/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: userSignUpEmail,
      credentials: 'include',
    })
      .then(response => {
        console.log('RESPONSE SignUpEmail: ', response)
        setErrorSignUpEmail('') //очищаем стейты, чтоб при новом запросе прошлая ошибка не оставалась
        return response.json()
      })
      .then(data => {
        console.log('data: ', data)
        //ниже идет проверка наличия ключа в объекте дата.
        if ('email' in data) {
          setErrorSignUpEmail(data.email[0])
        } else if (data.status == 'success') {
          window.sessionStorage.setItem('email', signUpValue.email) //чтоб отобразить почту на /verify_email
          navigate('/verify_email')
        }
      })
      .catch(error => {
        console.log('ERROR SignIn: ', error)
      })
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

  //Показать / скрыть пароль на входе
  const [hiddenSignIn, setHiddenSignIn] = useState(true)

  function handleHiddenSignIn() {
    setHiddenSignIn(!hiddenSignIn)
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
            {errorMessagePassword && (
              <div className='form__input-error'>{errorMessagePassword}</div>
            )}
            <img
              className='password-icon'
              src={hiddenSignIn ? eyeClose : eyeOpen}
              alt={hiddenSignIn ? 'показать' : 'скрыть'}
              onClick={handleHiddenSignIn}
            />
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
          <h5 onClick={handleSignUpShow}>Зарегистрироваться</h5>
        </div>
      </div>

      {/* Блок Регистрация Почта*/}
      <div style={{ display: signUpShown ? 'block' : 'none' }}>
        <div className='auth__text'>Для регистрации введите Ваш e-mail</div>
        <form className='auth__form'>
          <div className='auth__form__input-wrapper'>
            <input
              className='form__input signUpEmail'
              name='email'
              type='email'
              placeholder='E-mail'
              value={signUpValue.email}
              onChange={onChangeSignUp}
              style={{
                borderBottom: errorSignUpEmail
                  ? '1px solid var(--add-pink)'
                  : '',
              }}
            />
            {errorSignUpEmail && (
              <div className='form__input-error'>{errorSignUpEmail}</div>
            )}
          </div>

          <div className='auth__form__checkbox-wrapper'>
            <input
              className='auth__form__checkbox-switch'
              id='checkbox'
              type='checkbox'
              checked={agree}
              onChange={handleAgree}
            />
            <label id='auth__form__checkbox-signUpLabel' htmlFor='checkbox'>
              Я даю согласие на обработку персональных данных
            </label>
          </div>

          <button
            className='btn auth__form__btn signUp'
            type='submit'
            disabled={!agree}
            onClick={onSubmitSignUpEmail}
          >
            Зарегистрироваться
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
