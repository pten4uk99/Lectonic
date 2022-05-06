import React, {useState} from "react";
import {connect} from "react-redux";
import {reverse} from "../../../../ProjectConstants";
import {useNavigate} from "react-router-dom";
import {DeactivateModal} from "../../../Layout/redux/actions/header";
import {emailConfirmation} from "../../ajax";


function ForgotPassword(props) {
  const navigate = useNavigate()
  
  const [email, setEmail] = useState({email: ''})
  
  function onSubmit() {
    emailConfirmation(email, true)
      .then(response => {
        props.setError('')
        return response.json()
      })
      .then(data => {
        if ('email' in data) {
          props.setError(data.email[0])
        } else if (data.status === 'error') {
          props.setError(data.detail)
        } else if (data.status === 'success') {
          navigate(reverse('change_password'))
          props.DeactivateModal()
        }
        props.setRequestLoaded(true)
      })
      .catch(error => console.log(error))
  }
  
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
                 onChange={(e) => setEmail({email: e.target.value})}/>
          
          <div className='auth__password-forgotten__text'>Ссылка на смену пароля будет выслана Вам по e-mail</div>
        </div>

        <button className='btn auth__form__btn' type='button' onClick={onSubmit}>Продолжить</button>
        
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
  dispatch => ({
    DeactivateModal: () => dispatch(DeactivateModal()),
  })
)(ForgotPassword)