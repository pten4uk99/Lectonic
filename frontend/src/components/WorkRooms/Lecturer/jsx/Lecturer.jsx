import React, { useEffect, useRef, useState } from 'react'
import { connect } from 'react-redux'
import bg from '~/assets/img/lecturer/bg.svg'
import photo_profile from '~/assets/img/lecturer/profile_photo.png'
import empty_card from '~/assets/img/lecturer/empty_card.svg'
import edit_photo from '~/assets/img/lecturer/edit_photo.svg'
import card1 from '~/assets/img/lecturer/potential1.svg'
import card2 from '~/assets/img/lecturer/potential2.svg'
import card3 from '~/assets/img/lecturer/potential3.svg'
import card4 from '~/assets/img/lecturer/potential4.svg'
import card5 from '~/assets/img/lecturer/potential5.svg'

import mini_photo from '~/assets/img/lecturer/mini_photo.svg'

import LectureCard from './LectureCard'
import PotentialCard from './PotentialCard'
import Calendar from '~@/WorkRooms/Calendar/jsx/Calendar'
import DateDetail from '~@/WorkRooms/DateDetail/jsx/DateDetail'
import Customer from './Customer'
import { Link } from 'react-router-dom'
import logo from '~/assets/img/header_logo.svg'
import iconSearch from '~/assets/img/icon-search.svg'
import iconChat from '~/assets/img/lecturer/chat.svg'
import instagram from '~/assets/img/footer-instagram.svg'
import vk from '~/assets/img/footer-vkontakte.svg'
import fb from '~/assets/img/footer-facebook.svg'
import history from '~/assets/img/lecturer/history.svg'
import shadow from '~/assets/img/lecturer/shadow.svg'
import add_role from '~/assets/img/lecturer/add_role.svg'

import chatLecturer from '~/assets/img/lecturer/chat_lecturer_temporary.svg'
import chatCustomer from '~/assets/img/lecturer/chat_customer_temporary.svg'
import PopUpChat from './PopUpChat'

