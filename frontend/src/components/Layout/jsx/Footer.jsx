import React from 'react'
import {Link, useLocation} from 'react-router-dom'
// import '~/styles/Footer.styl'
import telegram from '~/assets/img/footer-telegram.svg'

export default function Footer() {
  let location = useLocation()
  return (
    <footer style={location.pathname === '/' ? {zIndex: 9} : {}}>
      <div className="footer-wrapper">
        <div className="footer__copyright">2022 © Сервис Lectonic</div>
        <div className="footer__rules">
          <a className="footer__rules-link" href="/license/polsovatelskoe_soglashenije.html" target="_blank">
            Условия использования
          </a>
          <a className="footer__rules-link" href="/license/politica_konfidentialnosty.html" target="_blank">
            Политика конфиденциальности
          </a>
        </div>

        <div className="footer__socials">
          <p className="footer__socials-text">Тех. поддержка:</p>
          <span>support@lectonic.com</span>
          <a href="https://t.me/LectonicSupport_bot" target="_blank" rel="noreferrer">
            <img className="footer__insta-icon" src={telegram} alt="LectonicSupport"/>
          </a>
        </div>
      </div>
    </footer>
  );
}
