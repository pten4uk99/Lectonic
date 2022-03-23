import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import {getDomainArray} from "../../../WorkRooms/CreateEvent/ajax/event";
import {domainSelectHandler} from "~@/WorkRooms/CreateEvent/jsx/CreateEvent";
import {UpdateDomain} from "~@/WorkRooms/CreateEvent/redux/actions/event";
import {UpdatePerfLinks, UpdatePubLinks} from "../../redux/actions/lecturer";
import LecturerLink from "./LecturerLink";


function LecturerStep1(props) {
  let selectedDomains = props.store.event.domain
  let performancesLinks = props.store.addRole.lecturer.performances_links
  let publicationLinks = props.store.addRole.lecturer.publication_links
  
  
  let [domainArray, setDomainArray] = useState(null)
  
  useEffect(() => {
    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])
  
  useEffect(() => {
    if (selectedDomains.length > 0 && domainArray) {
      let newDomainArray
      newDomainArray = domainArray.filter(elem => !selectedDomains.includes(elem.name))
      setDomainArray(newDomainArray)
    }
  }, [selectedDomains])
  
  return (
    <>
      <div className="step-block margin-bottom-24">
        <p className="step-block__left-part">
          Тематика лекций:
          <span className="required-sign step-block__required-sign">*</span>
        </p>
        <div className='domain-list flex'>
            <select className='selector'
                    onChange={e => domainSelectHandler(e, props)}>
              <option value='' disabled selected>Выберите тематику</option>
              {domainArray ? domainArray.map((elem) => {
                return <option key={elem.id} value={elem.id}>{elem.name}</option>
              }): <></>}
            </select>
            {selectedDomains.map((domain, index) => {
              return <div key={index} className='pill pill-grey'>{domain}</div>
            })}
          </div>
      </div>
      
      <LecturerLink label="Ссылки на видео Ваших выступлений:" 
                    links={performancesLinks}
                    blur={props.UpdatePerfLinks}/>
      <LecturerLink label="Ссылки на видео Ваших публикаций:" 
                    links={publicationLinks}
                    blur={props.UpdatePubLinks}/>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    UpdatePerfLinks: (link, index) => dispatch(UpdatePerfLinks(link, index)),
    UpdatePubLinks: (link, index) => dispatch(UpdatePubLinks(link, index)),
  })
)(LecturerStep1)