import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";
import {useLocation, useNavigate} from "react-router-dom";

import photoIcon from '~/assets/img/photo-icon.svg'
import locationIcon from '~/assets/img/location-icon.svg'
import birthdateIcon from '~/assets/img/birthdate-icon.svg'
import backArrow from '~/assets/img/back-arrow.svg'
import infoIcon from '~/assets/img/Info-icon.svg'
import {getDaysArr, getMonthsArr, getYearsArr} from "./utils/date";
import {UpdateBirthDate} from "../redux/actions/profile";
import {createProfile, getCities, getProfile, setProfile} from "../ajax/profile";
import {reverse, reverseEqual} from "../../../ProjectConstants";
import {SwapPerson, SwapUserId} from "../../Authorization/redux/actions/permissions";
import {SetErrorMessage} from "../../Layout/redux/actions/header";
import DropDown from '~@/Utils/jsx/DropDown';
import {SetIdDropDown} from "../../Utils/redux/actions/dropdown";
import Loader from "../../Utils/jsx/Loader";


function SetProfileInfo(props) {
  let birth_date = props.store.profile.birth_date
  let navigate = useNavigate()
  let location = useLocation()
  let setInfo = reverseEqual('set_profile', location.pathname)
  let [loadedRequest, setLoadedRequest] = useState(true)
  
  let [profileInfo, setProfileInfo] = useState(null)
  let [avatarPreview, setAvatarPreview] = useState(null)

  useEffect(() => {
    if (!setInfo) {
      if (props.store.permissions.is_person) navigate(reverse('workroom'))
    }
  }, [props.store.permissions.is_person])
  
  useEffect(() => {
    if (setInfo) {
      getProfile()
        .then(r => r.json())
        .then(data => setProfileInfo(data.data[0]))
        .catch(e => console.log(e))
    }
  }, [])
  
  useEffect(() => {
    if (profileInfo) {
      let [year, month, day] = profileInfo.birth_date.split('-')
      props.UpdateBirthDate({year: year, month: month, day: day})
      props.SetIdDropDown(profileInfo.city.id)
      setAvatarPreview(profileInfo.photo)
    }
  }, [profileInfo])
  
  let [requiredFields, setRequiredFields] = useState({
    lastName: '',
    firstName: '',
    city: '',
  })
  
  const handleAvatarPreview = e => {
    const reader = new FileReader();
    reader.onload = () => {
      if(reader.readyState === 2) {
        setAvatarPreview(reader.result)
      }
    }
    reader.readAsDataURL(e.target.files[0])
  }
  
  let [dayArray, setDayArray] = useState(getDaysArr(birth_date.year, birth_date.month))
  
  useEffect(() => {
    setDayArray(getDaysArr(birth_date.year, birth_date.month))
  }, [birth_date.year, birth_date.month])

  
  let [errorMessages, setErrorMessages] = useState({
    firstName: '',
    lastName: '',
    middleName: '',
    birthDate: '',
    city: ''
  })
  
  function handleFormSubmit(e) {
    setLoadedRequest(false)
    e.preventDefault()
    let formData = new FormData(e.target)
    formData.set('city', props.store.dropdown.id)
    formData.delete('year')
    formData.delete('month')
    formData.delete('day')
    formData.set('birth_date', `${birth_date.year}-${birth_date.month}-${birth_date.day}`)
    
    if (!setInfo) {
      createProfile(formData)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'created') {
            setLoadedRequest(true)
            props.SwapUserId(data.data[0].user_id)
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
        .catch(error => console.log(error))
    } else {
      setProfile(formData)
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            setLoadedRequest(true)
            navigate(reverse('workroom'))
          } else {
            setErrorMessages({
              firstName: data?.first_name || '',
              lastName: data?.last_name || '',
              middleName: data?.middle_name || '',
              birthDate: data?.birth_date || '',
              city: data?.city || ''
            })
          }
        })
        .catch(e => console.log(e))
    }
    
  }

  return (
    <>
      {setInfo && <div className="navigate-back__block" 
                       onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrow} alt="назад"/>
      </div>}
      
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
            <input name='last_name' 
                   className='form__input'
                   type='text' 
                   placeholder='Фамилия' 
                   defaultValue={profileInfo?.last_name}
                   onChange={(e) => setRequiredFields({...requiredFields, lastName: e.target.value})}/>
            <span className='required-sign'>*</span>
            {errorMessages.lastName && (<div className='form__input-error'>{errorMessages.firstName}</div>)}
          </div>

          <div className='userInfo__form__input-container'>
            <input name='first_name' 
                   className='form__input'
                   type='text' 
                   placeholder='Имя' 
                   defaultValue={profileInfo?.first_name}
                   onChange={(e) => setRequiredFields({...requiredFields, firstName: e.target.value})}/>
            <span className='required-sign'>*</span>
            {errorMessages.firstName && (<div className='form__input-error'>{errorMessages.lastName}</div>)}
          </div>

          <div className='userInfo__form__input-container'>
            <input name='middle_name' 
                   className='form__input' 
                   type='text' 
                   defaultValue={profileInfo?.middle_name}
                   placeholder='Отчество'/>
            {errorMessages.middleName && (<div className='form__input-error'>{errorMessages.middleName}</div>)}
          </div>

          <div className='userInfo__form__inputIcon-container'>
            <img className='location-icon' src={locationIcon} />
            <div className='dropDown-wrapper'>
              <DropDown request={getCities}
                        width={true} 
                        input={true} 
                        placeholder='Ваш город'
                        defaultValue={profileInfo?.city.name}
                        onSelect={(value) => setRequiredFields({...requiredFields, city: value})}/>
            </div>
            <div className='required-sign required-sign-location'>*</div>
          </div>
          {errorMessages.city && (<div className='form__input-error'>{errorMessages.city}</div>)}

          <div className='userInfo__form__inputIcon-container'>
            <img className='birthdate-icon' src={birthdateIcon}/>
            <div className='dropDown-wrapper'>
              <DropDown request={dayArray} 
                        onSelect={(value) => props.UpdateBirthDate({day: value})} 
                        defaultValue={birth_date.day}
                        inputName="day"/>
            </div>

            <div className='dropDown-wrapper'>
            <DropDown request={getMonthsArr()}
                      onSelect={(value) => props.UpdateBirthDate({month: value})}
                      defaultValue={getMonthsArr()[birth_date.month - 1]}
                      inputName="month" monthArr={true}/>
            </div>
            <div className='dropDown-wrapper'>
            <DropDown request={getYearsArr()}
                      onSelect={(value) => props.UpdateBirthDate({year: value})} 
                      defaultValue={birth_date.year}
                      inputName="year"/>
            </div>
            <div className='required-sign required-sign-birthdate'>*</div>
          </div>
          {errorMessages.birthDate && (<div className='form__input-error'>{errorMessages.birthDate}</div>)}

          <div className='userInfo__form__inputIcon-container'>
            <img className='info-icon' src={infoIcon}/>
            <textarea name='description' 
                      className='form__textarea textarea-height178 w-298'
                      defaultValue={profileInfo?.description}
                      placeholder='Напишите о себе'/>
          </div>
          <button type='submit' 
                  className='btn userInfo__btn' 
                  disabled={checkRequiredFields(requiredFields, setInfo)}>
            {!loadedRequest ? 
              <Loader size={20} 
                      left="50%" 
                      top="50%" 
                      tX="-50%" tY="-50%"/> : 
              "Продолжить"}
            </button>
        </form>
      </div>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SetErrorMessage: (message) => dispatch(SetErrorMessage(message)),
    SwapUserId: (user_id) => dispatch(SwapUserId(user_id)),
    SetIdDropDown: (id) => dispatch(SetIdDropDown(id)),
    SwapPerson: (is_person) => dispatch(SwapPerson(is_person)),
    UpdateBirthDate: (data) => dispatch(UpdateBirthDate(data)),
  })
)(SetProfileInfo)


function checkRequiredFields(obj, setInfo) {
  if (setInfo) return false
  for (let field in obj) {
    if (!obj[field]) return true
  }
  return false
}