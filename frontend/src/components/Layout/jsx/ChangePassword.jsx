import React from 'react'
import { useNavigate } from 'react-router-dom'

import backArrow from '~/assets/img/back-arrow.svg'
import {reverse} from "../../../ProjectConstants";


export default function ChangePassword() {
  const navigate = useNavigate()
  
  function back() {
    navigate(reverse('index'))
  }

  return (
    <>
      <img className='change-password__back-arrow' 
           src={backArrow} 
           alt="назад"
           onClick={back}/>
      <div className='change-password__text'>
        <h2>Смена пароля</h2>
        <p>На Ваш e-mail отправлена ссылка для смены пароля.</p>
      </div>
    </>
  )
}
