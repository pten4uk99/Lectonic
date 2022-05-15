import React, {useEffect, useRef, useState} from 'react'
import {connect} from "react-redux";
import {useNavigate, useSearchParams} from "react-router-dom";

import calendarIcon from '~/assets/img/event/calendar-icon.svg'
import backArrow from '~/assets/img/back-arrow.svg'
import {
  SwapEventType, SwapPayment, SwapPlace, SwapEquipment,
  UpdateDomain,
  UpdatePhoto,
  DeleteDomain
} from "../redux/actions/event";
import {createEvent, getDomainArray} from "../ajax/event";
import {reverse} from "../../../../ProjectConstants";
import Modal from "../../../Layout/jsx/Modal";
import {ActivateModal} from "../../../Layout/redux/actions/header";
import CalendarModal, {getMonth} from "./CalendarModal";
import DropDown from "../../../Utils/jsx/DropDown";
import btnDelete from '~/assets/img/btn-delete.svg';
import {SwapModalChooseDates} from "../../FullCalendar/Calendar/redux/actions/calendar";
import Loader from "../../../Utils/jsx/Loader";


function CreateEvent(props) {
  let [responseLoaded, setResponseLoaded] = useState(true)
  let navigate = useNavigate()
  let [searchParams, setSearchParams] = useSearchParams()
  useEffect(() => {
    if (
      !props.store.permissions.is_lecturer && 
      !props.store.permissions.is_customer
    ) navigate(reverse('add_role'))
  }, [props.store.permissions.is_lecturer, props.store.permissions.is_customer])

  let role = searchParams.get('role')
  
  let chooseDates = props.store.calendar.modalChooseDates
  let duration = props.store.calendar.chosenDuration
  let selectedDomains = props.store.event.domain
  let eventType = props.store.event.type
  let place = props.store.event.place
  let equipment = props.store.event.equipment
  let payment = props.store.event.payment
  let titlePhotoSrc = props.store.event.photo
  let [deletedDomain, setDeletedDomain] = useState();

  function deleteElem (indexElem) {
    props.DeleteDomain(selectedDomains, indexElem);
    domainArray.push(deletedDomain);
    setDomainArray(domainArray.sort((a, b) => a.name > b.name ? 1 : -1));
  }
  
  let [requiredFields, setRequiredFields] = useState({
    name: '',
    date: chooseDates,
  })
  
  let [errorMessages, setErrorMessages] = useState({
    name: '',
    datetime: '',
  })
  
  useEffect(() => {
    setRequiredFields({...requiredFields, date: chooseDates})
  }, [chooseDates])
  
  let [domainArray, setDomainArray] = useState()

  useEffect(() => {
    if (role === 'customer') setRequiredFields({...requiredFields, listeners: ''})
    props.UpdatePhoto('')
    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])
  
  useEffect(() => {
    if (selectedDomains.length > 0 && domainArray) {
      let newDomainArray
      newDomainArray = domainArray.filter(elem => !selectedDomains.includes(elem.name))
      setDomainArray(newDomainArray)
    }
  }, [selectedDomains])
  
  function domainSelectHandler(value, setValue, index) {
    if (props.store.event.domain.length >= 10) return setValue('')
    props.UpdateDomain(value)
    setValue('')
  }
  
  function submitFormHandler(e) {
    setResponseLoaded(false)
    e.preventDefault()
    let formData = new FormData(e.target)
    selectedDomains.map((elem) => formData.append('domain',  elem))
    for (let date of chooseDates) formData.append(
      'datetime',
      (`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}T${date.getHours()}:${date.getMinutes()}` + 
      ',' +
      `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}T${getStrTime(date.getHours(), date.getMinutes(), duration)}`)
    )
    formData.set('type', eventType)
    formData.set('svg', String(1 + Math.floor(Math.random() * 10)))
    createEvent(formData, role)
      .then(response => response.json())
      .then(data => {
        setResponseLoaded(true)
        if (data.status === 'created') navigate(reverse('workroom'))
        else {
          setErrorMessages({
            name: data?.name,
            datetime: data?.datetime,
            listeners: data?.listeners
          })
        }
      })
      .catch(() => e.target.innerText = 'Ошибка...')
  }

  return (
    <>
      <div className="navigate-back__block" onClick={() => navigate(-1)}>
        <img src={backArrow} alt="назад"/>
      </div>

      <form onSubmit={(e) => submitFormHandler(e)}>
        <div className={role === 'customer' ? 'create-event__wrapper customer' : 'create-event__wrapper'}>
          <div className='heading'>
            <h1 className='main-heading'>{role === 'lecturer' ? 
              "Создание мероприятия" : "Создание заказа на мероприятие"}</h1>
          </div>
          <div className='subheading'>
            <h2 className='main-subheading'>
              {role === 'lecturer' ? 
                "Вы можете создать одно или несколько мероприятий, " +
                "чтобы потенциальне слушатели могли откликнуться." :
                "Вы можете создать один или несколько заказов на мероприятие, " +
                "чтобы потенциальне лекторы могли откликнуться."
              }
            </h2>
          </div>
          
          {/*<div className='cover-l label'>*/}
          {/*  Обложка:*/}
          {/*  <span className="required-sign step-block__required-sign">*</span>*/}
          {/*</div>*/}
          {/*<label className={titlePhotoSrc ? 'cover' : 'cover no-photo'}>*/}
          {/*  <img className='icon' */}
          {/*       src={photoIcon} */}
          {/*       alt='photo-icon'/>*/}
          {/*    <span className='add-photo'>Добавить фото</span>*/}
          {/*    <input name='photo'*/}
          {/*           className='add-photo__input'*/}
          {/*           type='file'*/}
          {/*           onChange={e => addPhotoHandler(e, props.UpdatePhoto)}/>*/}
          {/*  <img className='title-img'*/}
          {/*       src={titlePhotoSrc}*/}
          {/*       alt='Обложка'/>*/}
          {/*</label>*/}
          
          <div className='domain-l label'>
            Тематика:
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <div className='domains'>
            <div className='domain-list flex'>
              <DropDown request={domainArray} 
                    width={true} 
                    placeholder='Выберите тематику' 
                    onSelect={(value, setValue) => domainSelectHandler(value, setValue)} 
                    domainArr={true}/>
            </div>
            <div className="step-block mt-12">
              <div className='domain-list flex'>
                {selectedDomains.map((domain, index) => {
                  return <div key={index} className='pill pill-grey'
                              onMouseUp={() => {setDeletedDomain({name: domain})}}>
                                {domain}
                                <div className='pill-btn-delete' 
                                  onClick={() => deleteElem(index)}>
                                  <img src={btnDelete} alt="delete"/>
                                </div>
                        </div>
                })}
        </div>
      </div>
          </div>
          
          <div className='topic-l label'>
            Тема лекции:
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <div className='topic flex'>
            <input name='name' 
                   type='text' 
                   className='text-input' 
                   autoComplete='none'
                   onChange={(e) => setRequiredFields({...requiredFields, name: e.target.value})}/>
          </div>
          {errorMessages.name && (<div className='form__input-error' 
                                       style={{
                                             gridArea: 'topic',
                                             transform: 'translateY(25px)'
                                           }}>{errorMessages.name[0]}</div>)}
          <div className='type-l label'>Тип лекции:</div>
          <div className='type flex'>
            <div className={eventType !== 'online' ? 'pill' : 'pill pill-blue'} 
                 onClick={() => props.SwapEventType('online')}>Онлайн</div>
            <div className={eventType !== 'offline' ? 'pill' : 'pill pill-blue'} 
                 onClick={() => props.SwapEventType('offline')}>Оффлайн</div>
            <div className={eventType !== 'hybrid' ? 'pill' : 'pill pill-blue'} 
                 onClick={() => props.SwapEventType('hybrid')}>Гибрид</div>
          </div>
          
          <div className='date-l label'>
            Дата:
            <span className="required-sign step-block__required-sign">*</span>
          </div>
          <div className='date flex'>
            <div className='open-calendar' onClick={props.ActivateModal}>
              <img src={calendarIcon} alt=""/>
              {chooseDates.length > 0 ? 
                chooseDates.map((elem, index) => (
              <div className="calendar-modal__date create-event ml-8" key={index}>
                {elem.getDate()} {getMonth(elem.getMonth())}
              </div>)) : 
                <div className='date-link'>Открыть календарь</div>}
              
            </div>
            <Modal styleWrapper={{background: 'background: rgba(0, 5, 26, 1)'}} 
                   styleBody={{width: 1045, height: 681}} 
                   onCancel={() => props.SwapModalChooseDates([])}>
                <CalendarModal/>
            </Modal>
          </div>
          {errorMessages.datetime && (<div className='form__input-error' 
                                           style={{
                                             gridArea: 'date',
                                             transform: 'translateY(25px)'
                                           }}>{errorMessages.datetime[0]}</div>)}

          {role === 'customer' && 
            <>
              <div className='listeners-l label'>
                Количество слушателей:
                <span className="required-sign step-block__required-sign">*</span>
              </div>
              <div className='listeners flex'>
                <input name='listeners' 
                       type='text'
                       className='text-input'
                       autoComplete='nope'
                       onChange={(e) => {
                         setRequiredFields({...requiredFields, listeners: e.target.value})
                         onlyNumber(e, 5)
                       }}/>
              </div>
            </>}
            {errorMessages.listeners && (<div className='form__input-error' 
                                   style={{
                                     gridArea: 'listeners',
                                     transform: 'translateY(25px)'
                                   }}>{errorMessages.listeners[0]}</div>)}
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

          <div className='workspace-2 label'>Оборудование:</div>
          <div className='workspace-btn flex'>
            <div className={equipment ? 'pill pill-blue': 'pill'}
                 onClick={() => props.SwapEquipment(true)}>Есть</div>
            <div className={equipment ? 'pill' : 'pill pill-blue'}
                 onClick={() => props.SwapEquipment(false)}>Нет</div>
          </div>
          
          <div className={equipment ? 'equip-l label' : 'equip-l label disabled'}>Список оборудования:</div>
          <div className='equip flex'>
            <textarea name='equipment' 
                      className='text-area' 
                      rows='4'
                      placeholder='Перечислите имеющееся для лекции оборудование'
                      readOnly={!equipment}/>
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
            {payment ? <><input name='cost' 
                              className='text-input' 
                              type='text'
                              placeholder='Укажите цену' 
                              onChange={(e) => onlyNumber(e, 7)}/> <span>руб.</span></> : 
              <></>}
          </div>
          <div className='submit'>
            <button className='btn big-button' 
                    type='submit' 
                    disabled={checkRequiredFields(requiredFields, props)}>
              {!responseLoaded ? 
                <Loader size={20} left="50%" top="50%" tX="-50%" tY="-50%"/> : 
                'Создать'}
            </button>
          </div>
        </div>
      </form>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    ActivateModal: () => dispatch(ActivateModal()),
    UpdatePhoto: (photo) => dispatch(UpdatePhoto(photo)),
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    DeleteDomain: (domain, i) => dispatch(DeleteDomain(domain, i)),
    SwapEventType: (type) => dispatch(SwapEventType(type)),
    SwapPlace: (place) => dispatch(SwapPlace(place)),
    SwapEquipment: (equipment) => dispatch(SwapEquipment(equipment)),
    SwapPayment: (payment) => dispatch(SwapPayment(payment)),
    SwapModalChooseDates: (dates) => dispatch(SwapModalChooseDates(dates)),
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

function checkRequiredFields(obj, props) {
  if ((props.store.event.domain.length < 1)) return true
  
  for (let field in obj) {
    if (!obj[field]) return true
  }
  return false
}

function getStrTime(hour, minute, duration) {
  let oldMinutes = hour * 60 + minute
  let newMinutes = oldMinutes + duration
  let newHour = newMinutes / 60
  let newMinute = newMinutes % 60
  
  if (newHour < 1) return `00:${newMinute}`
  else return `${Math.floor(newHour)}:${newMinute}`
}

function onlyNumber(e, maxLength) {
  if (isNaN(Number(e.target.value)) || e.target.value.length > maxLength) {
    e.target.value = e.target.value.slice(0, -1)
  }
  else if (e.target.value.length === 1 && e.target.value == 0) {
    e.target.value = e.target.value.slice(0, -1)
  }
}