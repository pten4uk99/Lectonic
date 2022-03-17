import React, { useState } from 'react'
// import DropDownElement from './DropdownElement'
import Header from '~@/Layout/jsx/Header'
// import '~/styles/UserBasicInfo.styl'
import photoIcon from '~/assets/img/photo-icon.svg'
import locationIcon from '~/assets/img/location-icon.svg'
import birthdateIcon from '~/assets/img/birthdate-icon.svg'
import infoIcon from '~/assets/img/Info-icon.svg'
import profileSelected from '~/assets/img/header_profile-selected.svg'
import DropDownTest from './DropDownTest'
import { baseURL } from '~/ProjectConstants'


export default function UserBasicInfo() {
  //отображение выбранного аватара
  const [avatarPreview, setAvatarPreview] = useState(null) //выбранный файл для отправки на сервер
  console.log('avatarPreview: ', avatarPreview)
  
  const handleAvatarPreview = e => {
    const reader = new FileReader();
    reader.onload = () => {
      if(reader.readyState === 2) {
        setAvatarPreview(reader.result)
      }
    }
    reader.readAsDataURL(e.target.files[0])
  }
  
  //метод get для отображения городов
  fetch(`${baseURL}/api/workrooms/city`, {
    method: 'GET',
    credentials: 'include',
  })
    .then(response => {
      console.log('RESPONSE: ', response)
      return response.json()
    })
    .then(data => {
      console.log('data: ', data)
    })
    .catch(error => {
      console.log('ERROR: ', error)
    })
  
  
  let defaultUserDetails = {
    userSurname: '',
    userFirstName: '',
    userMiddleName: '',
    userCity: '',
    dayOfBirth: '',
    monthOfBirth: '',
    yearOfBirth: '',
    userSelfDescription: '',
  }

  let [userDetails, setUserDetails] = useState({ ...defaultUserDetails })

  function handleInputChange(event, input) {
    setUserDetails(prev => {
      return {
        ...prev,
        [input]: event.target.value,
      }
    })
  }

  function handleAddEvent(e) {
    e.preventDefault()
    if (
      userDetails.userFirstName &&
      userDetails.userMiddleName &&
      userDetails.userSurname
    ) {
      console.log(userDetails)
      setUserDetails({ ...defaultUserDetails })
    }
  }

  let citySelect = {
    class: 'city-select',
    default: 'Ваш город',
    options: ['Москва', 'Санкт-Петербург', 'Воронеж'],
  }

  let daySelect = {
    class: 'day-select',
    default: '01',
    options: ['01', '02', '03'],
  }

  let monthSelect = {
    class: 'month-select',
    default: 'Января',
    options: [
      'Января',
      'Февраля',
      'Марта',
      'Апреля',
      'Мая',
      'Июня',
      'Июля',
      'Августа',
      'Сентября',
      'Октября',
      'Ноября',
      'Декабря',
    ],
  }

  let yearSelect = {
    class: 'year-select',
    default: '1990',
    options: ['1990', '1991', '1993'],
  }

  function click() {
    console.log('clicked yes')
  }

  return (
    <>
      <div className='userInfo'>
        <h2 className='userInfo__text-header'>Информация профиля</h2>
        <p className='userInfo__text'>
          Заполните информацию профиля.
          <br />
          Это даст Вам возможность пользоваться сервисом.
        </p>

        <form encType='multipart/form-data'
              className='userInfo__form' 
              onSubmit={e => handleAddEvent(e)}>
          <div className='add-avatar'>
            {avatarPreview && (
              <img
                src={avatarPreview}
                className='preview-avatar__img'
                alt='аватар'
              />
            )}
            <label 
              className='add-avatar__label' 
              htmlFor='avatar'
            >
              <img 
                src={photoIcon}
                alt='выбрать фото'
                style={{marginLeft: avatarPreview ? '-130px' : ''}}/>
              <div 
                className='add-avatar__text'
                style={{display: avatarPreview ? 'none' : ''}}
              >Добавить аватар
              </div>
            </label>
            <input
              type='file'
              name='avatar'
              id='avatar'
              accept='image/*'
              onChange={handleAvatarPreview}
            />
          </div>
          
          <div className='userInfo__form__input-container'>
            <input
              className='form__input'
              value={userDetails.userSurname}
              type='text'
              placeholder='Фамилия'
              onChange={e => handleInputChange(e, 'userSurname')}
            />
            <span className='required-sign'>*</span>
          </div>

          <div className='userInfo__form__input-container'>
            <input
              className='form__input'
              value={userDetails.userFirstName}
              type='text'
              placeholder='Имя'
              onChange={e => handleInputChange(e, 'userFirstName')}
            />
            <span className='required-sign'>*</span>
          </div>

          <div className='userInfo__form__input-container'>
            <input
              className='form__input'
              value={userDetails.userMiddleName}
              type='text'
              placeholder='Отчество'
              onChange={e => handleInputChange(e, 'userMiddleName')}
            />
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='location-icon' src={locationIcon} />
            <DropDownTest
              selectDetails={citySelect}
              className='city-select'
              placeholder='Ваш город'
              style={{ width: '228px' }}
            />
            <div className='required-sign required-sign-location'>*</div>
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='birthdate-icon' src={birthdateIcon} />
            <div className='dropDown-wrapper'>
              <DropDownTest
                className='day-select'
                selectDetails={daySelect}
                placeholder='01'
                style={{ width: '55px' }}
              />
            </div>

            <div className='dropDown-wrapper'>
              <DropDownTest
                className='month-select'
                selectDetails={monthSelect}
                placeholder='Января'
                style={{ width: '99px' }}
              />
            </div>

            <DropDownTest
              className='year-select'
              selectDetails={yearSelect}
              placeholder='1990'
              style={{ width: '71px' }}
            />
            <div className='required-sign required-sign-birthdate'>*</div>
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='info-icon' src={infoIcon} />
            <textarea
              className='form__textarea textarea-height178'
              value={userDetails.userSelfDescription}
              placeholder='Напишите о себе'
              onChange={e => handleInputChange(e, 'userSelfDescription')}
            ></textarea>
          </div>
          <button
            className='btn userInfo__btn'
            onClick={e => handleAddEvent(e)}
          >
            Продолжить
          </button>
        </form>
      </div>
    </>
  )
}
