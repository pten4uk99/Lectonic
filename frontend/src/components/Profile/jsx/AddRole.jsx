import React, { useState } from 'react'
// import '~/styles/AddRole.styl'
import addRoleIcon from '~/assets/img/add-icon.svg'
import addRoleIconHover from '~/assets/img/add-icon-hover.svg'
import Icons from '~@/Profile/jsx/Icons'
import DropdownElement from '~@/Profile/jsx/DropdownElement'
// import DropDownElement from '~/components/DropdownElement'

export default function AddRole(props) {
  let roleSelect = {
    class: 'role-select',
    default: 'Добавить роль',
    options: ['Лектор', 'Заказчик'],
  }

  const [isClicked, setClicked] = useState(false)

  function handleAddRole() {
    setClicked(!isClicked)
  }

  return (
    <>
      <Icons
        srcNormal={addRoleIcon}
        srcHovered={addRoleIconHover}
        onClick={handleAddRole}
      />
      {isClicked ? (
        <DropdownElement selectDetails={roleSelect} className='role-select' />
      ) : (
        <p className='addRole-text'>Добавить роль</p>
      )}
    </>
  )
}
