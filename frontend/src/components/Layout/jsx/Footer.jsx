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
          <a className="footer__rules-link" href="/license/polsovatelskoe_soglashenije.pdf" target="_blank">
            Условия использования
          </a>
          <a className="footer__rules-link" href="/license/politica_konfidentialnosty.pdf" target="_blank">
            Политика конфиденциальности
          </a>
        </div>

        <div className="footer__supportInfo is-desktop">
          Техническая поддержка:
          <br/>
          <span>support@lectonic.ru</span>
        </div>

        <div className="footer__socials">
          <p className="footer__socials-text">Мы в соц. сетях:</p>
          <div className="footer__socials-icons">
            <a href="https://web.telegram.org/z/#5485561224" target="_blank">
              <img className="footer__insta-icon" src={telegram} alt="Telegram"/>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
