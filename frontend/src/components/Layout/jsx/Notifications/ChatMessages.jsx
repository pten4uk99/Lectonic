import React, {useState} from "react";
import {connect} from "react-redux";

import backArrow from '~/assets/img/back-arrow.svg'
import sendMessage from '~/assets/img/send-message-icon.svg'


function ChatMessages(props) {
  let [inputMessage, setInputMessage] = useState('')
  
  function handleSendMessage(e) {
    if (props.notificationsSocket) {
      props.notificationsSocket.send(JSON.stringify({message: inputMessage}))
      console.log('Отправлено')
    }
  }
  
  return (
    <div className="chat-messages__block">
      <div className="actions__block">
        <div className="lecture">
          <div className="back-arrow" onClick={() => props.setArea(false)}>
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
      
      <div className="messages__block">
        <div className="block-message">
          <div className="self-message">Привет андрей блин</div>
        </div>
        <div className="block-message">
          <div className="other-message">Пока нафиг андрей блин</div>
        </div>
        
      </div>
      
      <div className="textarea__block">
        <textarea name="" 
                  placeholder='Введите текст' 
                  onChange={(e) => setInputMessage(e.target.value)}/>
        <img src={sendMessage} 
             alt="отправить" 
             onClick={(e) => handleSendMessage(e)}/>
      </div>
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(ChatMessages);