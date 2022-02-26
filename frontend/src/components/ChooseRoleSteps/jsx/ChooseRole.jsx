import React, { useState } from 'react'
import Header from '~@/Layout/jsx/Header'
// import '~/styles/ChooseRole.styl'
// import DropDownElement from '~@/UserArea/jsx/DropdownElement'
import ChooseRole_Lecturer_step1 from './ChooseRole_Lecturer_step1'
import ChooseRole_Lecturer_step2 from './ChooseRole_Lecturer_step2'
import ChooseRole_Lecturer_step3 from './ChooseRole_Lecturer_step3'
import ChooseRole_Lecturer_step4 from './ChooseRole_Lecturer_step4'
import ChooseRole_Customer_step1 from './ChooseRole_Customer_step1'
import ChooseRole_Customer_step2 from './ChooseRole_Customer_step2'
import ChooseRole_Customer_step3 from './ChooseRole_Customer_step3'
import ChooseRole_Customer_step4 from './ChooseRole_Customer_step4'
import profileSelected from '~/assets/img/header_profile-selected.svg'

//пока есть вопрос по логике переключения шагов, уточняю
export default function ChooseRole() {
  const [isLecturerStep1, setLecturerStep1] = useState(false)
  const [isLecturerStep2, setLecturerStep2] = useState(false)
  const [isLecturerStep3, setLecturerStep3] = useState(false)
  const [isLecturerStep4, setLecturerStep4] = useState(false)

  const [isCustomerStep1, setCustomerStep1] = useState(false)
  const [isCustomerStep2, setCustomerStep2] = useState(false)
  const [isCustomerStep3, setCustomerStep3] = useState(false)
  const [isCustomerStep4, setCustomerStep4] = useState(false)

  const allLecturersFalse = () => {
    setLecturerStep1(false)
    setLecturerStep2(false)
    setLecturerStep3(false)
    setLecturerStep4(false)
  }

  const allCustomersFalse = () => {
    setCustomerStep1(false)
    setCustomerStep2(false)
    setCustomerStep3(false)
    setCustomerStep4(false)
  }

  function showLecturerStep1() {
    setLecturerStep1(true)
    setLecturerStep2(false)
    setLecturerStep3(false)
    setLecturerStep4(false)
    allCustomersFalse()
  }

  function showLecturerStep2() {
    setLecturerStep1(false)
    setLecturerStep2(true)
    setLecturerStep3(false)
    setLecturerStep4(false)
    allCustomersFalse()
  }

  function showLecturerStep3() {
    setLecturerStep1(false)
    setLecturerStep2(false)
    setLecturerStep3(true)
    setLecturerStep4(false)
    allCustomersFalse()
  }

  function showLecturerStep4() {
    setLecturerStep1(false)
    setLecturerStep2(false)
    setLecturerStep3(false)
    setLecturerStep4(true)
    allCustomersFalse()
  }

  function showCustomerStep1() {
    setCustomerStep1(true)
    setCustomerStep2(false)
    setCustomerStep3(false)
    setCustomerStep4(false)
    allLecturersFalse()
  }

  return (
    <>
      <Header src={profileSelected} />
      <div className='chooseRole__steps'>
        <div className='chooseRole__steps__text-wrapper'>
          <h2
            style={{
              color:
                isLecturerStep1 || isCustomerStep1
                  ? 'var(--main-blue)'
                  : 'var(--add-darkGrey)',
            }}
          >
            Шаг 1
          </h2>
          <h2
            style={{
              color:
                isLecturerStep2 || isCustomerStep2
                  ? 'var(--main-blue)'
                  : 'var(--add-darkGrey)',
            }}
          >
            Шаг 2
          </h2>
          <h2
            style={{
              color:
                isLecturerStep3 || isCustomerStep3
                  ? 'var(--main-blue)'
                  : 'var(--add-darkGrey)',
            }}
          >
            Шаг 3
          </h2>
          <h2
            style={{
              color:
                isLecturerStep4 || isCustomerStep4
                  ? 'var(--main-blue)'
                  : 'var(--add-darkGrey)',
            }}
          >
            Шаг 4
          </h2>
        </div>
        <div className='chooseRole__steps__bar'>
          <div
            className='chooseRole__steps__bar-current'
            style={{
              marginLeft: isLecturerStep2 || isCustomerStep2 ? '25%' : '',
            }}
          ></div>
        </div>
      </div>

      <div className='chooseRole__content-wrapper'>
        <div
          className='chooseRole__role'
          style={{
            display:
              isLecturerStep2 ||
              isLecturerStep3 ||
              isLecturerStep4 ||
              isCustomerStep2 ||
              isCustomerStep3 ||
              isCustomerStep4
                ? 'none'
                : 'block',
          }}
        >
          <div className='chooseRole__role__text'>
            <h2 className='choseRole-leftPart'>Выбор роли</h2>
            <p>
              Выберите Вашу основную роль на платформе:
              <br />
              лектор или заказчик лекции.
            </p>
          </div>
          <div className='chooseRole__content__block-wrapper'>
            <div className='choseRole-leftPart'>
              <div>
                Кто вы?<span className='required-sign chooseRole'>*</span>
              </div>
            </div>
            <button
              className={`${isLecturerStep1 ? 'btn-chosen' : 'btn-notChosen'}`}
              onClick={showLecturerStep1}
            >
              Лектор
            </button>
            <button
              className={`${isCustomerStep1 ? 'btn-chosen' : 'btn-notChosen'}`}
              onClick={showCustomerStep1}
            >
              Заказчик
            </button>
          </div>

          <ChooseRole_Lecturer_step1
            style={{ display: isLecturerStep1 ? 'block' : 'none' }}
          />
          <ChooseRole_Customer_step1
            style={{ display: isCustomerStep1 ? 'block' : 'none' }}
          />

          <div className='chooseRole__bottom-btns'>
            <button className='btn-outline'>Продолжить позже</button>
            <button className='btn' onClick={showLecturerStep2}>
              Следующий шаг
            </button>
          </div>
        </div>

        <ChooseRole_Lecturer_step2
          style={{ display: isLecturerStep2 ? 'block' : 'none' }}
        />
        <ChooseRole_Lecturer_step3
          style={{ display: isLecturerStep3 ? 'block' : 'none' }}
        />
        <ChooseRole_Lecturer_step4
          style={{ display: isLecturerStep4 ? 'block' : 'none' }}
        />

        <ChooseRole_Customer_step2
          style={{ display: isCustomerStep2 ? 'block' : 'none' }}
        />
        <ChooseRole_Customer_step3
          style={{ display: isCustomerStep3 ? 'block' : 'none' }}
        />
        <ChooseRole_Customer_step4
          style={{ display: isCustomerStep4 ? 'block' : 'none' }}
        />
      </div>
    </>
  )
}
