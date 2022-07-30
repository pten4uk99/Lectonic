import React, {useEffect, useState} from 'react'
import {connect} from 'react-redux'

import {getDomainArray} from '../../../WorkRooms/CreateEvent/ajax/event'
import {DeleteDomain, UpdateDomain} from '~@/WorkRooms/CreateEvent/redux/actions/event'
import {AddPerfLink, AddPubLink, DeletePerfLink, DeletePubLink} from '../../redux/actions/lecturer'
import LecturerLink from './LecturerLink'
import DropDown from '../../../Utils/jsx/DropDown'
import btnDelete from '~/assets/img/btn-delete.svg'


function LecturerStep1(props) {
  let selectedDomains = props.store.event.domain
  let performancesLinks = props.store.addRole.lecturer.performances_links
  let publicationLinks = props.store.addRole.lecturer.publication_links

  let [domainArray, setDomainArray] = useState(null)
  let [deletedDomain, setDeletedDomain] = useState()

  function deleteElem(indexElem) {
    props.DeleteDomain(selectedDomains, indexElem)
    domainArray.push(deletedDomain)
    setDomainArray(domainArray.sort((a, b) => a.name > b.name ? 1 : -1))
  }

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

  function domainSelectHandler(value, setValue) {
    if (props.store.event.domain.length >= 10) return setValue('')
    props.UpdateDomain(value)
    setValue('')
  }

  return (
    <>
      <div className="step-block mt-24">
        <p className="step-block__left-part pt-0">
          Тематика лекций:
          <span className="required-sign step-block__required-sign">*</span>
        </p>
        <DropDown request={domainArray}
                  width={true}
                  placeholder='Выберите тематику'
                  onSelect={(value, setValue) => domainSelectHandler(value, setValue)}
                  domainArr={true}/>
      </div>
      <div className="step-block mt-12 margin-bottom-24">
        <p className="step-block__left-part pt-0"/>
        <div className='domain-list flex'>
          {selectedDomains.map((domain, index) => {
            return <div key={index} className='pill pill-grey'
                        onMouseUp={() => {
                          setDeletedDomain({name: domain})
                        }}>{domain}
              <div className='pill-btn-delete'
                   onClick={() => deleteElem(index)}>
                <img src={btnDelete} alt="delete"/>
              </div>
            </div>
          })}
        </div>
      </div>

      <LecturerLink label="Ссылки на видео Ваших выступлений:"
                    links={performancesLinks}
                    blur={props.AddPerfLink}
                    deleteLink={props.DeletePerfLink}/>
      <LecturerLink label="Ссылки на Ваши публикации:"
                    links={publicationLinks}
                    blur={props.AddPubLink}
                    deleteLink={props.DeletePubLink}/>
    </>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    UpdateDomain: (domain) => dispatch(UpdateDomain(domain)),
    DeleteDomain: (domain, i) => dispatch(DeleteDomain(domain, i)),
    AddPerfLink: (link) => dispatch(AddPerfLink(link)),
    DeletePerfLink: (link) => dispatch(DeletePerfLink(link)),
    AddPubLink: (link) => dispatch(AddPubLink(link)),
    DeletePubLink: (link) => dispatch(DeletePubLink(link))
  })
)(LecturerStep1)