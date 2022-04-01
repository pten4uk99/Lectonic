import React, {useEffect, useState} from "react";
import {connect} from "react-redux";
import ChatMessages from "./ChatMessages";
import NotificationsList from "./NotificationsList";


function ChatDropdown(props) {
  let [messagesArea, setMessagesArea] = useState(false)
  
  return (
    <div className="chat-dropdown__block">
      {!messagesArea ? 
        <NotificationsList setArea={setMessagesArea} 
                           setChatSocket={props.setChatSocket}/> : 
        <ChatMessages setArea={setMessagesArea} 
                      chatSocket={props.chatSocket}/>
      }
    </div>
  )
}


export default connect(
  state => ({store: state}),
  dispatch => ({})
)(ChatDropdown);