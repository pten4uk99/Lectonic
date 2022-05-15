import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {DateTime} from "luxon";
import {toggleResponseOnLecture} from "../../ajax/workRooms";
import {RemoveNotification} from "../../../../Layout/redux/actions/notifications";
import {getLecturePhoto, reverse} from "../../../../../ProjectConstants";
import {useNavigate} from "react-router-dom";
import Loader from "../../../../Utils/jsx/Loader";


function LectureCardList(props) {
  let [isLoaded, setIsLoaded] = useState(false)
  let navigate = useNavigate()
  
  function getClientName(lecture) {
    if (lecture?.related_person) {
      return `${lecture.related_person.first_name} ${lecture.related_person.last_name}`
    }
    else {
      return `${lecture.creator_first_name} ${lecture.creator_last_name}`
    }
  }
  
  useEffect(() => {
    if (props.data) setIsLoaded(true)
  }, [props.data])
  
    return (
        <section className="block__created-lectures">
          {!props?.inPage && 
            <div className="workroom__block-header">
              <span>{props.header}</span>
              <img src={tooltip} alt="Подсказка"/>
              {!isLoaded && <Loader size={15} left={12}/>}
          </div>}
          
          <div className="cards-block minus-ml-20">
            {props.isError ? 
              <div className="lecture-cards__error">Ошибка загрузки данных</div> : 
              props.data.length > 0 &&
                <div className="created-lectures__wrapper">
                  <div className="created-lectures">
                    {props.data.map((lecture) => {
                      return <WorkroomCard key={lecture.id} 
                                           data={{
                                             src: getLecturePhoto(lecture.svg), 
                                             client: !props.isLecturer ? 'Лектор:' : 'Заказчик:', 
                                             clientName: getClientName(lecture), 
                                             name: lecture.name, 
                                             date: getDates(lecture.dates), 
                                             type: lecture.lecture_type, 
                                             city: lecture.hall_address, 
                                             textBtn: 'Подробнее', 
                                             potentialLecture: true,
                                           }} 
                                           onClick={(e) => navigate(reverse('lecture', {id: lecture.id}))}/>})}
                  </div>
                </div>}
          </div>

          {!props?.inPage && <div className="workroom__block-underline"/>}
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
    dates.push(DateTime.fromISO(date.start).toFormat('dd.MM'))
  }
  return dates.join(', ')
}