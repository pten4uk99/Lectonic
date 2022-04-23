import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import LectureCardList from "./Elements/LectureCardList";
import {
  getAllLecturersForCustomer,
  getAllLecturesForCustomer, getConfirmedLectures,
  getCreatedLecturesForCustomer, getLecturesHistory
} from "../ajax/workRooms";
import LecturersList from "./Elements/LecturersList";


function Customer(props) {
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])
  let [confirmedLectures, setConfirmedLectures] = useState([])
  let [lecturesHistory, setLecturesHistory] = useState([])
  let [lecturersList, setLecturersList] = useState([])
  
  useEffect(() => {
    if (props.store.permissions.is_customer && props.store.permissions.logged_in) {
      getConfirmedLectures('lecturer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setConfirmedLectures(data.data)
        })
        .catch((error) => console.log(error))
      
      getLecturesHistory('customer')
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setLecturesHistory(data.data)
        })
        .catch((error) => console.log(error))
          
      getCreatedLecturesForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setCreatedLectures(data.data)
        })
        .catch((error) => console.log(error))
      
      getAllLecturesForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setPotentialLectures(data.data)
        })
        .catch((error) => console.log(error))
      
      getAllLecturersForCustomer()
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') setLecturersList(data.data)
        })
        .catch((error) => console.log(error))
    }
  }, [])
    return (
        <article className="customer__content">
          <CreatedLectures role='customer' 
                           data={createdLectures}/>
          <LectureCardList header='Новые лекции' 
                           isLecturer={false}
                           data={potentialLectures}/>          
          <LectureCardList header='История' 
                           isLecturer={false}
                           data={lecturesHistory}/>
          <LectureCardList header='Подтвержденные лекции' 
                           isLecturer={true} 
                           data={confirmedLectures}/>
          <LecturersList data={lecturersList}/>
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Customer);