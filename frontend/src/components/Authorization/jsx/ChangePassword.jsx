import React from 'react'
import { useNavigate } from 'react-router-dom'
import Header from '~@/Layout/jsx/Header'
// import '~/styles/ChangePassword.styl'
import profileSelected from '~/assets/img/header_profile-selected.svg'
import backArrow from '~/assets/img/back-arrow.svg'
import {reverse} from "../../../ProjectConstants";

export default function ChangePassword() {
  const navigate = useNavigate()
  function backToRegistration() {
    navigate(reverse('index'))
  }

  return (
    <>
      <Header src={profileSelected} />
      <img
        className='change-password__back-arrow'
        src={backArrow}
        onClick={backToRegistration}
      />
      <div className='change-password__text'>
        <h2>Смена пароля</h2>
        <p>На Ваш e-mail отправлена ссылка для смены пароля.</p>
      </div>
    </>
  )
}
