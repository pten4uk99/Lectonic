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
          
          <div className="cards-block">
            <div className="new-lecture" onClick={handleCreateLectureCard}>
              <WorkroomCard data={{
                  name: 'Создать лекцию',
                  createLecture: true,
              }}/>
            </div>
            {/*<DropDown request={getDomainArray} width={true} placeholder='10:00'/>*/}
            <div className="created-lectures">
            {/*  <WorkroomCard data={{*/}
            {/*    name: 'Лидеры-доноры',*/}
            {/*    description: 'Лекции от создателей проекта о донорстве',*/}
            {/*    textBtn: 'Статус мероприятия',*/}
            {/*    img: '',*/}
            {/*}}/>*/}
            </div>
          </div>
          
          <div className="workroom__block-underline"/>
        </section>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(CreatedLectures);