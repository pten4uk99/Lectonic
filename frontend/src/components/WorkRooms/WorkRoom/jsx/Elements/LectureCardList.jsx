import React, {useState} from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {DateTime} from "luxon";
import {toggleResponseOnLecture} from "../../ajax/workRooms";
import {RemoveNotification} from "../../../../Layout/redux/actions/notifications";


function LectureCardList(props){

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
                                           client: !props.isLecturer ? 'Лектор:' : 'Заказчик:', 
                                           clientName: `${lecture.creator_first_name} ${lecture.creator_last_name}`, 
                                           name: lecture.lecture_name, 
                                           date: getDates(lecture.dates), 
                                           description: lecture.description, 
                                           city: lecture.hall_address, 
                                           textBtn: lecture.in_respondents ? 'Отменить отклик' : 'Откликнуться', 
                                           potentialLecture: true,
                                         }} 
                                         onClick={(e) => handleResponse(e, lecture.lecture_id, lecture.dates)}/>})}
                </div>
            </div>}
          </div>
          
          <div className="workroom__block-underline"/>
        </section>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    RemoveNotification: (data) => dispatch(RemoveNotification(data)),
  })
)(LectureCardList);


export function getDates(str_dates) {
  let dates = []
  for (let date of str_dates) {
    dates.push(DateTime.fromISO(date).toFormat('dd.MM'))
  }
  return dates.join(', ')
}