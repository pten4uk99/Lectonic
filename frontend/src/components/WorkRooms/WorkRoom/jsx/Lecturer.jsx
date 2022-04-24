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

  useEffect(() => {
    if (props.store.permissions.is_lecturer && props.store.permissions.logged_in) {
      getConfirmedLectures('customer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setConfirmedLectures(data.data)
        })
        .catch((error) => console.log(error))
      
      getLecturesHistory('lecturer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setLecturesHistory(data.data)
        })
        .catch((error) => console.log(error))
      
      getCreatedLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLectures(data.data)
        })
        .catch((error) => console.log(error))
      
      getAllLecturesForLecturer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setPotentialLectures(data.data)
        })
        .catch((error) => console.log(error))
    }
  }, [])
  
  return (
    <article className="lecturer__content">
      <CreatedLectures role='lecturer'
                       data={createdLectures} 
                       setData={setCreatedLectures}/>
      <LectureCardList header='Потенциальные заказы' 
                       isLecturer={true}
                       data={potentialLectures}/>
      <LectureCardList header='История' 
                       isLecturer={true}
                       data={lecturesHistory}/>
      <LectureCardList header='Подтвержденные лекции' 
                 isLecturer={true}
                 data={confirmedLectures}/>

    </article>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Lecturer);