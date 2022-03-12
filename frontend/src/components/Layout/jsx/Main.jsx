import React, { useState } from 'react'
import Header from './Header'
import Modal from './Modal'
import Authorization from '~@/Authorization/jsx/Authorization'
import profileSelected from '~/assets/img/header_profile-selected.svg'
import profile from '~/assets/img/header_profile.svg'
import mainIllustration from '~/assets/img/main-illustration.svg'
// import '~/styles/Main.styl'

export default function Main() {
  const [open, setOpen] = useState(false) //открыто модальное окно или нет

  return (
    <>
      <Header
        src={open ? profileSelected : profile}
        onOpenAuth={() => setOpen(true)}
      />
      <Modal
        isOpened={open}
        onModalClose={() => setOpen(false)}
        styleBody={{ width: '400px' }}
      >
        <Authorization />
      </Modal>
      <div className="main">
        <div className="main__text-wrapper">
          <p className="main__text-header">
            Платформа для лекторов
            <br />и не только!
          </p>
          <p className="main__text">
            Работаем, чтобы слушатели слышали,
            <br />а лекторы читали.
          </p>
          <button className="btn main__btn" onClick={() => setOpen(true)}>
            Присоединиться
          </button>
        </div>
        <div className="main__illustration-wrapper">
          <img
            className="main__illustration"
            src={mainIllustration}
            alt="Иллюстрация"
          />
        </div>
      </div>
    </>
  );
}

