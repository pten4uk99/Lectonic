import React from "react";
import {connect} from "react-redux";
import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {useNavigate} from "react-router-dom";
import {getCities} from "~@/Profile/ajax/profile";
import {getDomainArray} from "~@/WorkRooms/CreateEvent/ajax/event"
import DropDown from "~@/Utils/jsx/DropDown";



function CreatedLectures(props){
  let navigate = useNavigate()
 
    return (
        <section className="block__created-lectures">
          <div className="workroom__block-header">
            <span>Созданные лекции</span>
            <img src={tooltip} alt="Подсказка"/>
          </div>
          
          <div className="cards-block">
            <div className="new-lecture" onClick={() => navigate('/create_event')}>
              <WorkroomCard data={{
                  name: 'Создать лекцию',
                  createLecture: true,
              }}/>
            </div>
            <DropDown request={getDomainArray} width={true} placeholder='10:00'/>
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