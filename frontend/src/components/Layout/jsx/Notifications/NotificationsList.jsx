import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {getChatMessages, getNotificationsList} from "../../ajax";
import {createChatSocket} from "../../../../webSocket";
import {UpdateMessages} from "../../redux/actions/messages";
import {SetNeedRead} from "../../redux/actions/notifications";
import {SetSelectedChat} from "../../redux/actions/header";
import {getLecturePhoto} from "../../../../ProjectConstants";


function NotificationsList(props) {
  let chatList = props.store.notifications
  
  function handleNotificationClick(chat_id) {
    props.setArea(true)
    createChatSocket(props.setChatSocket, chat_id)
    getChatMessages(chat_id)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          props.UpdateMessages(data.data[0])
          props.SetNeedRead(chat_id, false)
          props.SetSelectedChat(chat_id)
        }
      })
  }

  return (
    <div className="notifications-list__block">
      <div className="notification__header">Отклики</div>

      {chatList.length > 0 ? chatList.map((elem) => {
        return <li key={elem.id} 
                   className="chat-dropdown__notification" 
                   onClick={() => handleNotificationClick(elem.id)}>
          <div className="photo"><img src={getLecturePhoto(elem.lecture_svg)} alt="обложка"/></div>
          <div className="text">
            <p className='lecture-name'>{elem.lecture_name}</p>
            <p className='respondent-name'>{elem.respondent_first_name} {elem.respondent_last_name}</p>
          </div>
          {elem.need_read && <div className="need-read"/>}
        </li>
      }) :
        <div className="empty-list">
          Здесь будут отображаться отклики на ваши неподтвержденные лекции
        </div>
      }
      
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateMessages: (data) => dispatch(UpdateMessages(data)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
  })
)(NotificationsList);