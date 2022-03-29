import React, {useState} from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {useNavigate} from "react-router-dom";
import {getCities} from "~@/Profile/ajax/profile";
import {getDomainArray} from "~@/WorkRooms/CreateEvent/ajax/event"
import DropDown from "~@/Utils/jsx/DropDown";
import {reverse} from "../../../../../ProjectConstants";
import {DateTime} from "luxon";
import {toggleResponseOnLecture} from "../../ajax/workRooms";



function LectureCardList(props){

  function handleResponse(e, lecture_id) {
    let text = e.target.innerText
      
    toggleResponseOnLecture(lecture_id)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          text === 'Откликнуться' ? 
            e.target.innerText = 'Отменить отклик' : 
            e.target.innerText = 'Откликнуться'
        }
      })
  }
  
    return (
        <section className="block__created-lectures">
          <div className="workroom__block-header">
            <span>{props.header}</span>
            <img src={tooltip} alt="Подсказка"/>
          </div>
          
          <div className="cards-block minus-ml-20">
            {props.data.length > 0 && 
              <div className="created-lectures__wrapper">
                <div className="created-lectures">
                  {props.data.map((lecture, index) => {
                    return <WorkroomCard key={index} 
                                         data={{
                                           src: lecture.photo, 
                                           client: 'Заказчик:', 
                                           clientName: `${lecture.creator_first_name} ${lecture.creator_last_name}`, 
                                           name: lecture.lecture_name, 
                                           date: getDates(lecture.dates), 
                                           description: lecture.description, 
                                           city: lecture.hall_address, 
                                           textBtn: lecture.in_respondents ? 'Отменить отклик' : 'Откликнуться', 
                                           potentialLecture: true,
                                         }} 
                                         onClick={(e) => handleResponse(e, lecture.lecture_id)}/>})}
                </div>
            </div>}
          </div>
          
          <div className="workroom__block-underline"/>
        </section>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(LectureCardList);


function getDates(str_dates) {
  let dates = []
  for (let date of str_dates) {
    dates.push(DateTime.fromISO(date).toFormat('dd.MM.yyyy'))
  }
  return dates.join(', ')
}