import React, {useEffect, useRef, useState} from "react";
import {connect} from "react-redux";

import backArrow from '~/assets/img/back-arrow.svg'
import sendMessage from '~/assets/img/send-message-icon.svg'
import {AddMessage} from "../../redux/actions/messages";
import {SetSelectedChat} from "../../redux/actions/header";
import {toggleConfirmResponseOnLecture, toggleResponseOnLecture} from "../../../WorkRooms/WorkRoom/ajax/workRooms";
import {RemoveNotification} from "../../redux/actions/notifications";


function ChatMessages(props) {
  let data = props.store.messages
  let messages = data.messages
  let messagesBlock = useRef()
  let input = useRef()
  
  useEffect(() => {
    if (messagesBlock) messagesBlock.current.scrollTop = messagesBlock.current.scrollHeight
  }, [messagesBlock?.current?.scrollHeight])
  
  useEffect(() => {
    props.chatSocket?.addEventListener('message', (e) => {
      let data = JSON.parse(e.data)
      props.AddMessage(data)
    })
  }, [props.chatSocket])
  
  function handleArrowClick() {
    props.setArea(false)
    props.chatSocket.close()
    props.SetSelectedChat(null)
  }
  
  function handleSendMessage(e) {
    if (e.keyCode === 13) {
      props.chatSocket.send(JSON.stringify({
        'type': 'chat_message',
        'author': props.store.permissions.user_id,
        'text': e.target.value,
      }))
      e.target.value = ''
    }
  }
  function handleClickIcon() {
    props.chatSocket.send(JSON.stringify({
      'type': 'chat_message',
      'author': props.store.permissions.user_id,
      'text': input.current.value,
    }))
    input.current.value = ''
  }
  
  function handleToggleConfirm(reject) {
    toggleConfirmResponseOnLecture(data.lecture_id, data.talker_respondent, reject)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          // props.setArea(false)
          // props.chatSocket.close()
          // props.SetSelectedChat(null)
          if (reject) {
            props.RemoveNotification(props.store.header.selectedChatId)
          }
        }
      })
  }
  function handleRejectResponse() {
    toggleResponseOnLecture(data.lecture_id)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          handleArrowClick()
          props.RemoveNotification(props.store.header.selectedChatId)
        }
      })
  }
  
  return (
    <div className="chat-messages__block">
      <div className="actions__block">
        <div className="lecture">
          <div className="back-arrow" onClick={handleArrowClick}>
            <img src={backArrow} alt="назад"/>
          </div>
          <div className="text">
            <p className='lecture-name'>{data.lecture_name}</p>
            <p className='respondent-name'>{data.talker_first_name} {data.talker_last_name}</p>
          </div>
        </div>
        <div className="buttons">
          {data.confirmed === null ? 
            data.is_creator ? 
              <>
                <button className="confirm" onClick={() => handleToggleConfirm(false)}>Принять</button>
                <button className="reject" onClick={() => handleToggleConfirm(true)}>Отклонить</button>
              </> : 
              <button className="reject-response" onClick={handleRejectResponse}>Отменить отклик</button> :
            data.confirmed ? 
              <div className="lecture-confirmed">Лекция подтверждена</div> : 
              <div className="lecture-rejected">Лекция отклонена</div>
          }

        </div>
      </div>
      
      <div className="messages__block" ref={messagesBlock}>
        {messages && messages.length > 0 && messages.map((elem, index) => {
          if (elem.confirm) return <div key={index} className="block-message">
            <div className="confirm-message">Лекция подтверждена!</div>
          </div>
          else if (elem.confirm === null) return <div key={index} className="block-message">
            <div className={props.store.permissions.user_id === elem.author ? 
              "self-message" : "other-message"}>{elem.text}</div>
          </div>
          else if (!elem.confirm) return <div key={index} className="block-message">
            <div className="reject-message">Лекция отклонена!</div>
          </div>
        })}
      </div>
      
      <div className="input__block">
        <input placeholder='Введите текст' 
               onKeyUp={(e) => handleSendMessage(e)} 
               ref={input}/>
        <img src={sendMessage} 
             alt="отправить" 
             onClick={handleClickIcon}/>
      </div>
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    AddMessage: (message) => dispatch(AddMessage(message)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
  })
)(ChatMessages);