import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {getNotificationsList} from "../../ajax";


function NotificationsList(props) {
  let [notifications, setNotifications] = useState([])
  
  useEffect(() => {
    getNotificationsList()
      .then(r => r.json())
      .then(data => setNotifications(data.data))
  }, [])
  
  return (
    <div className="notifications-list__block">
      <div className="notification__header">Отклики</div>

      {notifications.map((elem) => {
        return <li key={elem.id} className="chat-dropdown__notification" onClick={() => props.setArea(true)}>
          <div className="photo"><img src={elem.lecture_photo} alt="обложка"/></div>
          <div className="text">
            <p className='lecture-name'>{elem.lecture_name}</p>
            <p className='respondent-name'>Отклик: {elem.respondent_first_name} {elem.respondent_last_name}</p>
          </div>
        </li>
      })}
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(NotificationsList);