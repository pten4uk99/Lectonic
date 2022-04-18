import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import tooltip from "~/assets/img/workrooms/workroom/tooltip.svg";
import WorkroomCard from "../WorkroomCard";
import {useNavigate} from "react-router-dom";
import {getLecturePhoto, reverse} from "../../../../../ProjectConstants";
import {getDates} from "./LectureCardList";
import Loader from "../../../../Utils/jsx/Loader";
import {deleteLecture} from "../../ajax/workRooms";
import ConfirmAction from "../../../../Utils/jsx/ConfirmAction";
import {ActivateModal, DeactivateModal} from "../../../../Layout/redux/actions/header";



function CreatedLectures(props){
  let [isLoaded, setIsLoaded] = useState(false)
  let [selectedLecture, setSelectedLecture] = useState(null)
  let navigate = useNavigate()
  
  useEffect(() => {
    if (props.data) setIsLoaded(true)
  }, [props.data])

  
  function handleDeleteLecture(lecture_id) {
    setSelectedLecture(lecture_id)
    props.ActivateModal()
  }
  
  function handleConfirmDelete() {
    deleteLecture(selectedLecture)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'deleted') {
          let newData = props.data.filter((elem) => elem.lecture_id !== selectedLecture)
          props.setData(newData)
          props.DeactivateModal()
        }
      })
    setSelectedLecture(null)
  }
  
    return (
        <section className="block__created-lectures">
          {selectedLecture && <ConfirmAction onConfirm={handleConfirmDelete}
                                             onCancel={() => setSelectedLecture(null)}
                                             text="Вы уверены, что хотите удалить событие?"/>}
          <div className="workroom__block-header">
            {props.role === 'lecturer' && <span>Созданные лекции</span>}
            {props.role === 'customer' && <span>Мои запросы на лекции</span>}
            <img src={tooltip} alt="Подсказка"/>
            {!isLoaded && <Loader size={15} left={12}/>}
          </div>
          
          <div className="cards-block mt-20">
            <div className="new-lecture" 
                 onClick={() => navigate(reverse('create_event', {role: props.role}))}>
              <WorkroomCard data={{
                  name: props.role === 'lecturer' ? 'Создать лекцию' : 'Создать запрос на лекцию',
                  createLecture: true,
              }}/>
            </div>
            {props.data.length > 0 && 
              <div className="created-lectures__wrapper">
                <div className="created-lectures">
                  {props.data.map((lecture) => {
                    return <WorkroomCard key={lecture.id} 
                                         data={{
                                           src: getLecturePhoto(lecture.svg),
                                           client: !props.isLecturer ? 'Лектор:' : 'Заказчик:',
                                           clientName: `${lecture.creator_first_name} ${lecture.creator_last_name}`,
                                           name: lecture.name,
                                           date: getDates(lecture.dates),
                                           description: lecture.description,
                                           city: lecture.hall_address,
                                           textBtn: 'Подробнее',
                                           createdLecture: true,
                                         }} 
                                         onClick={() => navigate(reverse('lecture', {id: lecture.id}))} 
                                         canDelete={true} 
                                         onDelete={() => handleDeleteLecture(lecture.id)}/>})}
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
    ActivateModal: () => dispatch(ActivateModal()),
    DeactivateModal: () => dispatch(DeactivateModal()),
  })
)(CreatedLectures);