function Lecturer(props) {
  /*работа с чатом*/
  const [open, setOpen] = useState(false) //открыто модальное окно или нет

  let [lecturer, swapLecturer] = useState(true)
  let l_profile = useRef()
  let c_profile = useRef()

  useEffect(() => {
    activateLecturer()
  }, [])

  function activateLecturer() {
    swapLecturer(true)
    l_profile.current.classList.add('active')
    c_profile.current.classList.remove('active')
  }
  function activateCustomer() {
    swapLecturer(false)
    c_profile.current.classList.add('active')
    l_profile.current.classList.remove('active')
  }

  return (
    <>
      <header className='profile__header'>
        <Link to='/'>
          <img className='header-logo' src={logo} alt='логотип' />
        </Link>

        <nav className='header__nav'>
          <img className='header__nav-search' src={iconSearch} alt='поиск' />
          <img
            className='header__nav-chat'
            src={iconChat}
            alt='чат'
            onClick={() => setOpen(true)}
          />

          <img
            className='header__nav-profile'
            src={mini_photo}
            alt='ваш профиль'
            onClick={props.onOpenAuth}
          />
        </nav>
      </header>

      {/*Чат-картинка открывается в модальном окне*/}
      <PopUpChat
        isOpened={open}
        onModalClose={() => setOpen(false)}
        styleBody={{ width: '980px' }}
      >
        <img
          className='profile__chat-svg'
          src={lecturer ? chatLecturer : chatCustomer}
        />
      </PopUpChat>

      <div className='full__profile'>
        <div className='lecturer__background'>
          <img src={bg} alt='Фон' />
        </div>
        <div className='lecturer__profile__header'>
          <div className='profile-photo'>
            <img src={photo_profile} alt='Фон' />
            <div className='edit-photo'>
              <img src={edit_photo} alt='' />
            </div>
          </div>
          {/*<div className="additional-info">*/}
          {/*    <div className="edit-photo"><img src={additional} alt=""/></div>*/}
          {/*    Дополнительная информация*/}
          {/*</div>*/}
          <div className='profile-name'>
            <span>Марк</span>
            <span>Туллий</span>
            <span>Цицерон</span>
          </div>
          {/*Добавляю дивы для отображения ролей профиля */}
          <img className='add-lecturer-role' src={add_role} alt='' />
          <div className='profile-roles-btn lecturer-role'>Лектор</div>
          <div className='profile-roles-btn'>Заказчик</div>
        </div>
        <div
          className='lecturer__profile'
          onClick={() => {
            swapLecturer(true)
            activateLecturer()
          }}
          ref={l_profile}
        >
          Лектор
        </div>
        <div
          className='customer__profile'
          onClick={() => {
            swapLecturer(false)
            activateCustomer()
          }}
          ref={c_profile}
        >
          Заказчик
        </div>
        {lecturer ? (
          <main className='lecturer__main'>
            <div className='lecturer__wrapper'>
              <section className='in-projects'>
                <div className='header'>Участие в проектах</div>
                <div className='projects'>
                  <div className='project'>
                    Лидеры-доноры<span>3</span>
                  </div>
                  <div className='project'>
                    Научные субботы<span>5</span>
                  </div>
                  <div className='project'>
                    Клуб Эльбрус<span>2</span>
                  </div>
                </div>
              </section>
              <section className='created-lectures'>
                <div className='header'>
                  Созданные лекции <span>?</span>
                </div>
                <div className='lecture__cards'>
                  <div className='lecture__card__empty'>
                    <img src={empty_card} alt='' />
                  </div>
                  <LectureCard />
                </div>
              </section>
              <section className='potential-orders'>
                <div className='header'>
                  Потенциальные заказы<span>?</span>
                </div>
                <div className='lecture__cards'>
                  <PotentialCard
                    photo={card1}
                    header='Лидеры-доноры'
                    body='Лекции от создателей проекта о донорстве'
                  />
                  <PotentialCard
                    photo={card2}
                    header='Научные субботы'
                    body='Лекции от известных учёных о самых актуальных исследованиях'
                  />
                  <PotentialCard
                    photo={card3}
                    header='Лидеры-доноры'
                    body='Лекции от создателей проекта о донорстве'
                  />
                  <PotentialCard
                    photo={card4}
                    header='Научные субботы'
                    body='Лекции от известных учёных о самых актуальных исследованиях'
                  />
                  <PotentialCard
                    photo={card5}
                    header='Лидеры-доноры'
                    body='Лекции от создателей проекта о донорстве'
                  />
                  <PotentialCard
                    photo={card1}
                    header='Лидеры-доноры'
                    body='Лекции от создателей проекта о донорстве'
                  />
                </div>
              </section>
              <section className='confirmed-lectures'>
                <div className='header'>
                  Подтверждённые лекции<span>?</span>
                </div>
                <div className='lecture__cards'>
                  <LectureCard />
                </div>
              </section>
              <section className='lecturer-calendar'>
                <div className='header'>Календарь лектора</div>
                <div className='calendar__wrapper'>
                  <Calendar />
                  <DateDetail date={props.store.calendar.checkedDate} />
                </div>
              </section>
              <section className='bottom'>
                <div className='header'>
                  <span className='first' />
                  Событие не подтверждено
                </div>
                <div className='header'>
                  <span className='second' />
                  Событие подтверждено
                </div>
              </section>
            </div>
          </main>
        ) : (
          <Customer lecturer={lecturer} />
        )}
        <div className='history'>
          <img src={history} alt='' />
        </div>
        <div className='shadow'>
          <img src={shadow} alt='' />
        </div>
        <footer className='my_footer'>
          <div className='footer-wrapper'>
            <div className='footer__rulesLinks'>
              <Link to=''>
                <p className='footer__rulesLinks-text conditions'>
                  Условия использования
                </p>
              </Link>
              <Link to=''>
                <p className='footer__rulesLinks-text'>
                  Политика конфиденциальности
                </p>
              </Link>
            </div>

            <div className='footer__supportInfo'>
              <p className='footer__supportInfo-text'>
                Техническая поддержка:
                <br />
                <span>support@lectonic.ru</span>
              </p>
            </div>

            <div className='footer__socials'>
              <p className='footer__socials-text'>Мы в соц. сетях:</p>
              <div className='footer__socials-icons'>
                <a
                  href='https://www.instagram.com/'
                  rel='noreferrer'
                  target='_blank'
                >
                  <img src={instagram} alt='Instagram' />
                </a>
                <a href='https://www.vk.com' rel='noreferrer' target='_blank'>
                  <img src={vk} alt='VKontakte' />
                </a>
                <a
                  href='https://www.facebook.com'
                  rel='noreferrer'
                  target='_blank'
                >
                  <img src={fb} alt='Facebook' />
                </a>
              </div>
            </div>
          </div>
          <div className='footer__copyright'>2022 © Сервис Lectonic</div>
        </footer>
      </div>
    </>
  )
}

export default connect(
  state => ({ store: state }),
  dispatch => ({})
)(Lecturer)
