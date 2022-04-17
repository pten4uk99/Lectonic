import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import ChatMessages from "./ChatMessages";
import NotificationsList from "./NotificationsList";


function ChatDropdown(props) {
  let [messagesArea, setMessagesArea] = useState(false)
  let [isLoaded, setIsLoaded] = useState(false)
  
  return (
    <div className="chat-dropdown__block">
      {!messagesArea ? 
        <NotificationsList setArea={setMessagesArea} 
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
  dispatch => ({})
)(ChatDropdown);