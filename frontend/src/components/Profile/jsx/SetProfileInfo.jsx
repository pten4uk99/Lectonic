import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
import {useNavigate} from "react-router-dom";

import photoIcon from '~/assets/img/photo-icon.svg'
import locationIcon from '~/assets/img/location-icon.svg'
import birthdateIcon from '~/assets/img/birthdate-icon.svg'
import infoIcon from '~/assets/img/Info-icon.svg'
import {getDaysArr, getMonthsArr, getYearsArr} from "./utils/date";
import {UpdateBirthDate} from "../redux/actions/profile";
import {createProfile, getCities} from "../ajax/profile";
import {reverse} from "../../../ProjectConstants";
import {SwapPerson} from "../../Authorization/redux/actions/permissions";


function SetProfileInfo(props) {
  let birth_date = props.store.profile.birth_date
  let navigate = useNavigate()
  
  useEffect(() => {
    if (props.store.permissions.is_person) navigate(reverse('workroom'))
  }, [props.store.permissions.is_person])
  
  let [requiredFields, setRequiredFields] = useState({
    lastName: '',
    firstName: '',
    city: '',
  })
  
  //отображение выбранного аватара
  let [avatarPreview, setAvatarPreview] = useState(null) //выбранный файл для отправки на сервер
  
  const handleAvatarPreview = e => {
    const reader = new FileReader();
    reader.onload = () => {
      if(reader.readyState === 2) {
        setAvatarPreview(reader.result)
      }
    }
    reader.readAsDataURL(e.target.files[0])
  }
  
  let [cities, setCities] = useState(null)
  
  function handleCityChange(e) {
    getCities(e.target.value)
      .then(response => response.json())
      .then(data => setCities(data.data))
      .catch(error => console.log('ERROR: ', error))
    setRequiredFields({...requiredFields, city: e.target.value})
  }
  
  let [errorMessages, setErrorMessages] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    birthDate: ''
  })
  
  function handleFormSubmit(e) {
    e.preventDefault()
    let formData = new FormData(e.target)
    let year = formData.get('year')
    let month = formData.get('month')
    let day = formData.get('day')
    formData.delete('year')
    formData.delete('month')
    formData.delete('day')
    formData.set('birth_date', `${year}-${month}-${day}`)
    
    createProfile(formData)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'created') {
          props.SwapPerson(true)
          navigate(reverse('add_role'))
        }
        else {
          setErrorMessages({
            firstName: data?.first_name || '',
            lastName: data?.last_name || '',
            middleName: data?.middle_name || '',
            birthDate: data?.birth_date || '',
          })
        }
      })
      .catch(error => console.log('Ошибка в создании профиля: ', error))
  }

  return (
    <>
      <div className='userInfo'>
        <h2 className='userInfo__text-header'>Информация профиля</h2>
        <p className='userInfo__text'>
          Заполните информацию профиля.<br/>
          Это даст Вам возможность пользоваться сервисом.
        </p>

        <form className='userInfo__form' onSubmit={e => handleFormSubmit(e)}>
          <div className='add-avatar'>
            {avatarPreview && (
              <img src={avatarPreview} 
                   className='preview-avatar__img' 
                   alt='аватар'/>)}
            <label className='add-avatar__label' 
                   htmlFor='avatar'>
              <img src={photoIcon} 
                   alt='выбрать фото' 
                   style={{marginLeft: avatarPreview ? '-130px' : ''}}/>
              <div className='add-avatar__text' 
                   style={{display: avatarPreview ? 'none' : ''}}>Добавить аватар</div>
            </label>
            <input type='file' 
                   name='photo'
                   id='avatar' 
                   accept='image/jpeg, image/png' 
                   onChange={handleAvatarPreview}/>
          </div>
          
          <div className='userInfo__form__input-container'>
            <input name='first_name' 
                   className='form__input'
                   type='text' 
                   placeholder='Фамилия' 
                   onChange={(e) => setRequiredFields({...requiredFields, lastName: e.target.value})}/>
            <span className='required-sign'>*</span>
            {errorMessages.firstName && (<div className='form__input-error'>{errorMessages.firstName}</div>)}
          </div>

          <div className='userInfo__form__input-container'>
            <input name='last_name' 
                   className='form__input'
                   type='text' 
                   placeholder='Имя' 
                   onChange={(e) => setRequiredFields({...requiredFields, firstName: e.target.value})}/>
            <span className='required-sign'>*</span>
            {errorMessages.lastName && (<div className='form__input-error'>{errorMessages.lastName}</div>)}
          </div>

          <div className='userInfo__form__input-container'>
            <input name='middle_name' 
                   className='form__input' 
                   type='text' 
                   placeholder='Отчество'/>
            {errorMessages.middleName && (<div className='form__input-error'>{errorMessages.middleName}</div>)}
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='location-icon' src={locationIcon} />
            <div className='dropDown-wrapper'>
              <input type="text" 
                     list="cities" 
                     name="city"
                     autoComplete='none'
                     onChange={(e) => handleCityChange(e)}/>
              <datalist id="cities">
                {cities ? 
                  cities.map((city) => <option key={city.id}
                                               data-city-id={city.id}
                                               value={city.id}>{city.name}</option>) : <></>}
              </datalist>
            </div>
            <div className='required-sign required-sign-location'>*</div>
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='birthdate-icon' src={birthdateIcon} />
            <div className='dropDown-wrapper'>
              <select name="day" 
                      onChange={(e) => props.UpdateBirthDate({day: e.target.selectedOptions[0].value})}>
                <option value={birth_date.day}>{birth_date.day}</option>
                {getDaysArr(birth_date.year, birth_date.month).map((elem, index) => (
                  <option key={index} value={elem}>{elem}</option>
                ))}
              </select>
              {errorMessages.birthDate && (<div className='form__input-error'>{errorMessages.birthDate}</div>)}
            </div>

            <div className='dropDown-wrapper'>
              <select name="month" 
                      onChange={(e) => props.UpdateBirthDate({month: e.target.selectedOptions[0].value})}>
                <option value={birth_date.month}>{getMonthsArr()[birth_date.month - 1]}</option>
                {getMonthsArr().map((elem, index) => <option key={index} value={index + 1}>{elem}</option>)}
              </select>
            </div>

            <div className='dropDown-wrapper'>
              <select name="year" 
                      onChange={(e) => props.UpdateBirthDate({year: e.target.selectedOptions[0].value})}>
                <option value={birth_date.year}>{birth_date.year}</option>
                  {getYearsArr().map((elem, index) => <option key={index} value={elem}>{elem}</option>)}
                </select>
            </div>
            <div className='required-sign required-sign-birthdate'>*</div>
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='info-icon' src={infoIcon}/>
            <textarea name='description' 
                      className='form__textarea textarea-height178' 
                      placeholder='Напишите о себе'/>
          </div>
          <button type='submit' 
                  className='btn userInfo__btn' 
                  disabled={checkRequiredFields(requiredFields)}>Продолжить</button>
        </form>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapPerson: (is_person) => dispatch(SwapPerson(is_person)),
    UpdateBirthDate: (data) => dispatch(UpdateBirthDate(data)),
  })
)(SetProfileInfo)


function checkRequiredFields(obj) {
  for (let field in obj) {
    if (!obj[field]) return true
  }
  return false
}