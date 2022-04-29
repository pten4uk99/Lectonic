import React, {useEffect, useState} from "react";
import {connect} from "react-redux";

import {UpdateMessages} from "../../redux/actions/messages";
import {RemoveNotification, SetNeedRead} from "../../redux/actions/notifications";
import {SetSelectedChat} from "../../redux/actions/header";
import {getLecturePhoto} from "../../../../ProjectConstants";
import {SetChatConnFail} from "../../redux/actions/ws";
import myLectureIcon from "~/assets/img/chat/my-lecture-icon.svg"
import myResponseIcon from "~/assets/img/chat/my-response-icon.svg"
import PhotoName from "../../../Utils/jsx/PhotoName";


function NotificationsList(props) {
  let chatList = props.store.notifications
  let userId = props.store.permissions.user_id
  let onlineUsers = props.store.ws.onlineUsers
  
  function getClassName(elem) {
    let className = 'chat-dropdown__notification'
    if (elem.respondent_id == userId && elem.chat_confirm !== null && !elem.chat_confirm) {
      className += ' disabled'
    }
    return className
  }

  return (
    <div className="notifications-list__block">
      <div className="notification__header">Отклики</div>

      {chatList.length > 0 ? chatList.map((elem) => {
        return <li key={elem.id} 
                   className={getClassName(elem)}
                   onClick={() => props.setChatId(elem.id)}>
          <div className="talker-photo">
            <PhotoName firstName={elem.talker_first_name} 
                       lastName={elem.talker_last_name} 
                       size={32} 
                       colorNumber={2}/>
          </div>
          <div className="photo"><img src={getLecturePhoto(elem.lecture_svg)} alt="обложка"/></div>
          <img src={elem.respondent_id == userId ? myLectureIcon : myResponseIcon} alt="" className="lecture-response-icon"/>
          <div className="text">
            <p className='lecture-name'>{elem.lecture_name}</p>
            <p className='respondent-name'>{elem.talker_first_name} {elem.talker_last_name}</p>
            {onlineUsers.includes(elem.respondent_id) ? 
              <p className='is-online'>В сети</p> : <p className='is-offline'>Не в сети</p>}
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