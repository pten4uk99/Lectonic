import React from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {useNavigate} from "react-router-dom";
import {getCities} from "~@/Profile/ajax/profile";
import {getDomainArray} from "~@/WorkRooms/CreateEvent/ajax/event"
import DropDown from "~@/Utils/jsx/DropDown";
import {reverse} from "../../../../../ProjectConstants";



function CreatedLectures(props){
  let navigate = useNavigate()
  
  function handleCreateLectureCard() {
    navigate(reverse('create_event', {role: props.role}))
  }
    return (
        <section className="block__created-lectures">
          <div className="workroom__block-header">
            {props.role === 'lecturer' && <span>Созданные лекции</span>}
            {props.role === 'customer' && <span>Мои запросы на лекции</span>}
            <img src={tooltip} alt="Подсказка"/>
          </div>
          
          <div className="cards-block mt-20">
            <div className="new-lecture" onClick={handleCreateLectureCard}>
              <WorkroomCard data={{
                  name: props.role === 'lecturer' ? 'Создать лекцию' : 'Создать запрос на лекцию',
                  createLecture: true,
              }}/>
            </div>
            {/*<DropDown request={getDomainArray} width={true} placeholder='10:00'/>*/}
            {props.data.length > 0 && 
              <div className="created-lectures__wrapper">
                <div className="created-lectures">
                  {props.data.map((lecture, index) => {
                    return <WorkroomCard key={index} data={{
                      img: lecture.photo,
                      client: 'Заказчик:',
                      clientName: `${lecture.creator_first_name} ${lecture.creator_last_name}`,
                      name: lecture.name,
                      description: lecture.description,
                      textBtn: 'Статус мероприятия',
                    }}/>
                  })}
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
)(CreatedLectures);