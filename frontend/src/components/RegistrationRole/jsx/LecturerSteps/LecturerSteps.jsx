import React, {useEffect, useState} from 'react'
import {useNavigate} from 'react-router-dom'

import {connect} from "react-redux";
import {SwapSelectedRole, SwapStep} from "../../redux/actions/registerRole";
import LecturerStep1 from "./LecturerStep1";
import LecturerStep2 from "./LecturerStep2";
import LecturerStep3 from "./LecturerStep3";
import {createLecturer, uploadDiplomaPhotos, uploadDocumentPhoto} from "../../ajax";
import {reverse} from "../../../../ProjectConstants";


function LecturerSteps(props) {
  let navigate = useNavigate()
  if (props.store.permissions.is_lecturer) navigate(reverse('workroom'))
  
  let currentStep = props.store.registerRole.step
  
  let role = props.store.registerRole
  let domainList = props.store.event.domain
  let perfLinks = role.performances_links
  let pubLinks = role.publication_links
  let education = role.education
  let hallAddress = role.hall_address
  let equipment = role.equipment
  
  function handleSubmit(e) {
    console.log('пошол субмит блин')
    e.preventDefault()
    let formData = new FormData()
    
    for (let link of pubLinks) formData.append('publication_links', link)
    for (let link of perfLinks) formData.append('performances_links', link)
    for (let domain of domainList) formData.append('domain', domain)
    formData.set('education', education)
    formData.set('hall_address', hallAddress)
    formData.set('equipment', equipment)
    
    createLecturer(formData)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'created') {
          console.log('лекция создава успешно')
          let diploma = new File(role.diploma_photos, 'diploma.png')
          let diplomaForm = new FormData()
          diplomaForm.set('diploma', diploma)
          uploadDiplomaPhotos(diplomaForm)
            .then(response => response.json())
            .then(data => navigate(reverse('workroom')))
            .catch(error => console.log(error))
        }
      })
      .catch(error => console.log(error))
    
    let passport = new File([role.passport_photo], 'passport.png')
    let selfie = new File([role.selfie_photo], 'selfie.png')
    let documentForm = new FormData()
    documentForm.set('passport', passport)
    documentForm.set('selfie', selfie)
    uploadDocumentPhoto(documentForm)
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log(error))
  }

  useEffect(() => {
    props.SwapSelectedRole('lecturer')
  }, [])
  
  return (
    <form onSubmit={(e) => handleSubmit(e)}>
      {currentStep === 0 ? 
        <></> :
        currentStep === 1 ?
        <LecturerStep1/> :
          currentStep === 2 ?
        <LecturerStep2/> : 
            currentStep === 3 ? 
              <LecturerStep3/> : 
              <></>}
    </form>
  )
}

export default connect(
  state => ({store: state}),
  dispatch => ({
    SwapSelectedRole: (role) => dispatch(SwapSelectedRole(role)),
    SwapStep: (step) => dispatch(SwapStep(step))
  })
)(LecturerSteps)