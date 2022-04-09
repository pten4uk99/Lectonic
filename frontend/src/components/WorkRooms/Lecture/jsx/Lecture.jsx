import React, {useEffect, useState} from "react";

import lectureBg from '~/assets/img/lecture-bg.svg'
import lecturePhoto from '~/assets/img/default_lecture_photo/1.svg'
import backArrow from '~/assets/img/back-arrow.svg'
import LectureDates from "./LectureDates";
import {useNavigate, useSearchParams} from "react-router-dom";
import {getLectureDetail} from "../ajax/lecture";
import {reverse} from "../../../../ProjectConstants";
import {toggleResponseOnLecture} from "../../WorkRoom/ajax/workRooms";
import {connect} from "react-redux";
import {RemoveNotification} from "../../../Layout/redux/actions/notifications";
import PhotoName from "../../../Utils/jsx/PhotoName";
import {UpdateLectureDetailChosenDates} from "../redux/actions/lectureDetail";


function Lecture(props) {
  let [searchParams, setSearchParams] = useSearchParams()
  let navigate = useNavigate()
  let lectureId = searchParams.get('id')
  
  let [lectureData, setLectureData] = useState(null)
  
  useEffect(() => {
    props.UpdateLectureDetailChosenDates([])
    
    getLectureDetail(lectureId)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') setLectureData(data.data[0])
        else if (data.status === 'error') navigate(reverse('404'))
      })
      .catch(e => console.log(e))
  }, [])
  
  function handleResponse(e, lecture_id, dates) {
    let text = e.target.innerText
      
    toggleResponseOnLecture(lecture_id, dates[0])
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          text === 'Откликнуться' ? 
            e.target.innerText = 'Отменить отклик' : 
            e.target.innerText = 'Откликнуться'
          if (data.data[0]?.type === 'remove_respondent') props.RemoveNotification(data.data[0].id)
        }
      })
  }
  
  function checkDisabledButton() {
    if (props.store.lectureDetail.chosenDates.length < 1) return true
  }
  
  return (
    <>
      <div className="navigate-back__block" style={{top: 220}}
           onClick={() => navigate(reverse('workroom'))}>
        <img src={backArrow} alt="назад"/>
      </div>
      
      <div className="lecture__container">
        <div className="header__picture">
          <img src={lectureBg} alt="задний фон"/>
        </div>
        
        <div className="lecture__wrapper">
          
          <div className="left-block">
            <div className="lecture-photo"><img src={lecturePhoto} alt=""/></div>
            <div className="type">{lectureData?.lecture_type}</div>
            <div className="block__person">
              <div className="header">Лектор:</div>
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
              <div className="header">Лектор готов провести лекцию:</div>
              <LectureDates data={lectureData?.dates}/>
            </div>
            <div className="block__address">
              <div className="header">Место проведения:</div>
              <span>{lectureData?.hall_address || "Не согласовано"}</span>
            </div>
            <div className="block__description">
              <div className="header">Описание:</div>
              <span>{lectureData?.description || "Нет"}</span>
            </div>
            <button className="btn btn-response" disabled={checkDisabledButton()}>Откликнуться</button>
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
