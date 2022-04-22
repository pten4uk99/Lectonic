import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import ChatMessages from "./ChatMessages";
import NotificationsList from "./NotificationsList";
import {getChatMessages} from "../../ajax";
import {UpdateMessages} from "../../redux/actions/messages";
import {ActiveChatDropdown, SetSelectedChat} from "../../redux/actions/header";
import {RemoveNotification, SetNeedRead} from "../../redux/actions/notifications";


function ChatDropdown(props) {
  let [messagesArea, setMessagesArea] = useState(false)
  let [isLoaded, setIsLoaded] = useState(false)
  let [chatId, setChatId] = useState(null)
  let [func, setFunc] = useState(null)
  
  function getMessages(chat_id) {
    getChatMessages(chat_id)
      .then(r => r.json())
      .then(data => {
        if (data.status === 'success') {
          props.UpdateMessages(data.data[0])
          props.SetNeedRead(chat_id, false)
          props.SetSelectedChat(chat_id)
          setIsLoaded(true)
        } else {
          props.RemoveNotification(chat_id)
          setMessagesArea(false)
        }
      })
  }
  
  useEffect(() => {
    if (chatId) setMessagesArea(true)
  }, [chatId])
  
  useEffect(() => {
    if (messagesArea) {
      setIsLoaded(false)
      getMessages(chatId)
      setFunc(setInterval(() => getMessages(chatId), 3000))
    }
    else {
      clearInterval(func)
      setChatId(null)
    }
  }, [messagesArea])
  
  return (
    <div className="chat-dropdown__block">
      {!messagesArea ? 
        <NotificationsList setArea={setMessagesArea}
                           setChatId={setChatId}
                           setChatSocket={props.setChatSocket} 
                           chatSocket={props.chatSocket} 
                           setIsLoaded={setIsLoaded}/> : 
        <ChatMessages setArea={setMessagesArea} 
                      chatSocket={props.chatSocket} 
                      isLoaded={isLoaded}/>
      }
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateMessages: (data) => dispatch(UpdateMessages(data)),
    ActiveChatDropdown: (active) => dispatch(ActiveChatDropdown(active)),
    SetSelectedChat: (chat_id) => dispatch(SetSelectedChat(chat_id)),
    SetNeedRead: (chat_id, need_read) => dispatch(SetNeedRead(chat_id, need_read)),
    RemoveNotification: (chat_id) => dispatch(RemoveNotification(chat_id)),
  })
)(ChatDropdown);