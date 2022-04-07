import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import WorkroomCard from "./WorkroomCard";
import CreatedLectures from "~@/WorkRooms/WorkRoom/jsx/Elements/CreatedLectures";
import LectureCardList from "./Elements/LectureCardList";
import {getAllLecturersForCustomer, getAllLecturesForCustomer, getCreatedLecturesForCustomer} from "../ajax/workRooms";
import LecturersList from "./Elements/LecturersList";


function Customer(props) {
  let [createdLectures, setCreatedLectures] = useState([])
  let [potentialLectures, setPotentialLectures] = useState([])
  let [lecturersList, setLecturersList] = useState([])
  
  useEffect(() => {
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
    
  }, [])
    return (
        <article className="customer__content">
          <CreatedLectures role='customer' 
                           data={createdLectures}/>
          <LectureCardList header='Новые лекции' 
                           isLecturer={false}
                           data={potentialLectures}/>
          <LecturersList data={lecturersList}/>
        </article>
    )
}

export default connect(
  state => ({store: state}),
  dispatch => ({})
)(Customer);