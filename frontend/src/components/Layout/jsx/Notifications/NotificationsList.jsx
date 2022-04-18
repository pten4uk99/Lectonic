import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import {getChatMessages, getNotificationsList} from "../../ajax";
import {createChatSocket} from "../../../../webSocket";
import {UpdateMessages} from "../../redux/actions/messages";
import {RemoveNotification, SetNeedRead} from "../../redux/actions/notifications";
import {SetSelectedChat} from "../../redux/actions/header";
import {getLecturePhoto} from "../../../../ProjectConstants";
import {SetChatConnFail} from "../../redux/actions/ws";


function NotificationsList(props) {
  let chatList = props.store.notifications
  let selectedChatId = props.store.header.selectedChatId
  
  useEffect(() => {
    if (selectedChatId && props.store.ws.chatConn) getMessages(selectedChatId)
  }, [props.store.ws.chatConn])
  
  function handleNotificationClick(chat_id) {
    props.setArea(true)
    // createChatSocket(props.setChatSocket, chat_id, props.SetChatConnFail)
  }

  return (
    <div className="notifications-list__block">
      <div className="notification__header">Отклики</div>

      {chatList.length > 0 ? chatList.map((elem) => {
        return <li key={elem.id} 
                   className="chat-dropdown__notification" 
                   onClick={() => props.setChatId(elem.id)}>
          <div className="photo"><img src={getLecturePhoto(elem.lecture_svg)} alt="обложка"/></div>
          <div className="text">
            <p className='lecture-name'>{elem.lecture_name}</p>
            <p className='respondent-name'>{elem.respondent_first_name} {elem.respondent_last_name}</p>
          </div>
          {elem.need_read && <div className="need-read"/>}
        </li>
      }) :
        <div className="empty-list">
          Здесь будут отображаться отклики на Ваши неподтвержденные лекции
        </div>
      }
      
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateMessages: (data) => dispatch(UpdateMessages(data)),
    SetChatConnFail: (failed) => dispatch(SetChatConnFail(failed)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
  })
)(NotificationsList);