import React, { useState } from "react";
import "~/styles/AddRole.css";
import addRoleIcon from "~/assets/img/addRole-icon.svg";
import addRoleIconHover from "~/assets/img/addRole-icon-hover.svg";
import Icons from "~/components/Icons";
import DropdownElement from "~/components/DropdownElement";
import DropDownElement from "~/components/DropdownElement";

export default function AddRole(props) {
  let roleSelect = {
    class: "role-select",
    default: "Добавить роль",
    options: ["Лектор", "Заказчик"],
  };

  const [isClicked, setClicked] = useState(false);

  function handleAddRole() {
    setClicked(!isClicked);
  }

  return (
    <>
      <Icons
        srcNormal={addRoleIcon}
        srcHovered={addRoleIconHover}
        onClick={handleAddRole}
      />
      {isClicked ? (
        <DropdownElement selectDetails={roleSelect} className="role-select" />
      ) : (
        <p className="addRole-text">Добавить роль</p>
      )}
    </>
  );
}
