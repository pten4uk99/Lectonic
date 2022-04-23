import React, {useEffect, useState} from "react";

import lectureBg from '~/assets/img/lecture-bg.png'
import backArrowWhite from '~/assets/img/back-arrow-white.svg'
import LectureDates from "./LectureDates";
import {useNavigate, useSearchParams} from "react-router-dom";
import {getLectureDetail} from "../ajax/lecture";
import {getLecturePhoto, reverse} from "../../../../ProjectConstants";
import {toggleResponseOnLecture} from "../../../WorkRooms/WorkRoom/ajax/workRooms";
import {connect} from "react-redux";
import {RemoveNotification} from "../../../Layout/redux/actions/notifications";
import PhotoName from "../../../Utils/jsx/PhotoName";
import {UpdateLectureDetailChosenDates} from "../redux/actions/lectureDetail";
import Loader from "../../../Utils/jsx/Loader";


function Lecture(props) {
  let [isLoaded, setIsLoaded] = useState(false)
  let [responseLoaded, setResponseLoaded] = useState(true)
  
  let userId = props.store.permissions.user_id
  let [searchParams, setSearchParams] = useSearchParams()
  let navigate = useNavigate()
  let lectureId = searchParams.get('id')
  
  let [lectureData, setLectureData] = useState(null)
  let [isCreator, setIsCreator] = useState(null)
  let [confirmedRespondent, setConfirmedRespondent] = useState(null)
  
  useEffect(() => {
    props.UpdateLectureDetailChosenDates([])
    
    getLectureDetail(lectureId)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          setIsLoaded(true)
          setLectureData(data.data[0])
          setIsCreator(data.data[0].creator_user_id === userId)
          data.data[0].response_dates.forEach(elem => {
            if (elem.confirmed) setConfirmedRespondent(true)
          })
        }
        else if (data.status === 'error') navigate(reverse('404'))
      })
      .catch(e => console.log(e))
  }, [])
  
  function handleResponse(e) {
    if (!responseLoaded) return
    setResponseLoaded(false)
    let text = e.target.innerText
    let dates = props.store.lectureDetail.chosenDates.map(
      elem => `${elem.getUTCFullYear()}-${elem.getUTCMonth() + 1}-${elem.getUTCDate()}T${elem.getUTCHours()}:${elem.getUTCMinutes()}`)
    
    toggleResponseOnLecture(lectureId, dates)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          setResponseLoaded(true)
          text === 'Откликнуться' ? 
            e.target.innerText = 'Отменить отклик' : 
            e.target.innerText = 'Откликнуться'
          if (data.data[0]?.type === 'remove_respondent') {
            props.UpdateLectureDetailChosenDates([])
            props.RemoveNotification(data.data[0].id)
          }
          navigate(reverse('workroom'))
        }
      })
  }
  
  function checkDisabledButton() {
    if (props.store.lectureDetail.chosenDates.length < 1 || confirmedRespondent) return true
  }
  
  if (!isLoaded) return <Loader main={true}/>
  return (
    <>
      <div className="navigate-back__block"
           onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrowWhite} alt="назад" style={{fill: 'white'}}/>
      </div>
      
      <div className="lecture__container">
        <div className="header__picture">
          <img src={lectureBg} alt="задний фон"/>
        </div>
        
        <div className="lecture__wrapper">
          
          <div className="left-block">
            <div className="lecture-photo"><img src={getLecturePhoto(lectureData?.svg)} alt=""/></div>
            <div className="subheader">
              <div className="type blue">{lectureData?.creator_is_lecturer ? "Лекция" : "Запрос на лекцию"}</div>
              <div className="type">{lectureData?.lecture_type}</div>
            </div>
            <div className="block__person" 
                 onClick={() => lectureData?.creator_is_lecturer ? 
                   navigate(reverse('role_page', {lecturer: lectureData.creator_id})) : 
                   navigate(reverse('role_page', {customer: lectureData.creator_id})) }>
              <div className="header">{lectureData?.creator_is_lecturer ? "Лектор:" : "Заказчик:"}</div>
              <div className="block__data">
                <div className="person-photo">
                  {lectureData?.creator_photo ?
                    <img src={lectureData.creator_photo} alt="фото"/> :
                    lectureData && <PhotoName firstName={lectureData?.creator_first_name}
                               lastName={lectureData?.creator_last_name}
                               size={90}/>
                  }
                </div>
                <div className="person-data">
                  <span>{lectureData?.creator_last_name}</span>
                  <span>{lectureData?.creator_first_name}</span>
                  <span>{lectureData?.creator_middle_name}</span>
                </div>
              </div>
            </div>
            <div className="block__equipment">
              <div className="header">Оборудование в наличии:</div>
              <span className="content">{lectureData?.equipment ? lectureData.equipment : 'Нет'}</span>
            </div>
            <div className="block__cost">
              <div className="header">Стоимость:</div>
              <span className="content">{lectureData?.cost} р.</span>
            </div>
          </div>
          
          <div className="right-block">
            <div className="lecture-name">{lectureData?.lecture_name}</div>
            <div className="block__domains">
              {lectureData?.domain && lectureData.domain.map((elem, index) => {
                return <div className="domain" key={index}>{elem}</div>
              })}
            </div>
            <div className="block__dates">
              <div className="header">
                {lectureData?.creator_is_lecturer ? 
                  "Лектор готов провести лекцию:" : "Заказчик готов послушать лекцию:"}
              </div>
              <LectureDates data={lectureData?.dates} responseDates={lectureData?.response_dates}/>
            </div>
            <div className="block__address">
              <div className="header">Место проведения:</div>
              <span>{lectureData?.hall_address || "Не согласовано"}</span>
            </div>
            <div className="block__description">
              <div className="header">Описание:</div>
              <span>{lectureData?.description || "Нет"}</span>
            </div>
            {!isCreator && 
              <button className="btn btn-response" 
                      disabled={checkDisabledButton()} 
                      onClick={(e) => handleResponse(e)}>
                {!responseLoaded ? 
                  <Loader size={20} 
                          left="50%" 
                          top="50%" 
                          tX="-50%" tY="-50%"/> : 
                  confirmedRespondent ? "Лекция подтверждена" : 
                    lectureData?.can_response ? 
                      "Откликнуться" : "Отменить отклик"}
              </button>}
          </div>
          
        </div>
      </div>
    </>
  );
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    RemoveNotification: (data) => dispatch(RemoveNotification(data)),
    UpdateLectureDetailChosenDates: (dates) => dispatch(UpdateLectureDetailChosenDates(dates))
  })
)(Lecture);
