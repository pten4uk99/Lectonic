import React, {useEffect, useState} from 'react'
import {connect} from "react-redux";

import {getDomainArray} from "../../../CreateEvent/ajax/event";
import {domainSelectHandler} from "~@/CreateEvent/jsx/CreateEvent";
import {UpdateDomain} from "~@/CreateEvent/redux/actions/event";
import {UpdatePerfLinks, UpdatePubLinks} from "../../redux/actions/registerRole";
import LecturerLink from "../LecturerLink";


function LecturerStep1(props) {
  let selectedDomains = props.store.event.domain
  let performancesLinks = props.store.registerRole.performances_links
  let publicationLinks = props.store.registerRole.publication_links
  
  
  let [domainArray, setDomainArray] = useState(null)
  
  useEffect(() => {
    getDomainArray()
      .then(response => response.json())
      .then(data => setDomainArray(data.data))
      .catch(error => console.log(error))
  }, [])
  
  useEffect(() => {
    if (selectedDomains.length > 0) {
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
      
      <LecturerLink label="Ссылки на видео Ваших выступлений:"/>
      <LecturerLink label="Ссылки на видео Ваших публикаций:"/>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    UpdatePerfLinks: (links) => dispatch(UpdatePerfLinks(links)),
    UpdatePubLinks: (links) => dispatch(UpdatePubLinks(links)),
  })
)(LecturerStep1)