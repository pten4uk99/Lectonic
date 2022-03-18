import React, {useEffect, useRef, useState} from 'react'

import calendarIcon from '~/assets/img/event/calendar-icon.svg'
import photoIcon from '~/assets/img/photo-icon.svg'
import downArrow from '~/assets/img/down-arrow.svg'
import {connect} from "react-redux";
import {
  SwapEventType, SwapPayment, SwapPlace,
  UpdateDomain,
  UpdatePhoto
} from "../redux/actions/event";
import {createEvent, getDomainArray} from "../ajax/event";
import {useNavigate} from "react-router-dom";


function CreateEvent(props) {
  let navigate = useNavigate()
  let selectedDomains = props.store.event.domain
  let eventType = props.store.event.type
  let place = props.store.event.place
  let payment = props.store.event.payment
  let titlePhotoSrc = props.store.event.photo
  
  let [domainArray, setDomainArray] = useState(null)
  
  useEffect(() => {
    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])
  
  useEffect(() => {
    if (selectedDomains.length > 0) {
      let newDomainArray
      newDomainArray = domainArray.filter(elem => !selectedDomains.includes(elem.name))
      setDomainArray(newDomainArray)
    }
  }, [selectedDomains])
  
  function submitFormHandler(e) {
    e.preventDefault()
    let formData = new FormData(e.target)
    selectedDomains.map((elem) => formData.append('domain',  elem))
    formData.set('type', eventType)
    createEvent(formData)
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log('Ошибка в создании лекции: ', error))
    
    navigate('/user_profile')
  }
  
  return (
    <form onSubmit={(e) => submitFormHandler(e)}>
      <div className='create-event__wrapper'>
        <div className='heading'>
          <h1 className='main-heading'>Создание мероприятия</h1>
        </div>
        <div className='subheading'>
          <h2 className='main-subheading'>
            Вы можете создать одно или несколько мероприятий, чтобы потенциальне
            слушатели могли откликнуться.
          </h2>
        </div>
        
        <div className='cover-l label'> Обложка:</div>
        <label className={titlePhotoSrc ? 'cover' : 'cover no-photo'}>
          <img className='icon' 
               src={photoIcon} 
               alt='photo-icon'/>
            <span className='add-photo'>Добавить фото</span>
            <input name='photo'
                   className='add-photo__input'
                   type='file'
                   onChange={e => addPhotoHandler(e, props.UpdatePhoto)}/>
          <img className='title-img'
               src={titlePhotoSrc}
               alt='Обложка'/>
        </label>
        
        <div className='domain-l label'>Тематика:</div>
        <div className='domains'>
          <div className='domain-list flex'>
            <select className='selector'
                    style={{ backgroundImage: `url(${downArrow})` }} 
                    onChange={e => domainSelectHandler(e, props)}>
              <option value='' disabled selected>Выберите тематику</option>
              {domainArray ? domainArray.map((elem) => {
                return <option key={elem.id} value={elem.id}>{elem.name}</option>
              }): <></>}
            </select>
            {selectedDomains.map((domain, index) => {
              return <div key={index} className='pill pill-grey'>{domain}</div>
            })}
          </div>
        </div>
        
        <div className='topic-l label'>Тема лекции:</div>
        <div className='topic flex'>
          <input name='name' type='text' className='text-input'/>
        </div>
        
        <div className='type-l label'>Тип лекции:</div>
        <div className='type flex'>
          <div className={eventType !== 'online' ? 'pill' : 'pill pill-blue'} 
               onClick={() => props.SwapEventType('online')}>Онлайн</div>
          <div className={eventType !== 'offline' ? 'pill' : 'pill pill-blue'} 
               onClick={() => props.SwapEventType('offline')}>Оффлайн</div>
          <div className={eventType !== 'hybrid' ? 'pill' : 'pill pill-blue'} 
               onClick={() => props.SwapEventType('hybrid')}>Гибрид</div>
        </div>
        
        <div className='date-l label'>Дата:</div>
        <div className='date flex'>
          <div className='open-calendar'>
            <img src={calendarIcon} alt=""/>
            <div className='date-link'>Открыть календарь</div>
            <input name='date' type="date" style={{marginLeft: 50}}/>
          </div>
        </div>
        
        <div className='time-l label'>Время:</div>
        <div className='time flex'>
          <span>c</span>
          <input name='time_start' type="time"/>
          <span>до</span>
          <input name='time_end' type="time"/>
        </div>
        
        <div className='workspace-l label'>Помещение для лекции:</div>
        <div className='workspace flex'>
          <div className={place ? 'pill pill-blue': 'pill'}
               onClick={() => props.SwapPlace(true)}>Есть</div>
          <div className={place ? 'pill' : 'pill pill-blue'}
               onClick={() => props.SwapPlace(false)}>Нет</div>
        </div>
        
        <div className={place ? 'address-l label' : 'address-l label disabled'}>Адрес:</div>
        <div className='address flex'>
          <textarea name='hall_address' 
                    className='text-area' 
                    placeholder='Введите адрес помещения для лекций'
                    rows='4'
                    readOnly={!place}/>
        </div>
        
        <div className='equip-l label'>Оборудование:</div>
        <div className='equip flex'>
          <textarea name='equipment' 
                    className='text-area' 
                    rows='4'
                    placeholder='Перечислите имеющееся для лекции оборудование'/>
        </div>
        
        <div className='desc-l label'>Описание:</div>
        <div className='desc flex'>
          <textarea name='description' 
                    className='text-area' 
                    rows='5'
                    placeholder='Опишите лекцию'/>
        </div>
        
        <div className='fee-l label'>Цена лекции:</div>
        <div className='fee'>
          <div className='flex'>
            <div className={payment ? 'pill pill-blue' : 'pill'} 
                 onClick={() => props.SwapPayment(true)}>Платно</div>
            <div className={payment ? 'pill' : 'pill pill-blue'} 
                 onClick={() => props.SwapPayment(false)}>Бесплатно</div>
          </div>
          {payment ? <input name='cost' 
                            className='text-input' 
                            type='number' 
                            placeholder='Укажите цену'/> : <></>}
        </div>
        <div className='submit'>
          <button className='big-button' type='submit'>Создать</button>
        </div>
      </div>
    </form>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdatePhoto: (photo) => dispatch(UpdatePhoto(photo)),
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    SwapEventType: (type) => dispatch(SwapEventType(type)),
    SwapPlace: (place) => dispatch(SwapPlace(place)),
    SwapPayment: (payment) => dispatch(SwapPayment(payment)),
  })
)(CreateEvent)


export function addPhotoHandler(inputEvent, UpdatePhoto) {
  let file = inputEvent.target.files[0]
  let reader = new FileReader()
  reader.readAsDataURL(file);
  
  reader.onload = () => {
    UpdatePhoto(reader.result)
  }
}

export function domainSelectHandler(e, props) {
  if (props.store.event.domain.length >= 10) return e.target.value = '';
  let selectedDomain = e.target.selectedOptions[0].innerHTML;
  
  props.UpdateDomain(selectedDomain);
  e.target.value = '';
}