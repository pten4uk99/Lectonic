import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import {
  getAllLecturesForLecturer, getConfirmedLectures,
  getCreatedLecturesForLecturer, getLecturesHistory
} from "../ajax/workRooms";
import LectureCardList from "./Elements/LectureCardList";


function Lecturer(props){
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])
  let [confirmedLectures, setConfirmedLectures] = useState([])
  let [lecturesHistory, setLecturesHistory] = useState([])
  
  let [createdError, setCreatedError] = useState(false)
  let [potentialError, setPotentialError] = useState(false)
  let [confirmedError, setConfirmedError] = useState(false)
  let [historyError, setHistoryError] = useState(false)

  useEffect(() => {
    if (props.store.permissions.is_lecturer && props.store.permissions.logged_in) {
      getConfirmedLectures('customer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setConfirmedLectures(data.data)
          else setConfirmedError(true)
        })
        .catch(() => setConfirmedError(true))
      
      getCreatedLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLectures(data.data)
          else setCreatedError(true)
        })
        .catch(() => setCreatedError(true))
      
      getAllLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setPotentialLectures(data.data)
          else setPotentialError(true)
        })
        .catch(() => setPotentialError(true))
    }
  }, [])
  
  return (
    <article className="lecturer__content">
      <CreatedLectures role='lecturer'
                       data={createdLectures} 
                       setData={setCreatedLectures} 
                       isError={createdError}/>
      <LectureCardList header='Потенциальные заказы' 
                       isLecturer={true}
                       data={potentialLectures} 
                       isError={potentialError}/>
      <LectureCardList header='Подтвержденные лекции' 
                       isLecturer={true} 
                       data={confirmedLectures} 
                       isError={confirmedError}/>
    </article>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer);