import React, {useEffect, useRef, useState} from "react";
import {connect} from "react-redux";

import backArrow from '~/assets/img/back-arrow.svg'
import sendMessage from '~/assets/img/send-message-icon.svg'
import {AddMessage} from "../../redux/actions/messages";


function ChatMessages(props) {
  let messages = props.store.messages
  let messagesBlock = useRef()
  
  useEffect(() => {
    setTimeout(() => messagesBlock.current.scrollTop =  messagesBlock.current.scrollHeight)
  }, [])
  
  useEffect(() => {
    props.chatSocket?.addEventListener('message', (e) => {
      let data = JSON.parse(e.data)
      props.AddMessage(data)
      messagesBlock.current.scrollTop =  messagesBlock.current.scrollHeight
    })
  }, [props.chatSocket])
  
  function handleArrowClick(chat_id) {
    props.setArea(false)
    props.chatSocket.close()
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
  
  return (
    <div className="chat-messages__block">
      <div className="actions__block">
        <div className="lecture">
          <div className="back-arrow" onClick={handleArrowClick}>
            <img src={backArrow} alt="назад"/>
          </div>
          <div className="text">
            <p className='lecture-name'>Лекция о ногах</p>
            <p className='respondent-name'>Лектор: Ножнич</p>
          </div>
        </div>
        <div className="buttons">
          <button className="confirm">Принять</button>
          <button className="reject">Отклонить</button>
        </div>
      </div>
      
      <div className="messages__block" ref={messagesBlock}>
        {messages.length > 0 && messages.map((elem, index) => {
          return <div key={index} className="block-message">
          <div className={props.store.permissions.user_id === elem.author ? 
            "self-message" : "other-message"}>{elem.text}</div>
        </div>
        })}
      </div>
      
      <div className="input__block">
        <input name="" 
               placeholder='Введите текст' 
               onKeyUp={(e) => handleSendMessage(e)}/>
        <img src={sendMessage} 
             alt="отправить"/>
      </div>
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    AddMessage: (message) => dispatch(AddMessage(message))
  })
)(ChatMessages);