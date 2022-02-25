import React, { useState } from "react";
import Header from "../Header";
import Modal from "../Modal";
import profileSelected from "~/assets/img/header_profile-selected.svg";
import profile from "~/assets/img/header_profile.svg";
import AuthSignUpPassword from "./AuthSignUpPassword";

function ContinueRegistration() {
  const [open, setOpen] = useState(true); //открыто модальное окно или нет

  return (
    <div>
      <Header
        src={open ? profileSelected : profile}
        onOpenAuth={() => setOpen(true)}
      />
      <Modal
        isOpened={open}
        onModalClose={() => setOpen(false)}
        styleBody={{ width: "432px" }}
      >
        <AuthSignUpPassword />
      </Modal>
    </div>
  );
}

export default ContinueRegistration;
